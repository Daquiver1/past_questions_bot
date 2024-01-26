import pytest

from models.past_questions import PastQuestionCreate
from services.s3.s3 import delete_folder


@pytest.fixture(scope="module")
def setup_s3(mock_category: str):
    yield
    delete_folder(folder_name=mock_category)  # type: ignore


@pytest.fixture
def mock_tempfile() -> str:
    return "tests/s3/mock_file.txt"


@pytest.fixture(scope="module")
def mock_category() -> str:
    return "mock_category"


@pytest.fixture
def mock_file() -> PastQuestionCreate:
    return PastQuestionCreate(
        course_code="mock_code",
        course_name="mock_name",
        lecturer="mock_lecturer",
        past_question_url="mock_url",
        semester="mock_semester",
        year="mock_year",
    )
