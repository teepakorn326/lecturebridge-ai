from app.core.config import settings
from app.modules.ai.openai_client import OpenAILLMClient
from app.modules.ingestion.domain import SourceType
from app.modules.retrieval.domain import Chunk, Citation
from app.modules.translation.service import TranslationService
from app.modules.translation.glossary import GlossaryService


def make_chunk(
    text: str,
    index: int,
    *,
    page_number: int,
) -> Chunk:
    citation = Citation(
        filename="lecture.pdf",
        source_type=SourceType.PDF,
        page_number=page_number,
    )

    return Chunk(
        text=text,
        citations=[citation],
        index=index,
    )


def reveal_secret(value):
    """Support both plain strings and pydantic SecretStr."""
    if hasattr(value, "get_secret_value"):
        return value.get_secret_value()

    return value


def main() -> None:
    target_language = "th"

    chunks = [
        make_chunk(
            (
                "Gradient descent is an optimisation algorithm used to "
                "minimise a loss function by updating model parameters "
                "in the direction of the negative gradient."
            ),
            index=0,
            page_number=3,
        ),
        make_chunk(
            (
                "The learning rate controls the size of each update step. "
                "A learning rate that is too large may overshoot the minimum, "
                "while a very small learning rate can make training slow."
            ),
            index=1,
            page_number=4,
        ),
        make_chunk(
            (
                "In neural networks, backpropagation computes gradients "
                "that are then used by an optimiser to update the weights."
            ),
            index=2,
            page_number=5,
        ),
    ]

    api_key = reveal_secret(settings.openai_api_key)

    llm = OpenAILLMClient(
        api_key=api_key,
        model=settings.llm_model,
    )

    glossary_service = GlossaryService(llm=llm)
    translation_service = TranslationService(llm=llm)

    print("\n=== 1. Extract glossary ===")

    glossary = glossary_service.extract(
        chunks=chunks,
        target_language=target_language,
    )

    if not glossary:
        print("(no glossary terms returned)")
    else:
        for term in glossary:
            print(f'- "{term.term}" -> "{term.translation}"')

    print("\n=== 2. Translate chunks ===")

    translated_chunks = translation_service.translate_chunks(
        chunks=chunks,
        target_language=target_language,
        glossary=glossary,
    )

    for item in translated_chunks:
        print(f"\n--- Chunk {item.chunk_index} ---")

        if item.citations:
            labels = ", ".join(
                citation.label()
                for citation in item.citations
            )
            print(f"Source: {labels}")

        print("\nOriginal:")
        print(item.source_text)

        print("\nTranslated:")
        print(item.translated_text)

    print("\n=== Done ===")
    print(
        f"Translated {len(translated_chunks)} chunks "
        f"using {len(glossary)} glossary terms."
    )


if __name__ == "__main__":
    main()
