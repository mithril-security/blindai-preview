import torch
import os
def torch_to_onnx(model: torch.nn.Module):
    # We convert the method to ONNX
    # For the mean time, we will return a downloaded whisper model

    filename="fake-whisper-model.onnx"
    os.system(f"gdown --id 1wqg1F0UkEdm3KB7n1BjfRLHnzKU2-G5S --output {filename}")

    # Return the absolute path of the file
    return os.path.abspath(filename)