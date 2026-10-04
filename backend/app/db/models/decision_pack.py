from sqlalchemy import Column, String, DateTime, func, Boolean, Text
import uuid
from app.db import Base

def generate_uuid():
    return str(uuid.uuid4())

class DecisionPack(Base):
    __tablename__ = "decision_packs"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    name = Column(String(255), nullable=False, default="Decision Pack")
    deadline = Column(DateTime, nullable=True)
    policy_hurdle = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    blocked = Column(Boolean, default=True)
    block_reasons = Column(Text, nullable=True)
