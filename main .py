import SentenceTransformer
import numpy as np

class EndeeVectorDB:
    def __init__(self):
        self.vectors = []

    # Add data to vector DB
    def add_document(self, text):
        embedding = self.model.encode(text)
        self.vectors.append((text, embedding))

    # Search similar data
    def search(self, query, top_k=1):
        query_embedding = self.model.encode(query)

        scores = []
        for text, emb in self.vectors:
            score = np.dot(query_embedding, emb)
            scores.append((score, text))

        scores.sort(reverse=True)
        return [text for _, text in scores[:top_k]]

    # Load model
    def load_model(self):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')


# -------------------------------
# Run as standalone service
# -------------------------------
if __name__ == "__main__":
    db = EndeeVectorDB()
    db.load_model()

    print("🚀 Endee Vector DB Service Started")

    # Sample data
    db.add_document("Artificial Intelligence is the future")
    db.add_document("Machine Learning is a subset of AI")
    db.add_document("Deep Learning uses neural networks")

    while True:
        query = input("\nEnter your query (type 'exit' to quit): ")

        if query.lower() == "exit":
            print("👋 Exiting...")
            break

        results = db.search(query)

        print("🔍 Result:", results[0] if results else "No match found")