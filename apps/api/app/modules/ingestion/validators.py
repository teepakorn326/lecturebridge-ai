from pathlib import Path


ALLOWED_EXTENSIONS = {
    ".txt",
    ".pdf",
    ".pptx",
    ".vtt",
}


MAX_FILE_SIZE = (
    50 * 1024 * 1024
)


class UnsupportedFileTypeError(Exception):
    pass


class FileTooLargeError(Exception):
    pass


def validate_filename(
    filename: str,
) -> None:

    extension = Path(
        filename
    ).suffix.lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise UnsupportedFileTypeError(
            f"Unsupported file type: {extension}"
        )


def validate_file_size(
    file_size: int,
) -> None:

    if file_size > MAX_FILE_SIZE:
        raise FileTooLargeError(
            "File exceeds the 50 MB limit"
        )

