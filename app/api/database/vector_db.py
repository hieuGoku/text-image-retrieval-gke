"""Vector database client."""

from qdrant_client import QdrantClient
from qdrant_client.http import models
from qdrant_client.http.models import CollectionDescription

from app.core.config import config
from app.logger.logger import custom_logger

custom_logger.info("Initializing vector database client")
qdrant_client = QdrantClient(
    url=config.QDRANT_URL,
    api_key=config.QDRANT_API_KEY,
)


def get_or_create_collection(collection_name: str):
    collection_description = CollectionDescription(name=collection_name)
    list_of_collections = qdrant_client.get_collections().collections

    if collection_description in list_of_collections:
        custom_logger.info(
            f"Found collection {collection_name} in Qdrant DB, skipping creation and using it."
        )
        return collection_name

    custom_logger.info(f"Creating collection {collection_name} in Qdrant DB")
    qdrant_client.create_collection(
        collection_name=collection_name,
        vectors_config=models.VectorParams(size=768, distance=models.Distance.COSINE),
    )
    return collection_name


get_or_create_collection(config.COLLECTION_NAME)
