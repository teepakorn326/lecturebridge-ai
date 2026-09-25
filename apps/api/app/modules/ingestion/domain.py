from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any


class SourceType(str, Enum):
    PDF = "pdf"
    PPTX = "pptx"
    TXT = "txt"
    VTT = "vtt"


@dataclass(slots=True)
class SourceFile:
    path: Path
    original_filename: str


@dataclass(slots=True)
class Segment:
    text: str

    page_number: int | None = None
    slide_number: int | None = None

    timestamp_start: float | None = None
    timestamp_end: float | None = None

    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class CanonicalDocument:
    filename: str
    source_type: SourceType
    segments: list[Segment]
