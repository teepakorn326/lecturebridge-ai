# LectureBridge AI — Database Schema Draft

## Purpose

This document describes the initial relational database schema planned for LectureBridge AI.

The schema is designed around the main data flow:

```text
Lecture
   |
   v
Source Files
   |
   v
Chunks
   |
   v
Embedding / Retrieval
```

The first implementation will use PostgreSQL.

Vector embeddings will be stored using the `pgvector` extension.

Database migrations are intentionally deferred until Day 5.

## 1. High-Level Relationship

```text
lectures
   |
   | 1
   |
   | many
   v
source_files
   |
   | 1
   |
   | many
   v
chunks
```

A lecture may contain multiple source files.

A source file may produce multiple retrieval chunks.

## 2. Lectures Table

```sql
lectures (
    id,
    title,
    target_language,
    created_at
)
```

Possible PostgreSQL representation:

```sql
CREATE TABLE lectures (
    id UUID PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    target_language VARCHAR(20) NOT NULL,
    created_at TIMESTAMPTZ NOT NULL
);
```

### Responsibilities

The `lectures` table represents a lecture workspace.

Examples:

```text
COMP8460 Week 7
COMP6350 Week 5
Machine Learning Lecture 3
```

A lecture groups multiple related learning materials together.

## 3. Source Files Table

```sql
source_files (
    id,
    lecture_id,
    filename,
    source_type,
    status,
    created_at
)
```

Possible PostgreSQL representation:

```sql
CREATE TABLE source_files (
    id UUID PRIMARY KEY,

    lecture_id UUID NOT NULL
        REFERENCES lectures(id),

    filename VARCHAR(255) NOT NULL,

    source_type VARCHAR(20) NOT NULL,

    status VARCHAR(30) NOT NULL,

    created_at TIMESTAMPTZ NOT NULL
);
```

### Responsibilities

The `source_files` table stores metadata about uploaded lecture materials.

Examples:

```text
lecture.pdf
slides.pptx
lecture.vtt
notes.txt
```

The original binary file itself does not need to be stored directly in PostgreSQL.

In production, files may be stored in Object Storage such as S3 or Google Cloud Storage.

A future version may therefore add:

```sql
storage_key
mime_type
file_size
```

to this table.

## 4. Chunks Table

```sql
chunks (
    id,
    source_file_id,
    chunk_index,
    text,
    page_number,
    slide_number,
    timestamp_start,
    timestamp_end,
    embedding vector(1536)
)
```

Possible PostgreSQL representation:

```sql
CREATE TABLE chunks (
    id UUID PRIMARY KEY,

    source_file_id UUID NOT NULL
        REFERENCES source_files(id),

    chunk_index INTEGER NOT NULL,

    text TEXT NOT NULL,

    page_number INTEGER,

    slide_number INTEGER,

    timestamp_start DOUBLE PRECISION,

    timestamp_end DOUBLE PRECISION,

    embedding vector(1536),

    UNIQUE (
        source_file_id,
        chunk_index
    )
);
```

The `vector(1536)` column requires the PostgreSQL `pgvector` extension.

That extension will be enabled during Day 5.

## 5. Why Citation Metadata Is Stored Directly on Chunks

LectureBridge intentionally denormalises citation metadata into the `chunks` table.

Each chunk stores citation fields directly:

```text
page_number
slide_number
timestamp_start
timestamp_end
```

instead of requiring a separate `segments` table.

### Alternative Normalised Design

A more normalised schema could look like:

```text
source_files
     |
     v
segments
     |
     v
chunks
```

For example:

```sql
segments (
    id,
    source_file_id,
    page_number,
    slide_number,
    timestamp_start,
    timestamp_end
)

chunks (
    id,
    segment_id,
    chunk_index,
    text,
    embedding
)
```

This design reduces duplicated metadata.

However, LectureBridge does not initially use this design.

## 6. Read Path Drives the Decision

The primary RAG read path is:

```text
User Question
      |
      v
Vector Search
      |
      v
Retrieved Chunk
      |
      v
LLM Answer
      |
      v
Citation
```

When retrieval returns a chunk, the application usually needs both:

```text
chunk.text
+
citation information
```

immediately.

With denormalised citation columns:

```text
Retrieved chunk
      |
      +-- text
      +-- page_number
      +-- slide_number
      +-- timestamp
```

the application can build the citation directly.

Example:

```text
lecture.pdf, page 3
```

without retrieving a separate segment row.

## 7. Why Not Require a Segment Join

