from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.modules.lectures.router import router as lecture_router
from app.core.error import LectureNotFoundError

from app.modules.ingestion.router import (
    router as ingestion_router,
)


app = FastAPI(
    title="LectureBridge AI API",
    version="0.1.0",
)


app.include_router(
    lecture_router,
    prefix="/api/v1",
)


@app.get("/health")
def health_check():
    return {
        "status": "ok"
    }


@app.exception_handler(LectureNotFoundError)
async def lecture_not_found_handler(
    request: Request,
    exc: LectureNotFoundError,
):
    return JSONResponse(
        status_code=404,
        content={
            "detail": str(exc)
        },
    )

app.include_router(
    ingestion_router,
    prefix="/api/v1",
)