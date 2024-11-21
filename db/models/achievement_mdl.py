from sqlalchemy import Column, String, UUID
from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4
from db.database import Base


class Achievement(Base):
    __tablename__ = "achievement"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid4)
    title = Column(String)
    description = Column(String)
    badge = Column(String, default="default_badge.png")
    course_id = Column(UUID(as_uuid=True))
