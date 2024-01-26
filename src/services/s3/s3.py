import os

import boto3
import dotenv
from botocore.exceptions import ClientError

from models.past_questions import PastQuestionCreate
from utils.uuid import generate_n_digit_uuid

dotenv.load_dotenv()
BUCKET = os.environ["BUCKET_NAME"]
REGION = os.environ["REGION"]
s3_client = boto3.client("s3")


def upload_file(
    *, file_path: str, course_category: str, past_question: PastQuestionCreate
) -> str:
    """Upload a file to s3 bucket, returns the uploaded file name."""
    try:
        uuid_ = generate_n_digit_uuid(6)
        key = f"{course_category}/{past_question.course_code}_{uuid_}.pdf"
        s3_client.upload_file(
            file_path,
            BUCKET,
            key,
            ExtraArgs={
                "ACL": "public-read",
                "Metadata": {**past_question.dict(exclude={"past_question_url"})},
            },
        )
        return key
    except ClientError as e:
        print(e)
        raise
    except Exception as e:
        print(e)
        raise


def generate_download_url(*, key: str) -> str:
    return f"https://{BUCKET}.s3.{REGION}.amazonaws.com/{key}"


def delete_file(*, file_path: str) -> str:
    """Delete a file from s3 bucket."""
    try:
        s3_client.delete_object(Bucket=BUCKET, Key=file_path)
        return file_path

    except ClientError as e:
        print(e)
        raise
    except Exception as e:
        print(e)
        raise


def delete_folder(*, folder_name: str) -> str:
    # List all objects in the folder
    response = s3_client.list_objects_v2(Bucket=BUCKET, Prefix=folder_name)
    objects = response.get("Contents", [])

    # Delete each object in the folder
    for obj in objects:
        s3_client.delete_object(Bucket=BUCKET, Key=obj["Key"])

    return folder_name
