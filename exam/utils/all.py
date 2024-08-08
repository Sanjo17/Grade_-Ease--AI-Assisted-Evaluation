# Load model directly
from sentence_transformers import SentenceTransformer
import numpy as np
from numpy.linalg import norm

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
sentences = ["this is a joyful person"]
embeddings = model.encode(sentences)
query_embedding = model.encode("That is a happy person")
def cosine_similarity(a, b):
    return np.dot(a, b)/(norm(a)*norm(b))

for e, s in zip(embeddings, sentences):
    print(s, " -> similarity score = ",cosine_similarity(e, query_embedding))