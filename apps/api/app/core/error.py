# app/core/errors.py


class AppError(Exception):
    """Base ของ error ทุกตัวที่ "คาดไว้แล้ว" ในระบบ"""


class ValidationError(AppError):
    """input ของ user ไม่ผ่านกฎ"""


class NotFoundError(AppError):
    """ของที่ขอไม่มีอยู่"""


class LectureNotFoundError(NotFoundError):
    def __init__(self, lecture_id):
        self.lecture_id = lecture_id

        super().__init__(f"Lecture '{lecture_id}' was not found")
