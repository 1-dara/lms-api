from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.database import Base


class Image(Base):
    __tablename__ = "images"

    id = Column(Integer, primary_key=True, index=True)
    entity_type = Column(String, nullable=False)  # "course", "lesson", "user"
    entity_id = Column(Integer, nullable=False)
    image_url = Column(String, nullable=False)
    uploaded_at = Column(DateTime(timezone=True),
                         default=lambda: datetime.now(timezone.utc))

    # No direct relationships because of polymorphic; we'll handle via queries
