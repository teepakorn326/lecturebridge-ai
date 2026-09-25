import pytest

from app.modules.ingestion.domain import (
    CanonicalDocument,
    Segment,
    SourceType,
)
from app.modules.retrieval.chunker import ChunkingService


def make_doc(segments):
    return CanonicalDocument(
        filename="lecture.pdf",
        source_type=SourceType.PDF,
        segments=segments,
    )


def test_small_segments_are_merged_and_keep_all_citations():
    doc = make_doc([
        Segment(text="Intro to attention.", page_number=1),
        Segment(text="Query, key, value.", page_number=2),
    ])

    chunks = ChunkingService(max_chars=1200).chunk_document(doc)

    assert len(chunks) == 1                       
    citations = chunks[0].citations
    assert [c.page_number for c in citations] == [1, 2]  

def test_long_segment_is_split_with_overlap():
    service = ChunkingService(
        max_chars=1200,
        overlap_chars=150,
    )

    text = "".join(
        str(i % 10)
        for i in range(3000)
    )

    document = CanonicalDocument(
        filename="lecture.pdf",
        source_type=SourceType.PDF,
        segments=[
            Segment(
                text=text,
                page_number=3,
            )
        ],
    )

    chunks = service.chunk_document(document)

    assert len(chunks) > 1

    assert (
        chunks[0].text[-150:]
        == chunks[1].text[:150]
    )

    assert all(
        len(chunk.citations) == 1
        for chunk in chunks
    )

    assert all(
        chunk.citations[0].filename
        == "lecture.pdf"
        for chunk in chunks
    )

    assert all(
        chunk.citations[0].page_number == 3
        for chunk in chunks
    )


def test_no_chunk_exceeds_max_chars():
    service = ChunkingService(
        max_chars=1200,
        overlap_chars=150,
    )

    document = CanonicalDocument(
        filename="lecture.pdf",
        source_type=SourceType.PDF,
        segments=[
            Segment(
                text="a" * 300,
                page_number=1,
            ),
            Segment(
                text="b" * 400,
                page_number=1,
            ),
            Segment(
                text="c" * 3000,
                page_number=2,
            ),
            Segment(
                text="d" * 200,
                page_number=3,
            ),
            Segment(
                text="e" * 500,
                page_number=3,
            ),
        ],
    )

    chunks = service.chunk_document(document)

    assert all(
        len(chunk.text)
        <= 1200 + max(
            0,
            len(chunk.citations) - 1,
        )
        for chunk in chunks
    )


def test_empty_document_returns_no_chunks():
    service = ChunkingService()

    document = CanonicalDocument(
        filename="empty.txt",
        source_type=SourceType.TXT,
        segments=[],
    )

    chunks = service.chunk_document(document)

    assert chunks == []


def test_invalid_overlap_raises():
    with pytest.raises(ValueError):
        ChunkingService(
            max_chars=100,
            overlap_chars=100,
        )