from datetime import datetime, timezone
from uuid import UUID, uuid4

from app.core.error import LectureNotFoundError

from .domain import Lecture, LectureStatus, TargetLanguage
from .repository import LectureRepository


class LectureService:

    def __init__(self, repository: LectureRepository):
        self.repository = repository

    def create_lecture(
        self,
        title: str,
        target_language: TargetLanguage,
    ) -> Lecture:

        lecture = Lecture(
            id=uuid4(),
            title=title,
            target_language=target_language,
            status=LectureStatus.CREATED,
            created_at=datetime.now(timezone.utc),
        )

        return self.repository.add(lecture)

    def get_lecture(self, lecture_id: UUID) -> Lecture:

        lecture = self.repository.get_by_id(lecture_id)

        if lecture is None:
            raise LectureNotFoundError(lecture_id)

        return lecture