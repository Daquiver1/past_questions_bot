"""Conftest for s3 tests."""

import io
import sys
from pathlib import Path
from typing import Generator

import pytest
from fastapi import UploadFile
from moto import mock_aws as mock_s3

ROOT_DIR = Path(__file__).parent.parent.parent
sys.path.append(str(ROOT_DIR))
from src.core.config import S3_BUCKET_NAME
from src.models.past_questions import PastQuestionCreate


@pytest.fixture
def aws_credentials() -> dict[str, str]:
    """Mocked AWS Credentials for moto."""
    return {
        "aws_access_key_id": "testing",
        "aws_secret_access_key": "testing",
        "region_name": "us-east-1",
    }


@pytest.fixture
def new_past_question() -> PastQuestionCreate:
    """Return a PastQuestionCreate instance."""
    return PastQuestionCreate(
        course_code="104",
        course_name="Test",
        course_title="Test 104",
        lecturer_name="Test Test",
        past_question_url="http://example.com",
        semester="First",
        year="2022",
    )


@pytest.fixture
def s3_setup(aws_credentials: dict[str, str]) -> Generator[None, None, None]:
    """Setup s3 bucket for testing."""
    with mock_s3():
        import boto3

        s3 = boto3.client("s3", **aws_credentials)
        s3.create_bucket(Bucket=S3_BUCKET_NAME)
        yield


@pytest.fixture
def test_file() -> UploadFile:
    """Return a test file."""
    test_file_content = b"Test file content"
    return UploadFile(filename="test.txt", file=io.BytesIO(test_file_content))
