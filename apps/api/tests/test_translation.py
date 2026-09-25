import pytest

from app.modules.ai.client import LLMResponseFormatError
from app.modules.ingestion.domain import SourceType
from app.modules.retrieval.domain import Chunk, Citation
from app.modules.translation.domain import GlossaryTerm
from app.modules.translation.glossary import GlossaryService
from app.modules.translation.service import (
    TranslationService,
    UnsupportedLanguageError,
)
from tests.fakes import FakeLLMClient

def make_chunk(text: str, index: int = 0) -> Chunk:
    citation = Citation(filename="lecture.pdf", source_type=SourceType.PDF, page_number=1)
    return Chunk(text=text, citations=[citation], index=index)


def test_translation_injects_glossary_and_language_into_prompt():
    fake = FakeLLMClient(responses=["กลไก attention คือ..."])
    service = TranslationService(llm=fake)

    glossary = [GlossaryTerm(term="attention mechanism", translation="กลไก attention")]

    results = service.translate_chunks([make_chunk("Attention is...")], "th", glossary)

    system_prompt = fake.calls[0]["system"]
    assert "Thai" in system_prompt                   
    assert "attention mechanism" in system_prompt    
    assert results[0].translated_text == "กลไก attention คือ..."
    assert results[0].citations[0].page_number == 1   

def test_unsupported_language_raises():
    fake = FakeLLMClient(
        responses=["this should never be used"]
    )

    service = TranslationService(
        llm=fake
    )

    chunks = [
        make_chunk(
            "Attention is...",
            index=0,
        )
    ]

    with pytest.raises(
        UnsupportedLanguageError
    ):
        service.translate_chunks(
            chunks=chunks,
            target_language="jp",
            glossary=[],
        )

    assert fake.calls == []


def test_one_llm_call_per_chunk():
    fake = FakeLLMClient(
        responses=[
            "คำแปล chunk 1",
            "คำแปล chunk 2",
            "คำแปล chunk 3",
        ]
    )

    service = TranslationService(
        llm=fake
    )

    chunks = [
        make_chunk(
            "First chunk",
            index=0,
        ),
        make_chunk(
            "Second chunk",
            index=1,
        ),
        make_chunk(
            "Third chunk",
            index=2,
        ),
    ]

    results = service.translate_chunks(
        chunks=chunks,
        target_language="th",
        glossary=[],
    )

    assert len(fake.calls) == 3
    assert len(results) == 3

    assert results[0].chunk_index == 0
    assert results[1].chunk_index == 1
    assert results[2].chunk_index == 2

def test_glossary_parse_rejects_malformed_json():
    fake = FakeLLMClient(
        responses=[]
    )

    service = GlossaryService(
        llm=fake
    )

    raw = (
        'Sure! Here is the JSON: '
        '[{"term": "attention mechanism", '
        '"translation": "กลไก attention"}]'
    )

    with pytest.raises(
        LLMResponseFormatError
    ):
        service._parse(raw)

def test_glossary_parse_valid_json():
    fake = FakeLLMClient(
        responses=[]
    )

    service = GlossaryService(
        llm=fake
    )

    raw = """
    [
        {
            "term": "attention mechanism",
            "translation": "กลไก attention"
        },
        {
            "term": "embedding",
            "translation": "embedding"
        }
    ]
    """

    result = service._parse(raw)

    assert len(result) == 2

    assert all(
        isinstance(term, GlossaryTerm)
        for term in result
    )

    assert (
        result[0].term
        == "attention mechanism"
    )

    assert (
        result[0].translation
        == "กลไก attention"
    )

    assert result[1].term == "embedding"
    assert (
        result[1].translation
        == "embedding"
    )