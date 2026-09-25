from dataclasses import dataclass

from app.modules.ingestion.domain import SourceType


@dataclass(slots=True, frozen=True)
class Citation:
    filename: str
    source_type: SourceType
    page_number: int | None = None
    slide_number: int | None = None
    timestamp_start: float | None = None
    timestamp_end: float | None = None
