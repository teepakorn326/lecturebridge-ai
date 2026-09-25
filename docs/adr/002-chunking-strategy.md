# ADR-002: Use Fixed-Size Character Chunking with Overlap

## Status

Accepted

## Context

LectureBridge AI needs to split parsed lecture content into smaller chunks before the content can be embedded and retrieved by the RAG pipeline.

The ingestion layer already converts source files such as PDF, PPTX, TXT and VTT into a common `CanonicalDocument` representation containing source-aware `Segment` objects.

Each segment preserves source metadata such as:

- filename
- page number
- slide number
- timestamp start
- timestamp end

The chunking strategy must therefore satisfy several requirements:

- chunks must be small enough for efficient retrieval
- chunks must preserve enough neighbouring context
- source citation metadata must not be lost
- chunking behaviour should be deterministic and easy to test
- the implementation should not introduce unnecessary dependencies in the MVP
- the strategy should be replaceable later if retrieval evaluation shows that another approach performs better

## Decision

LectureBridge AI will initially use a fixed-size character-based chunking strategy with overlap.

The default configuration is:

```text
max_chars = 1200
overlap_chars = 150
```
