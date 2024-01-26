import validators

from models.past_questions import PastQuestionCreate
from services.s3.s3 import delete_file, generate_download_url, upload_file


def test_upload_file(
    setup_s3,
    mock_tempfile: str,
    mock_category: str,
    mock_file: PastQuestionCreate,
) -> None:
    result = upload_file(
        file_path=mock_tempfile,
        course_category=mock_category,
        past_question=mock_file,
    )
    assert result is not None
    assert result.endswith(".pdf")
    assert mock_category in result
    assert str(mock_file.course_code) in result


def test_generate_download_url(
    setup_s3,
    mock_tempfile: str,
    mock_category: str,
    mock_file: PastQuestionCreate,
) -> None:
    created_past_question_name = upload_file(
        file_path=mock_tempfile,
        course_category=mock_category,
        past_question=mock_file,
    )

    result = generate_download_url(key=created_past_question_name)

    assert result is not None
    assert is_valid_url(result)
    assert result.endswith(".pdf")


def test_delete_file(
    setup_s3,
    mock_tempfile: str,
    mock_category: str,
    mock_file: PastQuestionCreate,
) -> None:
    created_past_question_path = upload_file(
        file_path=mock_tempfile,
        course_category=mock_category,
        past_question=mock_file,
    )
    result = delete_file(file_path=created_past_question_path)

    assert result == created_past_question_path


def is_valid_url(url: str) -> bool:
    return validators.url(url)  # type: ignore
