from uuid import UUID

from fastapi import APIRouter, Depends, status

from app.dependencies import get_lecture_service

from .schemas import CreateLectureRequest, LectureResponse
from .service import LectureService


router = APIRouter(
    prefix="/lectures",
    tags=["lectures"],
)


@router.post(
    "",
    response_model=LectureResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_lecture(
    payload: CreateLectureRequest,
    service: LectureService = Depends(get_lecture_service),
):

    lecture = service.create_lecture(
        title=payload.title,
        target_language=payload.target_language,
    )

    return LectureResponse.model_validate(lecture)


@router.get(
    "/{lecture_id}",
    response_model=LectureResponse,
)
def get_lecture(
    lecture_id: UUID,
    service: LectureService = Depends(get_lecture_service),
):

    lecture = service.get_lecture(lecture_id)

    return LectureResponse.model_validate(lecture)
