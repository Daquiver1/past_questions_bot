"""Test cases for the s3 functions."""

from typing import Generator

import pytest
from fastapi import UploadFile

from src.models.past_questions import PastQuestionCreate
from src.services.s3 import generate_download_url, upload_file_to_bucket


class TestS3Functions:
    """Test s3 functions."""

    @pytest.mark.asyncio
    async def test_upload_file_to_bucket(
        self,
        s3_setup: Generator,
        test_file: UploadFile,
        new_past_question: PastQuestionCreate,
    ) -> None:
        """Test uploading a file to the s3 bucket."""
        file_url = await upload_file_to_bucket(
            past_question_file=test_file, past_question=new_past_question
        )

        assert file_url.startswith("https://")
        assert "test" in file_url
        assert file_url.endswith(".pdf")

    def test_generate_download_url(
        self,
    ) -> None:
        """Test generating a download url."""
        file_url = generate_download_url(key="Test.pdf")

        assert file_url is not None
        assert file_url.startswith("https://")
        assert file_url.endswith("Test.pdf")
