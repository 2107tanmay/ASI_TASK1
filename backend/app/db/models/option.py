from sqlalchemy import Column, String, DateTime, func, Boolean, Numeric, ForeignKey
import uuid
from app.db import Base

def generate_uuid():
    return str(uuid.uuid4())

class Option(Base):
    __tablename__ = "options"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    label = Column(String(50), nullable=False)  # e.g., "A", "B", "C", "D"
    description = Column(String(255), nullable=True)
    decision_pack_id = Column(String(36), ForeignKey("decision_packs.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    # Additional fields can be added (e.g., acquisition details)
