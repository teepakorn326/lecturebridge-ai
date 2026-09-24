import shutil
from pathlib import Path
from tempfile import NamedTemporaryFile

from fastapi import UploadFile

from app.core.error import ValidationError
from .domain import SourceFile
from .validators import (
    FileTooLargeError,
    validate_filename,
    validate_file_size,
)


async def stage_upload(file: UploadFile) -> SourceFile:
    """UploadFile → ไฟล์จริงบนดิสก์ + ผ่านกฎครบแล้ว"""

    # ① guard: filename เป็น None ไหม
    if file.filename is None:
        raise ValidationError("Filename is required")

    # ② เช็คนามสกุล ← ทำ "ก่อน" เขียนดิสก์
    validate_filename(file.filename)

    # ③ ดึงนามสกุลออกมา lowercase
    suffix = Path(file.filename).suffix.lower()

    # ④ คัดลอกเนื้อไฟล์ลง tmp
    with NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        shutil.copyfileobj(file.file, tmp)
        temp_path = Path(tmp.name)

    # ⑤ เช็คขนาดไฟล์จริงบนดิสก์
    #    ถ้าไม่ผ่าน → ลบ temp_path ทิ้งก่อน แล้วค่อยปล่อย error ต่อ
    try:
        validate_file_size(temp_path.stat().st_size)
    except FileTooLargeError:
        temp_path.unlink(missing_ok=True)
        raise

    return SourceFile(path=temp_path, original_filename=file.filename)
