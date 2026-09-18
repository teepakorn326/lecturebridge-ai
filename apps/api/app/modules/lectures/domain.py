from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from uuid import UUID


class TargetLanguage(str, Enum):
    THAI = "th"
    MANDARIN = "zh-CN"


class LectureStatus(str, Enum):
    CREATED = "created"
    PROCESSING = "processing"
    READY = "ready"
    FAILED = "failed"


@dataclass(slots=True)
class Lecture:
    id: UUID
    title: str
    target_language: TargetLanguage
    status: LectureStatus
    created_at: datetime