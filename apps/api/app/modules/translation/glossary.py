import json

from app.modules.ai.client import LLMClient, LLMResponseFormatError
from app.modules.retrieval.domain import Chunk
from .domain import GlossaryTerm
from .prompts import GLOSSARY_SYSTEM_PROMPT, LANGUAGE_NAMES


class GlossaryService:
    def __init__(self, llm: LLMClient, max_sample_chars: int = 6000):
        self._llm = llm
        self._max_sample_chars = max_sample_chars

    def extract(
        self,
        chunks: list[Chunk],
        target_language: str,
    ) -> list[GlossaryTerm]:

        sample = self._sample_text(chunks)          # ไม่ส่งทั้ง lecture! คุม cost

        raw = self._llm.complete(
            system=GLOSSARY_SYSTEM_PROMPT.format(
                language_name=LANGUAGE_NAMES[target_language]
            ),
            user=sample,
        )

        return self._parse(raw)

    def _sample_text(self, chunks: list[Chunk]) -> str:
        pieces: list[str] = []
        total = 0
        for chunk in chunks:
            if total + len(chunk.text) > self._max_sample_chars:
                break
            pieces.append(chunk.text)
            total += len(chunk.text)
        return "\n".join(pieces)

    def _parse(self, raw: str) -> list[GlossaryTerm]:

        try:
            data = json.loads(raw)
        except json.JSONDecodeError as exc:
            raise LLMResponseFormatError(
                "LLM response is not valid JSON"
            ) from exc

        if not isinstance(data, list):
            raise LLMResponseFormatError(
                "LLM response must be a JSON list"
            )

        results: list[GlossaryTerm] = []

        for item in data:
            if not isinstance(item, dict):
                raise LLMResponseFormatError(
                    "Each glossary item must be an object"
                )

            if "term" not in item or "translation" not in item:
                raise LLMResponseFormatError(
                    'Each glossary item must contain '
                    '"term" and "translation"'
                )

            if not isinstance(item["term"], str):
                raise LLMResponseFormatError(
                    '"term" must be a string'
                )

            if not isinstance(item["translation"], str):
                raise LLMResponseFormatError(
                    '"translation" must be a string'
                )

            results.append(
                GlossaryTerm(
                    term=item["term"],
                    translation=item["translation"],
                )
            )

        return results