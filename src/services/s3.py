"""S3 Service."""

import boto3
from botocore.exceptions import ClientError
from fastapi import UploadFile

from src.core.config import (
    S3_ACCESS_KEY_ID,
    S3_BUCKET_NAME,
    S3_REGION,
    S3_SECRET_ACCESS_KEY,
)
from src.models.past_questions import PastQuestionCreate
from src.utils.pasco_file_name import create_object_name

s3_client = boto3.client(
    "s3",
    region_name=S3_REGION,
    aws_access_key_id=S3_ACCESS_KEY_ID,
    aws_secret_access_key=S3_SECRET_ACCESS_KEY,
)


async def upload_file_to_bucket(
    *, past_question_file: UploadFile, past_question: PastQuestionCreate
) -> str:
    """Upload a file to s3 bucket, returns the uploaded file name."""
    try:
        object_name = create_object_name(past_question_file)
        s3_client.upload_fileobj(
            past_question_file.file,
            S3_BUCKET_NAME,
            "past_questions/" + object_name,
            ExtraArgs={
                "Metadata": {
                    **past_question.model_dump(exclude={"past_question_url", "updated_at"})
                },
            },
        )
        return f"https://{S3_BUCKET_NAME}.s3.{S3_REGION}.amazonaws.com/past_questions/{object_name}"
    except ClientError as e:
        print(e)
        raise
    except Exception as e:
        print(e)
        raise


def generate_download_url(*, key: str) -> str:
    """Generate a download url for a file in s3 bucket."""
    return f"https://{S3_BUCKET_NAME}/past_questions.s3.{S3_REGION}.amazonaws.com/{key}"
