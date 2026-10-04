import hashlib
from typing import List
from app.db import get_db
from app.db.models.document import Document, DocumentPage
from app.db.models.evidence import Evidence
from app.db.models.option import Option
from app.graph.driver import neo4j_driver

class GraphBuilder:
    """Service that syncs MySQL entities to Neo4j graph.
    It creates nodes for Document, DocumentPage, Evidence, and Option, and
    establishes relationships according to the domain model.
    """

    def __init__(self, db_session):
        self.db = db_session
        self.session = neo4j_driver.session()

    def close(self):
        self.session.close()

    def upsert_document(self, document: Document):
        query = """
        MERGE (d:Document {id: $id})
        SET d.filename = $filename,
            d.sha256 = $sha256,
            d.admissible = $admissible,
            d.created_at = datetime($created_at)
        RETURN d
        """
        self.session.run(
            query,
            id=document.id,
            filename=document.filename,
            sha256=document.sha256,
            admissible=document.admissible,
            created_at=document.created_at.isoformat(),
        )

    def upsert_document_pages(self, document: Document, pages: List[DocumentPage]):
        for page in pages:
            query = """
            MERGE (p:Page {id: $id})
            SET p.page_number = $page_number,
                p.text = $text,
                p.created_at = datetime($created_at)
            WITH p
            MATCH (d:Document {id: $doc_id})
            MERGE (d)-[:HAS_PAGE]->(p)
            """
            self.session.run(
                query,
                id=page.id,
                page_number=page.page_number,
                text=page.text,
                created_at=page.created_at.isoformat(),
                doc_id=document.id,
            )

    def upsert_evidence(self, evidence: Evidence):
        query = """
        MERGE (e:Evidence {id: $id})
        SET e.metric = $metric,
            e.value = $value,
            e.unit = $unit,
            e.source = $source,
            e.created_at = datetime($created_at)
        WITH e
        MATCH (d:Document {id: $doc_id})
        MERGE (d)-[:HAS_EVIDENCE]->(e)
        """
        self.session.run(
            query,
            id=evidence.id,
            metric=evidence.metric,
            value=float(evidence.value) if evidence.value is not None else None,
            unit=evidence.unit,
            source=evidence.source,
            created_at=evidence.created_at.isoformat(),
            doc_id=evidence.document_id,
        )

    def upsert_option(self, option: Option):
        query = """
        MERGE (o:Option {id: $id})
        SET o.label = $label,
            o.description = $description,
            o.created_at = datetime($created_at)
        WITH o
        MATCH (dp:DecisionPack {id: $dp_id})
        MERGE (dp)-[:HAS_OPTION]->(o)
        """
        self.session.run(
            query,
            id=option.id,
            label=option.label,
            description=option.description,
            created_at=option.created_at.isoformat(),
            dp_id=option.decision_pack_id,
        )

    def sync_document(self, document_id: str):
        """Fetch a document and its related entities from MySQL and push to Neo4j.
        This is called after a successful upload.
        """
        doc = self.db.query(Document).filter(Document.id == document_id).first()
        if not doc:
            raise ValueError(f"Document {document_id} not found in DB")
        self.upsert_document(doc)
        pages = self.db.query(DocumentPage).filter(DocumentPage.document_id == doc.id).all()
        self.upsert_document_pages(doc, pages)
        evidences = self.db.query(Evidence).filter(Evidence.document_id == doc.id).all()
        for ev in evidences:
            self.upsert_evidence(ev)
        # Options are linked to decision pack, not document, but we sync all options for completeness
        options = self.db.query(Option).filter(Option.decision_pack_id == doc.decision_pack_id).all()
        for opt in options:
            self.upsert_option(opt)
        self.session.close()
