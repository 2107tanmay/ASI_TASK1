import os
from fastapi.testclient import TestClient
import fitz

from app.main import app
from app.db import get_db, engine, Base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from app.db.models.document import Document, DocumentPage
from app.db.models.evidence import Evidence
import app.api.routes.document as document_route

# mock vector store
class MockVectorStore:
    def add_page(self, page_id: str, text: str):
        pass
document_route.VectorStore = MockVectorStore

test_engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)
Base.metadata.create_all(bind=test_engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()
app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

print("Starting tests...")

fixtures_dir = os.path.join(os.path.dirname(__file__), "fixtures")
os.makedirs(fixtures_dir, exist_ok=True)
doc1 = fitz.open()
page1 = doc1.new_page()
page1.insert_text((50, 50), "This is a valid test document. The revenue is $50,000 and profit margin is 15%.")
doc1.save(os.path.join(fixtures_dir, 'valid_doc.pdf'))
doc1.close()

doc2 = fitz.open()
page2 = doc2.new_page()
page2.insert_text((50, 50), "Desktop valuation note.")
doc2.save(os.path.join(fixtures_dir, 'desktop_valuation_note.pdf'))
doc2.close()

with open(os.path.join(fixtures_dir, 'invalid.pdf'), 'wb') as f:
    f.write(b"Not a PDF")

print("Fixtures created.")

# A
file_path = os.path.join(fixtures_dir, "valid_doc.pdf")
with open(file_path, "rb") as f:
    response = client.post("/api/documents/upload", files={"file": ("valid_doc.pdf", f, "application/pdf")})
assert response.status_code == 200, response.text
data = response.json()
assert data["status"] == "ADMISSIBLE"

# B
db = TestingSessionLocal()
doc = db.query(Document).filter(Document.filename == "valid_doc.pdf").first()
response = client.get(f"/api/documents/{doc.id}/pages/1")
assert response.status_code == 200, response.text

# C
evidences = db.query(Evidence).filter(Evidence.source_document_id == doc.id).all()
values = [e.value for e in evidences]
assert 50000 in values
assert 15 in values
db.close()

# D
file_path = os.path.join(fixtures_dir, "desktop_valuation_note.pdf")
with open(file_path, "rb") as f:
    response = client.post("/api/documents/upload", files={"file": ("desktop_valuation_note.pdf", f, "application/pdf")})
assert response.status_code == 200, response.text
assert response.json()["status"] == "REJECTED"

print("All custom tests passed!")

