from sentence_transformers import SentenceTransformer
from pathlib import Path
import json

BASE = Path(__file__).parent
IN_PATH = BASE / "data" / "chunks.json"


with open(IN_PATH, encoding="utf-8") as f:
        chunks = json.load(f)

texts = [chunk["text"] for chunk in chunks]      

model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

embeddings = model.encode(texts,batch_size=32,show_progress_bar=True)

print(embeddings.shape)

similarities = model.similarity(embeddings, embeddings)
print(similarities)