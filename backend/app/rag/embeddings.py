import os
from pathlib import Path
from functools import lru_cache
from langchain_community.embeddings import JinaEmbeddings


#0. Config
jina_api_key = os.getenv("JINA_API_KEY")
if not jina_api_key:
    raise ValueError("JINA_API_KEY environment variable set nahi hai!")

@lru_cache(maxsize=1)
def get_embeddings() -> JinaEmbeddings:
    """Load the Jina AI embedding model once."""
    return JinaEmbeddings(
        model_name="jina-embeddings-v3",  # Aap apni zaroorat ke hisab se model badal sakte hain (jaise jina-embeddings-v2-base-en)
        jina_api_key=jina_api_key
    )