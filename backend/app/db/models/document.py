from sqlalchemy import Column, String, DateTime, func, Boolean, Integer, Text, ForeignKey
import uuid
from app.db import Base

def generate_uuid():
    return str(uuid.uuid4())

class Document(Base):
    __tablename__ = "documents"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    filename = Column(String(255), nullable=False)
    content_type = Column(String(100), nullable=False)
    file_path = Column(String(512), nullable=False)
    sha256 = Column(String(64), nullable=False, unique=True)
    status = Column(String(50), nullable=False, default="ADMISSIBLE")  # e.g., 'ADMISSIBLE' or 'REJECTED'
    uploaded_at = Column(DateTime(timezone=True), server_default=func.now())
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    decision_pack_id = Column(String(36), ForeignKey("decision_packs.id"), nullable=False)

class DocumentPage(Base):
    __tablename__ = "document_pages"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    document_id = Column(String(36), ForeignKey("documents.id"), nullable=False)
    page_number = Column(Integer, nullable=False)
    text = Column(Text, nullable=True)
    # page image path can be stored if needed
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
