from typing import Protocol


class LLMClient(Protocol):
    def complete(self, *, system: str, user: str) -> str: ...


class LLMResponseFormatError(Exception):
    """โมเดลตอบมาไม่ตรง format ที่สัญญากันไว้"""