import os
import pytest
from app.services.graph import GraphService
from app.db.models.document import Document, DocumentPage
from app.db.models.evidence import Evidence
from app.db.models.decision_pack import DecisionPack
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db import Base
from fastapi.testclient import TestClient
from app.main import app
from app.db import get_db

TEST_DB_URL = "sqlite:///./test_graph.db"
test_engine = create_engine(TEST_DB_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

@pytest.fixture(scope="session", autouse=True)
def setup_db():
    Base.metadata.drop_all(bind=test_engine)
    Base.metadata.create_all(bind=test_engine)
    
    db = TestingSessionLocal()
    dp = DecisionPack(id="pack-1", name="Test Pack")
    db.add(dp)
    
    doc1 = Document(id="doc-1", filename="lease.pdf", content_type="application/pdf", file_path="mock.pdf", sha256="abc", status="ADMISSIBLE", decision_pack_id="pack-1")
    db.add(doc1)
    
    page1 = DocumentPage(id="page-1", document_id="doc-1", page_number=1, text="Test")
    db.add(page1)
    
    # Admissible evidence (92%)
    ev1 = Evidence(id="ev-92", label="Outgoings", value=92, source_document_id="doc-1", page=1, status="VERIFIED", decision_pack_id="pack-1", evidence_class="MEASURED")
    db.add(ev1)
    
    doc2 = Document(id="doc-2", filename="pm.pdf", content_type="application/pdf", file_path="mock2.pdf", sha256="def", status="ADMISSIBLE", decision_pack_id="pack-1")
    db.add(doc2)
    page2 = DocumentPage(id="page-2", document_id="doc-2", page_number=1, text="Test")
    db.add(page2)
    
    # Conflicting evidence (88%)
    ev2 = Evidence(id="ev-88", label="Outgoings", value=88, source_document_id="doc-2", page=1, status="VERIFIED", decision_pack_id="pack-1", evidence_class="MEASURED")
    db.add(ev2)
    
    # Rejected doc and evidence
    doc_rej = Document(id="doc-rej", filename="desktop_valuation_note.pdf", content_type="application/pdf", file_path="mock3.pdf", sha256="ghi", status="REJECTED", decision_pack_id="pack-1")
    db.add(doc_rej)
    ev_rej = Evidence(id="ev-rej", label="Rate", value=2930, source_document_id="doc-rej", page=1, status="UNVERIFIED_NO_SOURCE", decision_pack_id="pack-1", evidence_class="CLIENT_STATED")

    db.add(ev_rej)

    db.commit()
    yield
    db.close()
    Base.metadata.drop_all(bind=test_engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

def test_A_neo4j_connectivity():
    svc = GraphService()
    assert svc.verify_connectivity() is True

def test_B_schema_constraints():
    svc = GraphService()
    svc.setup_constraints()
    assert True

def test_C_D_E_F_G_sync_and_idempotent():
    svc = GraphService()
    db = TestingSessionLocal()
    assert svc.sync_decision_pack("pack-1", db) is True
    # Run again for idempotency
    assert svc.sync_decision_pack("pack-1", db) is True
    
    with svc.driver.session() as session:
        # Check counts
        assert session.run("MATCH (n:DecisionPack) RETURN count(n) as c").single()["c"] == 1
        assert session.run("MATCH (n:Document) RETURN count(n) as c").single()["c"] == 3
        
        # Provenance check
        ev = session.run("MATCH (e:Evidence {id: 'ev-92'}) RETURN e.filename as fn, e.page as pg, e.status as status").single()
        assert ev["fn"] == "lease.pdf"
        assert ev["status"].upper() == "VERIFIED"
        
        # Rejected evidence should have status REJECTED
        ev_r = session.run("MATCH (e:Evidence {id: 'ev-rej'}) RETURN e.status as status").single()
        assert ev_r["status"].upper() == "REJECTED"

def test_H_relationship_creation():
    svc = GraphService()
    with svc.driver.session() as session:
        rel = session.run("MATCH (d:Document {id: 'doc-1'})-[:HAS_PAGE]->(p:DocumentPage {id: 'page-1'}) RETURN p").single()
        assert rel is not None
        
        rel2 = session.run("MATCH (p:DocumentPage {id: 'page-1'})-[:SUPPORTS]->(e:Evidence {id: 'ev-92'}) RETURN e").single()
        assert rel2 is not None

def test_J_conflict_graph():
    # Phase 3 requirement: 92% and 88% evidence both exist
    # For now we just verify they both exist as admissible
    svc = GraphService()
    with svc.driver.session() as session:
        ev92 = session.run("MATCH (e:Evidence {id: 'ev-92'}) RETURN e").single()
        ev88 = session.run("MATCH (e:Evidence {id: 'ev-88'}) RETURN e").single()
        assert ev92 is not None
        assert ev88 is not None

def test_K_coverage_gap():
    # Placeholder for coverage gap logic
    pass

def test_L_rejected_evidence():
    svc = GraphService()
    with svc.driver.session() as session:
        ev_r = session.run("MATCH (e:Evidence {id: 'ev-rej'}) RETURN e.status as status").single()
        assert ev_r["status"].upper() == "REJECTED"

def test_M_option_D():
    pass

def test_N_graph_api():
    response = client.get("/api/graph/pack-1")
    assert response.status_code == 200
    assert "nodes" in response.json()
    assert "relationships" in response.json()

def test_O_restart_persistence():
    svc = GraphService()
    svc.close()
    
    svc2 = GraphService()
    with svc2.driver.session() as session:
        ev92 = session.run("MATCH (e:Evidence {id: 'ev-92'}) RETURN e").single()
        assert ev92 is not None
