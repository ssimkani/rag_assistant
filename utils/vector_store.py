from pinecone import Pinecone, ServerlessSpec
from utils.embedder import get_gemini_embedding
from utils.config import PINECONE_API_KEY, PINECONE_INDEX_NAME, NUM_CHUNKS, EXPECTED_DIM
import streamlit as st
import numpy as np

pc = Pinecone(api_key=PINECONE_API_KEY)

if not pc.has_index(PINECONE_INDEX_NAME):
    pc.create_index(
        name=PINECONE_INDEX_NAME,
        dimension=768,
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region="us-east-1"),
    )

index = pc.Index(PINECONE_INDEX_NAME)

# Helper that makes sure embedding is a list of floats
def _to_float_list(x):
  
    # Convert numpy array to list
    if isinstance(x, np.ndarray):
        x = x.reshape(-1).astype(float).tolist()

    elif isinstance(x, (list, tuple)) and len(x) == 1 and isinstance(x[0], (list, tuple, np.ndarray)):
        x = list(x[0])
    else:
        x = list(x)

    # Check dimensions
    if len(x) != EXPECTED_DIM:
        raise ValueError(f"Embedding dim {len(x)} != {EXPECTED_DIM}")

    return [float(v) for v in x]

def upsert_chunks(uid, chunks: list[str]):
    uid = str(uid)

    index.delete(filter={"uid": {"$eq": uid}})

    # Skip if no valid chunks
    valid_chunks = [chunk.strip() for chunk in chunks if chunk.strip()]

    if not valid_chunks:
        st.warning("No notes provided. Skipping upload.")
        return

    # Upsert new vectors
    vectors = []
    for i, chunk in enumerate(valid_chunks):
        embedding = get_gemini_embedding(chunk)

        # floats from embedding
        embedding = _to_float_list(embedding)
        vectors.append(
            {
                "id": f"{uid}_chunk_{i}",
                "values": embedding,
                "metadata": {"text": chunk, "uid": uid},
            }
        )
    index.upsert(vectors=vectors, batch_size=100)

def search_top_k(uid, query: str, k=NUM_CHUNKS) -> list[str]:
    uid = str(uid)
  
    query_vec = get_gemini_embedding(query)

    # Convert to float
    query_vec = _to_float_list(query_vec)


    results = index.query(
        vector=query_vec, top_k=k, include_metadata=True, filter={"uid": {"$eq": uid}}
    )
    return [match["metadata"]["text"] for match in results["matches"]]
