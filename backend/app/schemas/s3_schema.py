from app.schemas.base_schema import CamelCaseModel

class ViewURLResponse(CamelCaseModel):
    get_url: str

class UploadURLResponse(CamelCaseModel):
    upload_url: str
    s3_key: str
    max_file_size: int

class S3Key(CamelCaseModel):
    s3_key: str