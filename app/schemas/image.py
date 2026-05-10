from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class ImageResponse(BaseModel):
    id: int
    entity_type: str
    entity_id: int
    image_url: str
    uploaded_at: datetime

    class Config:
        from_attributes = True
