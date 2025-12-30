from google import genai
from google.genai import types
from utils.config import EMBEDDING_MODEL
import numpy as np

client = genai.Client()

def get_gemini_embedding(text: str) -> list[float]:
    result = client.models.embed_content(
        model=EMBEDDING_MODEL, contents=text,
        config=types.EmbedContentConfig(
            task_type="RETRIEVAL_QUERY",
            output_dimensionality=768
        )
    )
    
    # Extract the embedding and normalize it
    embedding = np.array(result.embeddings[0].values)
    embedding = embedding / np.linalg.norm(embedding)

    return embedding