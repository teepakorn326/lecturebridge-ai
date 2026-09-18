# LectureBridge AI — System Architecture

## 1. System Goal

LectureBridge AI helps international students understand academic lecture materials in Mandarin or Thai.

The system allows users to upload lecture materials, translate academic content, generate lecture summaries, ask questions based on lecture content, and review important concepts.

The MVP focuses on uploaded lecture materials before adding real-time live translation.

## 2. Architecture Style

The MVP uses a Modular Monolith architecture.

The backend is deployed as one FastAPI application, but the source code is separated into clear modules such as:

- lecture management
- ingestion
- translation
- summarisation
- retrieval
- review

This architecture keeps deployment simple while maintaining clear boundaries between responsibilities.

Microservices are not required for the MVP because the system does not yet have independent scaling or deployment requirements.

## 3. System Boundary

LectureBridge AI controls:

- Web Application
- Backend API
- Lecture Processing
- AI Processing
- Retrieval
- Database
- File metadata
- Application logic

External dependencies include:

- LLM Provider
- Embedding Model Provider
- Object Storage Provider in production
- LangSmith for AI observability

## 4. High-Level Architecture

```text
                         User
                          |
                          v
                 +----------------+
                 |    Next.js     |
                 |    Web App     |
                 +--------+-------+
                          |
                        HTTPS
                          |
                          v
                 +----------------+
                 |    FastAPI     |
                 |  Backend API   |
                 +--------+-------+
                          |
             +------------+-------------+
             |                          |
             v                          v
    +------------------+       +------------------+
    | Lecture          |       | AI Processing    |
    | Processing       |       |                  |
    +--------+---------+       +--------+---------+
             |                          |
             |                 +--------+--------+
             |                 |        |        |
             v                 v        v        v
      Canonical          Translation Summary Retrieval
      Document                                 |
             |                                  |
             |                                  v
             +---------------------------> PostgreSQL
                                               +
                                            pgvector

Original Files
      |
      v
Object Storage

External AI Services:
- LLM Provider
- Embedding Provider

Observability:
- LangSmith
```
