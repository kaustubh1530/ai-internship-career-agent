import json
import os
import numpy as np
import faiss
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Load jobs
with open("../data/live_jobs.json", "r") as f:
    jobs = json.load(f)

texts = []
metadata = []

for job in jobs:
    text = f"{job['title']} {job.get('description', '')}"
    texts.append(text)
    metadata.append(job)

# Generate embeddings
embeddings = []

for text in texts:
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text[:2000]
    )
    embeddings.append(response.data[0].embedding)

# Convert to numpy
embeddings = np.array(embeddings).astype("float32")

# Create FAISS index
dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(embeddings)

# Save index
faiss.write_index(index, "job_index.faiss")

# Save metadata
with open("job_metadata.json", "w") as f:
    json.dump(metadata, f)

print("✅ Embeddings created and stored!")