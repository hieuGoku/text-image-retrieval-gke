from PIL import Image

from app.api.database.qdrant_execute import retrieve
from app.core.config import config
from app.ml.scripts.embedding import Embedding

embedding = Embedding()


class RetrievalService:
    @staticmethod
    def get_urls(results):
        image_ids = [
            results.points[id].payload["image_id"] for id in range(len(results.points))
        ]

        urls = [
            config.IMAGE_URL_TEMPLATE.format(image_id=image_id)
            for image_id in image_ids
        ]

        return urls

    def retrieve_by_text(self, text: str = None):
        text_embedding = embedding.embedding_text(text)
        results = retrieve(query=text_embedding)
        return self.get_urls(results)

    def retrieve_by_image(self, image: Image = None):
        image_embedding = embedding.embedding_image(image)
        results = retrieve(query=image_embedding)
        return self.get_urls(results)