A normalised schema would require a relationship such as:

```text
chunks
  ↓
segments
  ↓
source_files
```

when constructing citations.

Conceptually:

```sql
SELECT
    chunks.text,
    segments.page_number,
    segments.slide_number,
    segments.timestamp_start,
    source_files.filename
FROM chunks
JOIN segments
    ON chunks.segment_id = segments.id
JOIN source_files
    ON segments.source_file_id = source_files.id;
```

This is technically valid.

However, citation metadata is part of the hot RAG read path.

The application expects retrieval to quickly return:

```text
text
+
source metadata
```

For the MVP, avoiding an additional segment lookup keeps the retrieval model simpler.

## 8. Denormalisation Trade-Off

Denormalisation introduces duplicated data.

For example, if page 3 produces three chunks:

```text
Chunk 0 → page_number = 3
Chunk 1 → page_number = 3
Chunk 2 → page_number = 3
```

The value `3` is repeated.

This is intentional.

### Benefits

- simpler RAG read path
- citation metadata available immediately
- fewer joins during retrieval
- simpler application mapping
- easier debugging
- retrieved chunk is self-contained

### Costs

- citation metadata is duplicated
- storage usage is slightly higher
- updates could require modifying multiple chunk rows
- duplicated values can theoretically become inconsistent

## 9. Why Duplication Is Acceptable Here

LectureBridge treats parsed source content as effectively immutable.

The expected workflow is:

```text
Upload Source File
      |
      v
Parse Once
      |
      v
Create Segments
      |
      v
Create Chunks
      |
      v
Persist Chunks
```

The application does not normally edit a parsed page, slide or transcript segment after ingestion.

If a source file changes, the expected behaviour is to reprocess that source rather than manually update individual segment metadata.

Therefore, the main disadvantage of denormalisation:

```text
keeping duplicated metadata synchronized
```

is small for this workflow.

## 10. Read-Optimised Schema

This schema is deliberately optimised for the dominant access pattern.

LectureBridge performs far more retrieval reads than citation metadata updates.

The design therefore prefers:

```text
slightly more duplicated storage
```

in exchange for:

```text
simpler and faster retrieval
```

This is a common database design trade-off.

Normalization is not always automatically better.

Schema design should reflect actual read and write patterns.

## 11. Example Data

### lectures

```text
id:              lecture-001
title:           COMP8460 Week 7
target_language: th
```

### source_files

```text
id:          source-001
lecture_id:  lecture-001
filename:    week7.pdf
source_type: pdf
status:      ready
```

### chunks

```text
id:             chunk-001
source_file_id: source-001
chunk_index:    0
text:           "Self-attention allows..."
page_number:    3
embedding:      [...]
```

Another chunk from the same page:

```text
id:             chunk-002
source_file_id: source-001
chunk_index:    1
text:           "Query, key and value..."
page_number:    3
embedding:      [...]
```

Both chunks duplicate:

```text
page_number = 3
```

because each chunk should be usable independently after retrieval.

## 12. Expected Day 5 Query

Conceptually, vector retrieval will eventually look similar to:

```sql
SELECT
    id,
    source_file_id,
    chunk_index,
    text,
    page_number,
    slide_number,
    timestamp_start,
    timestamp_end
FROM chunks
ORDER BY embedding <=> :query_embedding
LIMIT 5;
```

The exact pgvector operator and indexing strategy will be decided when the embedding pipeline is implemented.

## 13. Future Indexes

Possible relational indexes:

```sql
CREATE INDEX idx_source_files_lecture_id
ON source_files(lecture_id);
```

```sql
CREATE INDEX idx_chunks_source_file_id
ON chunks(source_file_id);
```

The vector column will later require an appropriate pgvector index depending on the expected data volume and retrieval strategy.

The MVP should not introduce vector index complexity until retrieval has working baseline behaviour.

## 14. Future Schema Evolution

Possible future fields include:

### lectures

```text
user_id
course_name
updated_at
```

### source_files

```text
storage_key
mime_type
file_size
processing_error
updated_at
```

### chunks

```text
token_count
content_hash
embedding_model
created_at
```

These fields should only be introduced when a concrete requirement appears.

## 15. Design Principle

The schema follows this principle:

> Normalize when consistency and update integrity dominate.  
> Denormalize when a frequently used read path benefits from having related data available together.

For LectureBridge, citation metadata belongs to the retrieval hot path and source-derived metadata is effectively immutable.

Therefore, denormalising citation fields into `chunks` is a reasonable trade-off for the MVP.
