import io

from fastapi import APIRouter, File, UploadFile
from PIL import Image

from app.api.responses.base import BaseResponse
from app.api.services.retrieval_service import RetrievalService
from app.logger.logger import custom_logger

retrieval_service = RetrievalService()

router = APIRouter()


@router.get("/retrieve_by_text")
async def retrieve_by_text(query: str = None):
    try:
        if not query:
            custom_logger.error("Query is empty")
            return BaseResponse.error_response(message="Query is empty")

        custom_logger.info(f"Retrieving image for query: {query}")
        urls = retrieval_service.retrieve_by_text(text=query)

        return BaseResponse.success_response(data=urls)

    except Exception as e:
        custom_logger.error(f"Error in retrieving image: {e}")
        return BaseResponse.error_response(message="Error in retrieving image")


@router.post("/retrieve_by_image")
async def retrieve_by_image(image: UploadFile = File(...)):
    try:
        contents = await image.read()

        image = Image.open(io.BytesIO(contents))
        texts = retrieval_service.retrieve_by_image(image=image)

        return BaseResponse.success_response(data=texts)

    except Exception as e:
        custom_logger.error(f"Error in retrieving text: {e}")
        return BaseResponse.error_response(message="Error in retrieving text")
