import os
import json
from dotenv import load_dotenv
from app.logger.logger import custom_logger

load_dotenv()


class Config:
    """Config for the app."""

    # qdrant
    QDRANT_URL = os.getenv("QDRANT_URL")
    QDRANT_API_KEY = os.getenv("QDRANT_CLOUD_KEY")
    COLLECTION_NAME = os.getenv("COLLECTION_NAME")

    # huggingface
    HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")

    # data dir
    DATA_DIR = os.getenv("DATA_DIR")

    # bucket
    BUCKET_NAME = os.getenv("BUCKET_NAME")

    # image url template
    IMAGE_URL_TEMPLATE = os.getenv("IMAGE_URL_TEMPLATE")


def print_config(config: Config):
    """Print config."""
    custom_logger.debug("Printing config")
    for attr in dir(config):
        if attr.startswith("__"):
            continue
        print(f"  {attr}: {getattr(config, attr)}")


config = Config()
