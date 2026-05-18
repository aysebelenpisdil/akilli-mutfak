"""
Pre-downloads embedding and reranker models from HuggingFace into the local cache.
Run this during the DigitalOcean build phase so models are cached before first request.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.config import settings


def main():
    from sentence_transformers import SentenceTransformer, CrossEncoder

    print(f"Downloading embedding model: {settings.EMBEDDING_MODEL} ...")
    SentenceTransformer(settings.EMBEDDING_MODEL)
    print("Embedding model ready.")

    print(f"Downloading reranker model: {settings.RERANKER_MODEL} ...")
    CrossEncoder(settings.RERANKER_MODEL)
    print("Reranker model ready.")

    print("All models downloaded successfully.")


if __name__ == "__main__":
    main()
