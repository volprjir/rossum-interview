from pydantic import BaseModel


class XMLConversionBody(BaseModel):
    annotation_id: str
    queue_id: str

    class Config:
        extra = "forbid"
