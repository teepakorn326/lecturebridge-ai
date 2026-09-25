from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator

from .domain import LectureStatus, TargetLanguage


class CreateLectureRequest(BaseModel):
    title: str = Field(
        min_length=1,
        max_length=200,
    )

    target_language: TargetLanguage

    @field_validator("title")
    @classmethod
    def validate_title(cls, value: str) -> str:
        cleaned = value.strip()

        if not cleaned:
            raise ValueError("Title cannot be empty")

        return cleaned


class LectureResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    title: str
    target_language: TargetLanguage
    status: LectureStatus
    created_at: datetime
