from app.modules.lectures.repository import InMemoryLectureRepository
from app.modules.lectures.service import LectureService


lecture_repository = InMemoryLectureRepository()

lecture_service = LectureService(repository=lecture_repository)


def get_lecture_service() -> LectureService:
    return lecture_service
