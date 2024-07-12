import uuid
import numpy as np
from qdrant_client.models import PointStruct

from app.api.database.vector_db import qdrant_client
from app.core.config import config


def get_collection_info():
    return qdrant_client.get_collection(config.COLLECTION_NAME)


def add_embedding(id: str, embedding: np.ndarray, metadata: dict):
    qdrant_client.upsert(
        collection_name=config.COLLECTION_NAME,
        wait=True,
        points=[
            PointStruct(id=id, vector=embedding, payload=metadata),
        ],
    )
    return id


def retrieve(query: np.ndarray):
    return qdrant_client.query_points(
        collection_name=config.COLLECTION_NAME,
        query=query,
        limit=9,
    )
