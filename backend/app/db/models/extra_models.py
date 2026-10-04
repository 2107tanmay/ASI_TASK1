from sqlalchemy import Column, String, DateTime, func, Boolean, Numeric, ForeignKey, Text, Enum
import uuid
from app.db import Base

def generate_uuid():
    return str(uuid.uuid4())

class OptionMetric(Base):
    __tablename__ = "option_metrics"
    id = Column(String(36), primary_key=True, default=generate_uuid)
    option_id = Column(String(36), ForeignKey("options.id"), nullable=False)
    metric_name = Column(String(255), nullable=False)
    metric_value = Column(Numeric(20, 6), nullable=True)

class Assumption(Base):
    __tablename__ = "assumptions"
    id = Column(String(36), primary_key=True, default=generate_uuid)
    option_id = Column(String(36), ForeignKey("options.id"), nullable=True)
    name = Column(String(255), nullable=False)
    value = Column(Numeric(20, 6), nullable=False)

class CalculationInput(Base):
    __tablename__ = "calculation_inputs"
    id = Column(String(36), primary_key=True, default=generate_uuid)
    run_id = Column(String(36), ForeignKey("calculation_runs.id"), nullable=False)
    input_name = Column(String(255), nullable=False)
    input_value = Column(Numeric(20, 6), nullable=False)

class SensitivityRun(Base):
    __tablename__ = "sensitivity_runs"
    id = Column(String(36), primary_key=True, default=generate_uuid)
    option_id = Column(String(36), ForeignKey("options.id"), nullable=False)
    exit_cap = Column(Numeric(20, 6), nullable=False)
    rent_growth = Column(Numeric(20, 6), nullable=False)
    irr_result = Column(Numeric(20, 6), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

class AuditEvent(Base):
    __tablename__ = "audit_events"
    id = Column(String(36), primary_key=True, default=generate_uuid)
    event_type = Column(String(255), nullable=False)
    details = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

class DecisionRecord(Base):
    __tablename__ = "decision_records"
    id = Column(String(36), primary_key=True, default=generate_uuid)
    decision_pack_id = Column(String(36), ForeignKey("decision_packs.id"), nullable=False)
    status = Column(String(50), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

class DecisionReview(Base):
    __tablename__ = "decision_reviews"
    id = Column(String(36), primary_key=True, default=generate_uuid)
    record_id = Column(String(36), ForeignKey("decision_records.id"), nullable=False)
    reviewer = Column(String(255), nullable=False)
    comments = Column(Text, nullable=True)

class Issue(Base):
    __tablename__ = "issues"
    id = Column(String(36), primary_key=True, default=generate_uuid)
    option_id = Column(String(36), ForeignKey("options.id"), nullable=False)
    description = Column(Text, nullable=False)

class TestCase(Base):
    __tablename__ = "test_cases"
    id = Column(String(36), primary_key=True, default=generate_uuid)
    name = Column(String(255), nullable=False)
    status = Column(String(50), nullable=False)

class TestEvidence(Base):
    __tablename__ = "test_evidence"
    id = Column(String(36), primary_key=True, default=generate_uuid)
    test_case_id = Column(String(36), ForeignKey("test_cases.id"), nullable=False)
    evidence_id = Column(String(36), ForeignKey("evidence.id"), nullable=False)

class ChatSession(Base):
    __tablename__ = "chat_sessions"
    id = Column(String(36), primary_key=True, default=generate_uuid)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

class ChatMessage(Base):
    __tablename__ = "chat_messages"
    id = Column(String(36), primary_key=True, default=generate_uuid)
    session_id = Column(String(36), ForeignKey("chat_sessions.id"), nullable=False)
    role = Column(String(50), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

class ChatCitation(Base):
    __tablename__ = "chat_citations"
    id = Column(String(36), primary_key=True, default=generate_uuid)
    message_id = Column(String(36), ForeignKey("chat_messages.id"), nullable=False)
    evidence_id = Column(String(36), ForeignKey("evidence.id"), nullable=False)
