import os
import glob
from PyPDF2 import PdfReader
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

DOCS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "docs")

corpus = []
vectorizer = TfidfVectorizer(stop_words='english')
tfidf_matrix = None

def init_rag():
    global corpus, vectorizer, tfidf_matrix
    corpus = []
    
    if not os.path.exists(DOCS_DIR):
        print(f"Docs directory not found at {DOCS_DIR}")
        return

    pdf_files = glob.glob(os.path.join(DOCS_DIR, "*.pdf"))
    
    for pdf_path in pdf_files:
        filename = os.path.basename(pdf_path)
        try:
            reader = PdfReader(pdf_path)
            for i, page in enumerate(reader.pages):
                text = page.extract_text()
                if text and text.strip():
                    corpus.append({
                        "filename": filename,
                        "page": i + 1,
                        "text": text.strip()
                    })
        except Exception as e:
            print(f"Error reading {filename}: {e}")

    if corpus:
        texts = [doc["text"] for doc in corpus]
        tfidf_matrix = vectorizer.fit_transform(texts)
        print(f"RAG initialized with {len(corpus)} pages from {len(pdf_files)} documents.")
    else:
        print("No content found in documents.")

def search_rag(query: str, top_k=1):
    if not corpus or tfidf_matrix is None:
        return "RAG system is not initialized or no documents found."

    query_vec = vectorizer.transform([query])
    similarities = cosine_similarity(query_vec, tfidf_matrix).flatten()
    
    # Get top k indices
    top_indices = similarities.argsort()[-top_k:][::-1]
    
    # If the highest similarity is very low, it might be out of context
    if similarities[top_indices[0]] < 0.15:
        return None  # No confident match found
        
    responses = []
    for idx in top_indices:
        if similarities[idx] > 0.15:
            doc = corpus[idx]
            # Clean up the text for display
            import re
            clean_text = doc['text']
            
            # Remove PDF headers and footers
            clean_text = clean_text.replace("STRICTLY CONFIDENTIAL - ASI INTELLIGENCE INTERNAL USE ONLY", "")
            clean_text = re.sub(r'Section \d+ / Page \d+', '', clean_text)
            clean_text = re.sub(r'Page \d+', '', clean_text)
            
            # Remove title-like uppercase strings if needed, or just clean spacing
            clean_text = ' '.join(clean_text.split())
            
            # Split into sentences
            sentences = re.split(r'(?<=[.!?]) +', clean_text)
            
            # Find the most relevant sentence based on query words
            query_words = set(query.lower().split())
            best_sentence = clean_text[:200] + "..." # Fallback
            max_matches = -1
            
            for sentence in sentences:
                matches = sum(1 for word in query_words if word in sentence.lower())
                if matches > max_matches and len(sentence) > 15:
                    max_matches = matches
                    best_sentence = sentence
                    
            if max_matches == 0:
                # If no word matches precisely in the sentence (which happens with TF-IDF vs exact match), 
                # just return the first proper sentence.
                best_sentence = sentences[0] if sentences else clean_text[:200]
                
            responses.append(f"{best_sentence.strip()} [Source: {doc['filename']}, page {doc['page']}]")

    return "\n\n".join(responses)

# Initialize on import
init_rag()
