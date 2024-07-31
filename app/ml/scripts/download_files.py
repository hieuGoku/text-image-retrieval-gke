import os

from huggingface_hub import login, snapshot_download

from app.core.config import config
from app.logger.logger import custom_logger


def download_models():
    siglip_path = os.path.join(config.MODEL_DIR, "siglip")
    os.makedirs(siglip_path, exist_ok=True)
    if not os.listdir(siglip_path):
        custom_logger.info("Siglip models not found. Downloading models ...")
        login(config.HUGGINGFACE_API_KEY)
        snapshot_download(
            repo_id="hieuGoku/siglip_onnx",
            local_dir=siglip_path,
        )
        custom_logger.info("Downloaded models")

    return siglip_path


if __name__ == "__main__":
    download_models()
