import os
import io
from uuid import uuid4
import pandas as pd
from PIL import Image
import gdown
from pathlib import Path
from tqdm import tqdm
from google.cloud.storage import Client, transfer_manager

from app.api.database import qdrant_execute
from app.ml.scripts.embedding import Embedding
from app.core.config import config
from app.logger.logger import custom_logger

embedding = Embedding()


class PrepareData:

    def __init__(self):
        self.parquet_dir = os.path.join(config.DATA_DIR, "parquet")
        self.image_dir = os.path.join(config.DATA_DIR, "art_dataset")

    def download_data(self):
        os.makedirs(self.parquet_dir, exist_ok=True)

        if not os.path.exists(f"{self.parquet_dir}/data.parquet"):
            custom_logger.info("Downloading data ...")
            id = "1hrH0xzsgpmFShRfsqjoS_2EwppN2_u8D"
            gdown.download(id=id, output=f"{self.parquet_dir}/data.parquet")
            custom_logger.info(f"Data downloaded to {self.parquet_dir} successfully")
            return id

        custom_logger.info("Data already exists")

    def load_data(self):
        data_df = pd.read_parquet(f"{self.parquet_dir}/data.parquet")

        if not os.path.exists(self.image_dir):
            custom_logger.info("Creating images directory ...")
            os.makedirs(self.image_dir)
            custom_logger.info(f"Images directory created at {self.image_dir}")

        custom_logger.info("Loading data to images directory ...")
        for i in tqdm(range(len(data_df))):
            image_pil = Image.open(io.BytesIO(data_df.iloc[i, 0]["bytes"]))

            width = 500
            ratio = width / float(image_pil.size[0])
            height = int((float(image_pil.size[1]) * float(ratio)))

            image_id = str(uuid4())
            image_pil.resize((width, height), Image.Resampling.LANCZOS).save(
                f"{self.image_dir}/{image_id}.jpg"
            )

        custom_logger.info("Data loaded to images directory successfully")

        return self.image_dir

    def embed_images(self):
        image_files = os.listdir(self.image_dir)

        custom_logger.info("Embedding images to Qdrant DB ...")
        for image_file in image_files:
            image_id = image_file.split(".")[0]
            image_path = os.path.join(self.image_dir, image_file)
            image = Image.open(image_path)
            image_embedding = embedding.embedding_image(image)

            qdrant_execute.add_embedding(
                id=image_id,
                embedding=image_embedding,
                metadata={"image_id": image_id},
            )

        custom_logger.info("Images embedded to Qdrant DB successfully")

    @staticmethod
    def upload_directory_with_transfer_manager(
        bucket_name, source_directory, workers=8
    ):
        """Upload every file in a directory, including all files in subdirectories.

        Each blob name is derived from the filename, not including the `directory`
        parameter itself. For complete control of the blob name for each file (and
        other aspects of individual blob metadata), use
        transfer_manager.upload_many() instead.
        """

        # The ID of your GCS bucket
        # bucket_name = "your-bucket-name"

        # The directory on your computer to upload. Files in the directory and its
        # subdirectories will be uploaded. An empty string means "the current
        # working directory".
        # source_directory=""

        # The maximum number of processes to use for the operation. The performance
        # impact of this value depends on the use case, but smaller files usually
        # benefit from a higher number of processes. Each additional process occupies
        # some CPU and memory resources until finished. Threads can be used instead
        # of processes by passing `worker_type=transfer_manager.THREAD`.
        # workers=8

        storage_client = Client().from_service_account_json(
            "ansible/secret_keys/fabled-essence-428302-u8-df3a5a196514.json"
        )
        bucket = storage_client.bucket(bucket_name)

        # Generate a list of paths (in string form) relative to the `directory`.
        # This can be done in a single list comprehension, but is expanded into
        # multiple lines here for clarity.

        # First, recursively get all files in `directory` as Path objects.
        directory_as_path_obj = Path(source_directory)
        paths = directory_as_path_obj.rglob("*")

        # Filter so the list only includes files, not directories themselves.
        file_paths = [path for path in paths if path.is_file()]

        # These paths are relative to the current working directory. Next, make them
        # relative to `directory`
        relative_paths = [path.relative_to(source_directory) for path in file_paths]

        # Finally, convert them all to strings.
        string_paths = [str(path) for path in relative_paths]

        print("Found {} files.".format(len(string_paths)))

        # Start the upload.
        results = transfer_manager.upload_many_from_filenames(
            bucket,
            string_paths,
            source_directory=source_directory,
            max_workers=workers,
            worker_type=transfer_manager.THREAD,
        )

        for name, result in zip(string_paths, results):
            # The results list is either `None` or an exception for each filename in
            # the input list, in order.

            if isinstance(result, Exception):
                print("Failed to upload {} due to exception: {}".format(name, result))
            else:
                print("Uploaded {} to {}.".format(name, bucket.name))

        custom_logger.info("Images uploaded to GCS bucket successfully")

    def pipeline(self):
        try:
            self.download_data()
            self.load_data()
            self.embed_images()
            self.upload_directory_with_transfer_manager(
                bucket_name=config.BUCKET_NAME,
                source_directory=self.image_dir,
                workers=4,
            )
            custom_logger.info("Pipeline executed successfully")
        except Exception as e:
            custom_logger.error(f"Error in pipeline: {e}")
            raise ValueError(f"Error in pipeline: {e}")


if __name__ == "__main__":
    prepare_data = PrepareData()
    prepare_data.pipeline()
