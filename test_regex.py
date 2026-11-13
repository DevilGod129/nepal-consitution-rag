from sentence_transformers import SentenceTransformer

sentences = ["It is the duty of every person to observe this Constitution.",
"Every citizen must follow the Constitution.",
"The weather in Pokhara is sunny today."]

model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
embeddings = model.encode(sentences)
print(embeddings.shape)
print(model.max_seq_length)

similarities = model.similarity(embeddings, embeddings)
print(similarities)