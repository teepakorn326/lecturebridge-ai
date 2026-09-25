from app.modules.ingestion.domain import CanonicalDocument, Segment
from .domain import Chunk, Citation


class ChunkingService:
    def __init__(
        self,
        max_chars: int = 1200,
        overlap_chars: int = 150,
    ):
        if overlap_chars >= max_chars:
            raise ValueError("overlap_chars must be smaller than max_chars")
        self.max_chars = max_chars
        self.overlap_chars = overlap_chars

    def _citation_from(
        self,
        document: CanonicalDocument,
        segment: Segment,
    ) -> Citation:
        return Citation(
            filename=document.filename,
            source_type=document.source_type,
            page_number=segment.page_number,
            slide_number=segment.slide_number,
            timestamp_start=segment.timestamp_start,
            timestamp_end=segment.timestamp_end,
        )

    def chunk_document(
        self,
        document: CanonicalDocument,
    ) -> list[Chunk]:

        chunks: list[Chunk] = []

        buffer_text: list[str] = []
        buffer_citations: list[Citation] = []
        buffer_len = 0

        def flush() -> None:
            """เท buffer ที่สะสมอยู่ออกเป็น 1 chunk"""
            nonlocal buffer_text, buffer_citations, buffer_len

            if not buffer_text:
                return

            chunks.append(
                Chunk(
                    text="\n".join(buffer_text),
                    citations=list(buffer_citations),
                    index=len(chunks),
                )
            )
            buffer_text = []
            buffer_citations = []
            buffer_len = 0

        for segment in document.segments:
            citation = self._citation_from(document, segment)

            if len(segment.text) > self.max_chars:
                flush()
                for piece in self._split_long_text(segment.text):
                    chunks.append(
                        Chunk(
                            text=piece,
                            citations=[citation],
                            index=len(chunks),
                        )
                    )
                continue

            if buffer_len + len(segment.text) > self.max_chars:
                flush()

            buffer_text.append(segment.text)
            buffer_citations.append(citation)
            buffer_len += len(segment.text)

        flush()

        return chunks

    def _split_long_text(
        self,
        text: str,
    ) -> list[str]:

        step = self.max_chars - self.overlap_chars

        return [
            text[start : start + self.max_chars] for start in range(0, len(text), step)
        ]
