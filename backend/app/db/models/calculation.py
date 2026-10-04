from sqlalchemy import Column, String, DateTime, func, Boolean, Numeric, ForeignKey, Text, JSON
import uuid
from app.db import Base

def generate_uuid():
    return str(uuid.uuid4())

class CalculationRun(Base):
    __tablename__ = "calculation_runs"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    option_id = Column(String(36), ForeignKey("options.id"), nullable=False)
    metric = Column(String(50), nullable=False)  # e.g., "NOI", "IRR", "YIELD"
    value = Column(Numeric(20, 6), nullable=True) # Modified to nullable
    unit = Column(String(20), nullable=True)
    calculation_version = Column(String(20), nullable=False)
    input_hash = Column(String(64), nullable=False)
    evidence_ids = Column(Text, nullable=True)  # comma-separated list of evidence UUIDs
    
    # New required fields
    inputs = Column(JSON, nullable=True)
    status = Column(String(50), nullable=True)
    reason = Column(String(255), nullable=True)
    missing_evidence = Column(JSON, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    completed_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)
