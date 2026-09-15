# LectureBridge AI — Product Requirements Document

## 1. Problem

International students often study university courses in a language that is not their first language.

They may understand general English, but they can still struggle with fast lectures, academic terminology, technical concepts, and large amounts of lecture material.

Existing translation tools usually translate text without understanding the full lecture context. They may also translate important technical terms incorrectly or inconsistently.

LectureBridge AI aims to help students understand lectures in their preferred language while preserving academic meaning and technical terminology.

## 2. Target User

### Primary User

International university students who study English-taught courses but prefer learning in Mandarin or Thai.

### Initial MVP Users

- Mandarin-speaking students
- Thai-speaking students

### Future Users

Students who want to study academic content in other languages.

## 3. User Journey

A student creates a lecture in LectureBridge AI.

The student uploads lecture materials such as:

- lecture slides
- PDF documents
- subtitle files
- text files

The student chooses a preferred language, such as Mandarin or Thai.

LectureBridge AI processes the uploaded materials and identifies the content of the lecture.

The student can then:

1. Read a translated version of the lecture content.
2. Generate structured lecture notes.
3. Ask questions about the lecture.
4. Review important concepts.
5. See the source of information used to generate an answer.

In a later version, students will also be able to use Live Translation while attending a lecture.

## 4. Functional Requirements

### FR-01 — Create Lecture

The user shall be able to create a lecture workspace.

A lecture can contain multiple learning materials.

### FR-02 — Multi-file Upload

The user shall be able to upload multiple files into the same lecture.

The MVP should support:

- PDF
- PPTX
- TXT
- VTT subtitle files

### FR-03 — Extract Lecture Content

The system shall extract text and metadata from uploaded lecture materials.

Where possible, the system should preserve information such as:

- page number
- slide number
- subtitle timestamp
- file name

### FR-04 — Language Selection

The user shall be able to select a target language.

The MVP shall support:

- Mandarin Chinese
- Thai

### FR-05 — Academic Translation

The system shall translate lecture content into the selected language.

Important technical terminology should remain consistent throughout the lecture.

Technical English terms may be preserved when translating them is not appropriate.

### FR-06 — Lecture Summary

The user shall be able to generate structured lecture notes.

The summary should include:

- lecture overview
- important concepts
- definitions
- examples
- important terminology
- key points for review

### FR-07 — Lecture Question and Answer

The user shall be able to ask questions about uploaded lecture materials.

The system should retrieve relevant lecture information before generating an answer.

### FR-08 — Source Citation

Answers generated from lecture materials should provide references to their source where possible.

For example:

- file name
- PDF page
- slide number
- subtitle timestamp

### FR-09 — Lecture Review

The user shall be able to review a lecture using AI-generated learning activities.

Possible activities include:

- concept explanation
- quiz questions
- flashcards
- concept comparison

### FR-10 — Live Translation

In a future version, the system shall receive lecture audio and display translated subtitles with low latency.

## 5. Non-functional Requirements

### NFR-01 — Translation Quality

Technical terminology should be translated consistently within the same lecture.

The system should avoid translating important technical terms incorrectly.

### NFR-02 — RAG Answer Quality

Answers about lecture content should be based on retrieved lecture materials.

When evidence cannot be found, the system should not pretend that the information exists in the lecture.

### NFR-03 — Source Traceability

Users should be able to identify where important information came from.

Generated answers should provide source references whenever possible.

### NFR-04 — Performance

Normal lecture questions should return a response within an acceptable interactive time.

Initial target:

P95 response time < 8 seconds for normal Q&A requests.

### NFR-05 — File Processing

File processing should run separately from normal user requests when processing takes a long time.

The UI should show processing status instead of blocking the user.

### NFR-06 — Reliability

If an AI model request fails, the system should handle the failure without losing the uploaded lecture.

Retry and fallback strategies may be added for recoverable AI failures.

### NFR-07 — Security

Uploaded lecture files must not be accessible by unauthorized users.

Secrets and API keys must not be stored in source code.

### NFR-08 — Observability

Important AI operations should be traceable.

The system should record information such as:

- request latency
- model used
- retrieval results
- errors
- token usage

### NFR-09 — Cost

The system should avoid sending unnecessary lecture content to the LLM.

Retrieval, chunking, caching, and smaller models may be used when appropriate.

## 6. MVP

The first MVP will focus on the core problem:

"Can AI help an international student understand uploaded academic lecture materials in Mandarin or Thai?"

The MVP will include:

- create a lecture
- upload multiple lecture files
- PDF support
- PPTX support
- TXT support
- VTT subtitle support
- extract lecture text
- English → Mandarin translation
- English → Thai translation
- academic terminology preservation
- structured lecture summary
- lecture Q&A using RAG
- source citations
- basic lecture review
- deployed web application

Live Translation is not required for the first MVP.

It will be developed after the document-based workflow is stable.

## 7. Out of Scope

The first MVP will not include:

- payment system
- native iOS or Android application
- teacher dashboard
- university LMS integration
- automatic Coursera account access
- automatic Echo360 account access
- automatic downloading of any protected video
- support for every language
- video hosting
- voice cloning
- production-scale live translation
- multi-agent architecture unless there is a clear requirement

## 8. Success Metrics

The initial engineering targets are:

### Translation

At least 90% of selected technical terminology test cases should remain consistent within the same lecture.

### Retrieval

At least 85% of evaluation questions should retrieve a relevant lecture chunk within the top retrieval results.

### Citation

At least 90% of answers that use lecture information should include a valid source reference.

### Reliability

At least 95% of supported test files should complete ingestion without unexpected application failure.

### Performance

P95 normal lecture Q&A response time should be below 8 seconds during MVP testing.

### Hallucination

When the requested information is not present in the lecture material, the system should explicitly state that the information could not be found instead of inventing an answer.
