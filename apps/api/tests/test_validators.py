import pytest

from app.modules.ingestion.validators import (
    MAX_FILE_SIZE,
    validate_file_size,
    validate_filename,
    UnsupportedFileTypeError,
    FileTooLargeError,
)


def test_validate_filename_accepts_supported_pdf():
    validate_filename("lecture.pdf")


def test_validate_filename_rejects_unsupported_file_type():
    with pytest.raises(UnsupportedFileTypeError):
        validate_filename("virus.exe")


def test_validate_file_size_accepts_small_file():
    validate_file_size(1024)


def test_validate_file_size_rejects_file_over_limit():
    with pytest.raises(FileTooLargeError):
        validate_file_size(MAX_FILE_SIZE + 1)
