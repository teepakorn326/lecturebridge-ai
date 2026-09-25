from app.modules.ai.client import LLMClient
from app.modules.retrieval.domain import Chunk
from .domain import GlossaryTerm, TranslatedChunk
from .prompts import LANGUAGE_NAMES, TRANSLATION_SYSTEM_PROMPT,SUMMARY_SYSTEM_PROMPT


class UnsupportedLanguageError(Exception):
    pass


class TranslationService:
    def __init__(self, llm: LLMClient):
        self._llm = llm

    def translate_chunks(
        self,
        chunks: list[Chunk],
        target_language: str,
        glossary: list[GlossaryTerm],
    ) -> list[TranslatedChunk]:

        if target_language not in LANGUAGE_NAMES:
            raise UnsupportedLanguageError(
                f"Unsupported target language: {target_language}"
            )

        system = TRANSLATION_SYSTEM_PROMPT.format(
            language_name=LANGUAGE_NAMES[target_language],
            glossary_block=self._format_glossary(glossary),
        )

        results: list[TranslatedChunk] = []

        for chunk in chunks:
            translated = self._llm.complete(system=system, user=chunk.text)

            results.append(
                TranslatedChunk(
                    chunk_index=chunk.index,
                    source_text=chunk.text,
                    translated_text=translated,
                    target_language=target_language,
                    citations=chunk.citations,
                )
            )

        return results

    def _format_glossary(self, glossary: list[GlossaryTerm]) -> str:
        if not glossary:
            return "(no glossary provided)"

        return "\n".join(
            f'- "{term.term}" -> "{term.translation}"'
            for term in glossary
    )

class SummaryService:

    def __init__(
        self,
        llm: LLMClient,
    ):
        self._llm = llm

    def summarize(
        self,
        chunks: list[Chunk],
        target_language: str,
    ) -> str:

        if target_language not in LANGUAGE_NAMES:
            raise UnsupportedLanguageError(
                f"Unsupported target language: {target_language}"
            )

        system = SUMMARY_SYSTEM_PROMPT.format(
            language_name=LANGUAGE_NAMES[target_language],
        )

        user = self._build_context(chunks)

        return self._llm.complete(
            system=system,
            user=user,
        )

    def _build_context(
        self,
        chunks: list[Chunk],
    ) -> str:

        blocks: list[str] = []

        for chunk in chunks:

            labels = [
                citation.label()
                for citation in chunk.citations
            ]

            citation_block = ", ".join(
                f"[{label}]"
                for label in labels
            )

            blocks.append(
                f"{citation_block}\n{chunk.text}"
            )

        return "\n\n".join(blocks)