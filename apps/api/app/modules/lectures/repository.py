from typing import Protocol
from uuid import UUID

from .domain import Lecture


class LectureRepository(Protocol):
    def add(self, lecture: Lecture) -> Lecture: ...

    def get_by_id(self, lecture_id: UUID) -> Lecture | None: ...


class InMemoryLectureRepository:
    def __init__(self):
        self._lectures: dict[UUID, Lecture] = {}

    def add(self, lecture: Lecture) -> Lecture:
        self._lectures[lecture.id] = lecture
        return lecture

    def get_by_id(self, lecture_id: UUID) -> Lecture | None:
        return self._lectures.get(lecture_id)
