import boto3
import os
from typing import Tuple
import uuid

BUCKET_NAME = os.getenv("AWS_BUCKET_NAME")
AWS_REGION = os.getenv("AWS_REGION", "ap-southeast-2")

_s3_client = None


def get_s3_client():
    global _s3_client
    if _s3_client is None:
        _s3_client = boto3.client(
            "s3",
            region_name=AWS_REGION,
        )
    return _s3_client


ALLOWED_CONTENT_TYPES = {
    "image/png": ".png",
    "image/jpeg": ".jpg",
    "application/pdf": ".pdf",
}


def generate_presigned_upload_url(
    content_type: str,
    expires_in: int = 300,
) -> Tuple[str, str]:

    if content_type not in ALLOWED_CONTENT_TYPES:
        raise ValueError("Unsupported file type")

    ext = ALLOWED_CONTENT_TYPES[content_type]
    filename = f"{uuid.uuid4().hex}{ext}"
    key = f"uploads/{filename}"

    s3 = get_s3_client()
    upload_url = s3.generate_presigned_url(
        ClientMethod="put_object",
        Params={
            "Bucket": BUCKET_NAME,
            "Key": key,
            "ContentType": content_type,
        },
        ExpiresIn=expires_in,
    )

    return upload_url, key

def generate_presigned_get_url(
    key: str,
    expires_in: int = 300,
) -> str:
    s3 = get_s3_client()
    get_url = s3.generate_presigned_url(
        ClientMethod="get_object",
        Params={
            "Bucket": BUCKET_NAME,
            "Key": key,
        },
        ExpiresIn=expires_in,
    )
    return get_url

def delete_file_from_s3(key: str):
    s3 = get_s3_client()
    s3.delete_object(
        Bucket=BUCKET_NAME,
        Key=key,
    )