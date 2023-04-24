import json
import logging
from collections.abc import Iterator
from typing import Dict, List, Tuple

from mypy_boto3_s3.client import S3Client

from past_question_bot.constant import s3_client

logger = logging.getLogger("s3_helper")


def get_data_from_s3(
    bucket: str, interaction_file: str, client: S3Client = s3_client()
) -> Iterator[bytes]:
    try:
        obj = client.get_object(
            Bucket=bucket,
            Key=interaction_file,
        )
        data = obj["Body"].read()
        yield data
    except client.exceptions.NoSuchBucket as err:
        logger.warning(
            "Bucket does not exits",
            extra={"error": json.dumps(err, default=str)},
            exc_info=True,
        )
    except client.exceptions.NoSuchKey as err:
        logger.warning(
            "Key does not exits",
            extra={"error": json.dumps(err, default=str)},
            exc_info=True,
        )


def split_s3_path(s3_path: str) -> Tuple[str, str]:
    path_parts = s3_path.replace("s3://", "").split("/")
    bucket = path_parts.pop(0)
    key = "/".join(path_parts)
    return bucket, key


def upload_to_s3(
    processed_data: List[Dict[str, str]],
    bucket: str,
    filename: str,
    client: S3Client = s3_client(),
) -> None:
    json_data = json.dumps(processed_data, indent=4)

    logger.info("Uploading Data to S3 Bucket")
    client.put_object(Bucket=bucket, Key=filename, Body=json_data)
    logger.info("Data Uploaded to s3 bucket")
