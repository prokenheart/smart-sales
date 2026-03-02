from app.schemas.base_schema import CamelCaseModel

class ViewUrlResponse(CamelCaseModel):
    get_url: str

class UploadUrlResponse(CamelCaseModel):
    upload_url: str
    s3_key: str
    max_file_size: int

class S3KeyParams(CamelCaseModel):
    s3_key: str