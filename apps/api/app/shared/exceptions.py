class LectureNotFoundError(Exception):

    def __init__(self, lecture_id):
        self.lecture_id = lecture_id

        super().__init__(
            f"Lecture '{lecture_id}' was not found"
        )