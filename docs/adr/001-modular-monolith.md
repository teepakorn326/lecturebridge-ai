# ADR-001: Use a Modular Monolith for the MVP

## Status

Accepted

## Context

LectureBridge AI contains several different responsibilities, including:

- lecture management
- file ingestion
- translation
- summarisation
- retrieval
- question answering
- lecture review

These responsibilities have different business purposes.

However, the MVP currently has a small expected user base and does not require each component to scale or deploy independently.

Using microservices at this stage would increase system complexity without solving an existing scaling problem.

## Decision

LectureBridge AI will use a Modular Monolith architecture for the MVP.

The backend will run as one FastAPI application.

The application will still separate business logic into modules with clear responsibilities.

Conceptually:

```text
FastAPI Application

├── lectures
├── ingestion
├── translation
├── summarisation
├── retrieval
└── review
```
