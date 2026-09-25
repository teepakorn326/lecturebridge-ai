from dataclasses import dataclass

from app.modules.retrieval.domain import Citation


@dataclass(slots=True, frozen=True)
class GlossaryTerm:
    term: str         
    translation: str   


@dataclass(slots=True)
class TranslatedChunk:
    chunk_index: int
    source_text: str
    translated_text: str
    target_language: str
    citations: list[Citation]