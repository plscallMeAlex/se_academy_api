from sqlalchemy import Column, String, ForeignKey, DateTime, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from uuid import uuid4
from db.database import Base

class Token(Base):
    __tablename__ = "token"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=lambda: str(uuid4()))
    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id"))
    token = Column(String, index=True, unique=True)
    state= Column(Boolean)
    created_at = Column(DateTime)
    expired_at = Column(DateTime)
    updated_at = Column(DateTime)

    user = relationship("User", back_populates="tokens")
    
