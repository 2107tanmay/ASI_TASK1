from sqlalchemy import Column, String, DateTime, func, Boolean, Enum, ForeignKey, Text
import uuid
from enum import Enum as PyEnum
from app.db import Base

def generate_uuid():
    return str(uuid.uuid4())

class ConflictStatus(PyEnum):
    UNRESOLVED = "unresolved"
    RESOLVED = "resolved"

class Conflict(Base):
    __tablename__ = "conflicts"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    evidence_a_id = Column(String(36), ForeignKey("evidence.id"), nullable=False)
    evidence_b_id = Column(String(36), ForeignKey("evidence.id"), nullable=False)
    description = Column(Text, nullable=True)
    status = Column(Enum(ConflictStatus), default=ConflictStatus.UNRESOLVED, nullable=False)
    selected_evidence_id = Column(String(36), ForeignKey("evidence.id"), nullable=True)
    resolved_by = Column(String(255), nullable=True)
    resolution_basis = Column(Text, nullable=True)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
