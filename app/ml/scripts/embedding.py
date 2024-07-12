import torch
from PIL import Image
import numpy as np
from transformers import AutoProcessor, AutoTokenizer
import onnxruntime as ort

from app.logger.logger import custom_logger

# load the model and the tokenizer
ort_vision = ort.InferenceSession(
    "app/resources/models/siglip_vision.onnx",
    providers=["CPUExecutionProvider"],
)
custom_logger.info("Loaded vision model")

ort_text = ort.InferenceSession(
    "app/resources/models/siglip_text.onnx",
    providers=["CPUExecutionProvider"],
)
custom_logger.info("Loaded text model")

processor = AutoProcessor.from_pretrained("nielsr/siglip-base-patch16-224")
custom_logger.info("Loaded processor")

tokenizer = AutoTokenizer.from_pretrained("nielsr/siglip-base-patch16-224")
custom_logger.info("Loaded tokenizer")


class Embedding:
    @staticmethod
    def to_numpy(tensor: torch.Tensor):
        return (
            tensor.detach().cpu().numpy()
            if tensor.requires_grad
            else tensor.cpu().numpy()
        )

    def embedding_image(self, image: Image.Image) -> np.ndarray:
        input = processor(images=image, return_tensors="pt")
        ort_inputs = {
            ort_vision.get_inputs()[0].name: self.to_numpy(tuple(input.values())[0])
        }
        image_feature = ort_vision.run(None, ort_inputs)
        return image_feature[1].squeeze()

    def embedding_text(self, text: str) -> np.ndarray:
        text_token = tokenizer([text], return_tensors="pt")
        ort_input = {
            ort_text.get_inputs()[0].name: self.to_numpy(tuple(text_token.values())[0])
        }
        text_features = ort_text.run(None, ort_input)
        return np.float32(text_features[1].squeeze())
