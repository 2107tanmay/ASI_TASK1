import os
import logging
from neo4j import GraphDatabase, exceptions
from app.core.config import settings

# In case we need to fetch from MySQL during sync
from app.db.models.document import Document, DocumentPage
from app.db.models.evidence import Evidence
from app.db.models.decision_pack import DecisionPack

logger = logging.getLogger(__name__)

class GraphService:
    def __init__(self):
        uri = os.getenv("NEO4J_URI", settings.NEO4J_URI)
        user = os.getenv("NEO4J_USER", settings.NEO4J_USER)
        password = os.getenv("NEO4J_PASSWORD", settings.NEO4J_PASSWORD)
        try:
            self.driver = GraphDatabase.driver(uri, auth=(user, password))
        except Exception as e:
            logger.error(f"Failed to initialize Neo4j driver: {e}")
            self.driver = None

    def verify_connectivity(self):
        if not self.driver:
            return False
        try:
            self.driver.verify_connectivity()
            return True
        except Exception:
            return False

    def close(self):
        if self.driver:
            self.driver.close()

    def setup_constraints(self):
        if not self.verify_connectivity():
            return
        with self.driver.session() as session:
            try:
                session.run("CREATE CONSTRAINT doc_id IF NOT EXISTS FOR (d:Document) REQUIRE d.id IS UNIQUE")
                session.run("CREATE CONSTRAINT dp_id IF NOT EXISTS FOR (p:DocumentPage) REQUIRE p.id IS UNIQUE")
                session.run("CREATE CONSTRAINT ev_id IF NOT EXISTS FOR (e:Evidence) REQUIRE e.id IS UNIQUE")
                session.run("CREATE CONSTRAINT opt_id IF NOT EXISTS FOR (o:Option) REQUIRE o.id IS UNIQUE")
                session.run("CREATE CONSTRAINT dec_id IF NOT EXISTS FOR (d:DecisionPack) REQUIRE d.id IS UNIQUE")
            except Exception as e:
                logger.error(f"Constraint setup failed: {e}")

    def sync_decision_pack(self, pack_id: str, db_session):
        if not self.verify_connectivity():
            return False

        # Fetch data from MySQL
        pack = db_session.query(DecisionPack).filter(DecisionPack.id == pack_id).first()
        if not pack:
            return False
        docs = db_session.query(Document).filter(Document.decision_pack_id == pack_id).all()
        pages = db_session.query(DocumentPage).join(Document).filter(Document.decision_pack_id == pack_id).all()
        evidence_list = db_session.query(Evidence).filter(Evidence.decision_pack_id == pack_id).all()

        with self.driver.session() as session:
            # Sync DecisionPack
            session.run("""
                MERGE (dp:DecisionPack {id: $id})
                SET dp.name = $name
            """, id=pack.id, name=pack.name)

            # Sync Documents and link to DecisionPack
            for doc in docs:
                doc_status_val = doc.status.value if hasattr(doc.status, "value") else doc.status
                session.run("""
                    MERGE (d:Document {id: $id})
                    SET d.filename = $filename, d.status = $status
                    WITH d
                    MATCH (dp:DecisionPack {id: $pack_id})
                    MERGE (dp)-[:HAS_DOCUMENT]->(d)
                """, id=doc.id, filename=doc.filename, status=doc_status_val, pack_id=pack_id)

            # Sync DocumentPages
            for page in pages:
                session.run("""
                    MERGE (p:DocumentPage {id: $id})
                    SET p.page_number = $page_number
                    WITH p
                    MATCH (d:Document {id: $doc_id})
                    MERGE (d)-[:HAS_PAGE]->(p)
                """, id=page.id, page_number=page.page_number, doc_id=page.document_id)

            # Sync Evidence
            for ev in evidence_list:
                doc_status = db_session.query(Document.status).filter(Document.id == ev.source_document_id).scalar()
                doc_status_val = doc_status.value if hasattr(doc_status, "value") else doc_status
                
                ev_status_val = ev.status.value if hasattr(ev.status, "value") else ev.status
                sync_status = "REJECTED" if doc_status_val == "REJECTED" else ev_status_val
                
                session.run("""
                    MERGE (e:Evidence {id: $id})
                    SET e.label = $label, e.value = $value, e.status = $status,
                        e.document_id = $doc_id, e.page = $page, e.filename = $filename
                    WITH e
                    MATCH (p:DocumentPage {id: $page_id})
                    MERGE (p)-[:SUPPORTS]->(e)
                """, 
                id=ev.id, label=ev.label, value=float(ev.value) if ev.value is not None else None, status=sync_status,
                doc_id=ev.source_document_id, page=ev.page, filename=next((d.filename for d in docs if d.id == ev.source_document_id), "unknown"),
                page_id=next((p.id for p in pages if p.document_id == ev.source_document_id and p.page_number == ev.page), None)
                )

        return True
