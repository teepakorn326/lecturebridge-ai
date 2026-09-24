from pydantic import BaseModel


class SegmentResponse(BaseModel):
    text: str

    page_number: int | None = None
    slide_number: int | None = None

    timestamp_start: float | None = None
    timestamp_end: float | None = None


class ParsedDocumentResponse(BaseModel):
    filename: str
    source_type: str
    segment_count: int
    segments: list[SegmentResponse]