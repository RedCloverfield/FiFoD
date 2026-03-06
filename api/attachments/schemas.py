from pydantic import BaseModel, ConfigDict, Field


class BaseAttachmentDTO(BaseModel):
    device_id: str = Field(alias='deviceId')
    comment: str | None = None
    tags: list[str] | None = None


class CreateAttachmentDTO(BaseAttachmentDTO):
    device_id: str
    filenames: list[str]


class AttachmentDTO(BaseAttachmentDTO):
    filenames: list[str] = Field(alias='fileNames')

    model_config = ConfigDict(from_attributes=True)
