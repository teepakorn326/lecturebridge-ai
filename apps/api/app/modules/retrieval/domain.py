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

    def label(self) -> str:
        if self.page_number is not None:
            return f"{self.filename}, page {self.page_number}"

        if self.slide_number is not None:
            return f"{self.filename}, slide {self.slide_number}"

        if self.timestamp_start is not None:
            minutes, seconds = divmod(
                int(self.timestamp_start),
                60,
            )

            return (
                f"{self.filename}, "
                f"{minutes:02d}:{seconds:02d}"
            )

        return self.filename
    
@dataclass(slots=True)
class Chunk:
    text: str
    citations: list[Citation]
    index: int