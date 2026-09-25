from fastapi import (
    APIRouter,
    File,
    HTTPException,
    UploadFile,
)

from app.core.error import ValidationError

from .adapters import DocumentParsingError
from .service import IngestionService
from .staging import stage_upload
from .validators import (
    FileTooLargeError,
    UnsupportedFileTypeError,
)


router = APIRouter(
    prefix="/ingestion",
    tags=["ingestion"],
)


service = IngestionService()


@router.post("/parse")
async def parse_file(
    file: UploadFile = File(...),
):
    try:
        source = await stage_upload(file)

    except ValidationError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    except UnsupportedFileTypeError as exc:
        raise HTTPException(status_code=415, detail=str(exc)) from exc

    except FileTooLargeError as exc:
        raise HTTPException(status_code=413, detail=str(exc)) from exc

    try:
        document = service.ingest(source)

    except DocumentParsingError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc

    finally:
        source.path.unlink(missing_ok=True)

    return {
        "filename": document.filename,
        "source_type": document.source_type.value,
        "segment_count": len(document.segments),
        "segments": [
            {
                "text": segment.text,
                "page_number": segment.page_number,
                "slide_number": segment.slide_number,
                "timestamp_start": segment.timestamp_start,
                "timestamp_end": segment.timestamp_end,
            }
            for segment in document.segments
        ],
    }


@router.post("/parse-many")
async def parse_many(
    files: list[UploadFile] = File(...),
):
    results = []

    for file in files:
        try:
            source = await stage_upload(file)

        except (
            ValidationError,
            UnsupportedFileTypeError,
            FileTooLargeError,
        ) as exc:
            results.append(
                {
                    "filename": file.filename,
                    "status": "error",
                    "error": str(exc),
                }
            )
            continue

        try:
            document = service.ingest(source)

        except DocumentParsingError as exc:
            results.append(
                {
                    "filename": file.filename,
                    "status": "error",
                    "error": str(exc),
                }
            )
            continue

        finally:
            source.path.unlink(missing_ok=True)

        results.append(
            {
                "filename": document.filename,
                "source_type": document.source_type.value,
                "segment_count": len(document.segments),
                "status": "ok",
            }
        )

    return {
        "file_count": len(results),
        "files": results,
    }
