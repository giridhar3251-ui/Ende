import streamlit as st
from sentence_transformers import SentenceTransformer
import numpy as np

# -------------------------------
# Simulated Endee Vector Database
# -------------------------------
class EndeeVectorDB:
    def __init__(self):
        self.data = []

    def add(self, text, embedding):
        self.data.append((text, embedding))

    def search(self, query_embedding):
        best_match = ""
        best_score = -1

        for text, emb in self.data:
            score = np.dot(query_embedding, emb)
            if score > best_score:
                best_score = score
                best_match = text

        return best_match


# Initialize DB
db = EndeeVectorDB()

# Load embedding model
model = SentenceTransformer('all-MiniLM-L6-v2')

# -------------------------------
# Streamlit UI
# -------------------------------
st.title("🤖 AI Document Chatbot (RAG with Endee)")

uploaded_file = st.file_uploader("Upload a text file", type=["txt"])

# -------------------------------
# Process Document
# -------------------------------
if uploaded_file is not None:
    text = uploaded_file.read().decode("utf-8")

    # Split into chunks
    chunks = [chunk.strip() for chunk in text.split("\n") if chunk.strip()]

    db.data.clear()

    for chunk in chunks:
        embedding = model.encode(chunk)
        db.add(chunk, embedding)

    st.success("✅ Document stored in Endee Vector DB!")

# -------------------------------
# Query Section
# -------------------------------
query = st.text_input("Ask your question:")

if query:
    query_embedding = model.encode(query)

    result = db.search(query_embedding)

    st.subheader("📌 Answer:")
    st.write(result)