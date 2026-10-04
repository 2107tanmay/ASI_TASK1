from sqlalchemy import Column, String, DateTime, func, Enum, Boolean, Integer, Numeric, ForeignKey, Text
import uuid
from enum import Enum as PyEnum
from app.db import Base

class EvidenceStatus(PyEnum):
    VERIFIED = "verified"
    UNVERIFIED_NO_SOURCE = "unverified_no_source"
    CONFLICT = "conflict"
    COVERAGE_GAP = "coverage_gap"
    REJECTED = "rejected"

class EvidenceClass(PyEnum):
    MEASURED = "measured"
    CLIENT_STATED = "client_stated"
    ESTIMATE = "estimate"

def generate_uuid():
    return str(uuid.uuid4())

class Evidence(Base):
    __tablename__ = "evidence"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    label = Column(String(255), nullable=False)
    value = Column(Numeric(20, 6), nullable=False)
    unit = Column(String(50))
    option_id = Column(String(36), ForeignKey("options.id"), nullable=True)
    source_document_id = Column(String(36), ForeignKey("documents.id"), nullable=True)
    page = Column(Integer, nullable=True)
    extract = Column(Text, nullable=True)
    evidence_class = Column(Enum(EvidenceClass), nullable=False)
    status = Column(Enum(EvidenceStatus), nullable=False)
    used_in_calculation = Column(Boolean, default=False)
    owner = Column(String(255), nullable=True)
    as_of_date = Column(DateTime, nullable=True)
    decision_pack_id = Column(String(36), ForeignKey("decision_packs.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
