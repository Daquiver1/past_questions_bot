import functools
import os

import boto3
from mypy_boto3_s3.client import S3Client

dotenv.load_dotenv()

ENV: str = os.environ.get("ENV", "DEV")

REGION_NAME: str = os.environ.get("REGION_NAME", "eu-west-1")

S3_BUCKET_NAME: str = os.environ.get("PROCESSED_DATA_BUCKET", "test-emile-dev")

URL: str = os.environ.get("URL")
USERNAME: str= os.environ.get("USER_NAME")
PASSWORD: str = os.environ.get("PASSWORD")
PORT = int(os.environ.get("PORT", "8443"))

TOKEN =os.environ.get("TOKEN")
DEVELOPER_CHAT_ID = os.environ.get("DEVELOPER_CHAT_ID")

@functools.cache
def s3_client() -> S3Client:
    return boto3.client(service_name="s3", region_name=REGION_NAME)


APPLICATIONS = ["xml_parser_service", "helpers", "s3_helper"]





