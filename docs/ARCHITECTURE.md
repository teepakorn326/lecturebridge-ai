# LectureBridge AI — Architecture

## System Goal

LectureBridge AI processes academic lecture materials and helps students understand them in Mandarin or Thai.

The architecture should support translation, summarisation, lecture Q&A, and lecture review while keeping the system simple enough for the MVP.

## High-Level Architecture

User
|
v
Web Application
|
v
Backend API
|
+--------------------+
| |
v v
Lecture Processing AI Processing
| |
v v
Storage AI Models
|
v
Lecture Data

## Main Components

### 1. Web Application

Responsibilities:

- create lectures
- upload files
- choose target language
- display translations
- display summaries
- ask lecture questions
- display source citations

### 2. Backend API

Responsibilities:

- receive frontend requests
- validate requests
- manage lectures
- manage uploaded files
- trigger lecture processing
- return results

### 3. Lecture Processing

Responsibilities:

- identify file type
- extract content
- clean extracted text
- preserve useful metadata
- convert different file formats into a common internal format

### 4. AI Processing

Responsibilities:

- translation
- terminology handling
- summarisation
- embedding generation
- information retrieval
- question answering
- lecture review generation

### 5. Storage

Responsibilities:

- store lecture information
- store file metadata
- store processing status
- store extracted lecture content
- store generated results

## Initial Data Flow

User uploads lecture files
|
v
Backend API
|
v
Lecture Processing
|
v
Normalised Lecture Content
|
+-------------------+
| |
v v
Translation Knowledge Index
| |
v v
Summary Retrieval
|
v
Q&A / Review

## Architecture Principles

1. Start simple.

2. Do not introduce microservices unless scaling or system boundaries require them.

3. Keep file parsing separate from AI business logic.

4. Convert different source formats into a common internal representation.

5. Use deterministic workflows when the required processing steps are already known.

6. Use agentic workflows only when dynamic decision-making is required.

7. AI outputs must be observable and measurable.

8. Source traceability should be preserved throughout the processing pipeline.
