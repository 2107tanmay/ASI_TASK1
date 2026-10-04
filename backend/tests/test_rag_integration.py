import pytest
import numpy as np
import sys
import types
from unittest.mock import patch

class MockSentenceTransformer:
    def __init__(self, *args, **kwargs):
        pass
    def encode(self, texts, convert_to_numpy=True):
        if isinstance(texts, str):
            return np.zeros(384, dtype=np.float32)
        return np.zeros((len(texts), 384), dtype=np.float32)

# Apply a clean patch instead of breaking sys.modules
import sentence_transformers
sentence_transformers.SentenceTransformer = MockSentenceTransformer

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db import Base
from app.db.models.document import Document, DocumentPage
from app.db.models.evidence import Evidence, EvidenceStatus, EvidenceClass
from app.db.models.calculation import CalculationRun
from app.db.models.option import Option
from app.db.models.decision_pack import DecisionPack
from app.services.rag import RagOrchestrator
from app.services.graph import GraphService
from app.vector.faiss_index import VectorStore

test_engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

@pytest.fixture(scope="module", autouse=True)
def setup_db():
    Base.metadata.create_all(bind=test_engine)
    db = TestingSessionLocal()
    
    dp = DecisionPack(id="dp1", name="Test DP")
    db.add(dp)
    
    opt_a = Option(id="optA", decision_pack_id="dp1", label="Option A")
    opt_b = Option(id="optB", decision_pack_id="dp1", label="Option B")
    opt_d = Option(id="optD", decision_pack_id="dp1", label="Option D")
    db.add_all([opt_a, opt_b, opt_d])
    
    doc1 = Document(id="doc1", decision_pack_id="dp1", filename="verified.pdf", status="ADMISSIBLE", content_type="application/pdf", file_path="/fake", sha256="fakehash")
    db.add(doc1)
    
    ev1 = Evidence(id="ev1", label="Option A NOI", value=657640, option_id="optA", source_document_id="doc1", page=1, evidence_class=EvidenceClass.MEASURED, status=EvidenceStatus.VERIFIED, decision_pack_id="dp1")
    ev2 = Evidence(id="ev2", label="Option B NOI", value=779780, option_id="optB", source_document_id="doc1", page=2, evidence_class=EvidenceClass.MEASURED, status=EvidenceStatus.VERIFIED, decision_pack_id="dp1")
    ev3 = Evidence(id="ev3", label="Option B Cost", value=500000, option_id="optB", source_document_id="doc1", page=3, evidence_class=EvidenceClass.ESTIMATE, status=EvidenceStatus.COVERAGE_GAP, decision_pack_id="dp1")
    ev4 = Evidence(id="ev4", label="Recovery Rate", value=92, option_id="optB", source_document_id="doc1", page=4, evidence_class=EvidenceClass.MEASURED, status=EvidenceStatus.CONFLICT, decision_pack_id="dp1")
    ev5 = Evidence(id="ev5", label="Recovery Rate", value=88, option_id="optB", source_document_id="doc1", page=5, evidence_class=EvidenceClass.MEASURED, status=EvidenceStatus.CONFLICT, decision_pack_id="dp1")
    ev6 = Evidence(id="ev6", label="Construction Cost / sqm", value=2930, option_id="optB", source_document_id="doc1", page=6, evidence_class=EvidenceClass.ESTIMATE, status=EvidenceStatus.UNVERIFIED_NO_SOURCE, decision_pack_id="dp1")
    ev7 = Evidence(id="ev7", label="Option D Rezoning M12", value=0, option_id="optD", source_document_id="doc1", page=7, evidence_class=EvidenceClass.ESTIMATE, status=EvidenceStatus.COVERAGE_GAP, decision_pack_id="dp1")
    
    db.add_all([ev1, ev2, ev3, ev4, ev5, ev6, ev7])
    
    calc1 = CalculationRun(id="calc1", option_id="optB", metric="IRR", value=5.80, calculation_version="1.0", input_hash="hash")
    db.add(calc1)
    
    db.commit()
    db.close()
    yield

@pytest.fixture
def db_session():
    db = TestingSessionLocal()
    yield db
    db.close()

@pytest.fixture
def rag(db_session):
    with patch("app.vector.faiss_index.SentenceTransformer", MockSentenceTransformer):
        faiss = VectorStore()
        neo4j = GraphService()
        return RagOrchestrator(db_session, faiss, neo4j)

def test_option_a_noi_retrieval(rag):
    resp = rag.query("What is the NOI for Option A?")
    assert len(resp.citations) == 1
    assert resp.citations[0].evidence_id == "ev1"
    assert resp.citations[0].status == "verified"
    assert resp.grounding_valid is True

def test_option_b_noi_retrieval(rag):
    resp = rag.query("What is the NOI for Option B?")
    assert any(c.evidence_id == "ev2" for c in resp.citations)

def test_option_b_coverage_gap(rag):
    resp = rag.query("What is Option B Cost?")
    assert any(c.status == "coverage_gap" for c in resp.citations)

def test_recovery_conflict(rag):
    resp = rag.query("What is the recovery rate? Is it 92% or 88%?")
    statuses = [c.status for c in resp.citations]
    assert "conflict" in statuses

def test_unsupported_figure(rag):
    resp = rag.query("Is the cost $2,930/sqm?")
    ev6_citations = [c for c in resp.citations if c.evidence_id == "ev6"]
    assert len(ev6_citations) == 0

def test_option_d_rezoning_gap(rag):
    resp = rag.query("What is the status of Option D rezoning M12?")
    assert any(c.evidence_id == "ev7" and c.status == "coverage_gap" for c in resp.citations)

def test_irr_discrepancy(rag):
    resp = rag.query("Why is Option B calculated IRR 5.80% when the reference document says 6.63%?")
    assert "5.80%" in resp.answer
    assert "6.63%" in resp.answer
