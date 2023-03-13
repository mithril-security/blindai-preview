import whisper
from typing import Optional, Dict
from .utils import torch_to_onnx
from .client import BlindAiConnection


class Audio:
    blindai_connection: "BlindAiConnection"

    @classmethod
    def transcribe(
        cls,
        model: str,
        file,
    ) -> Dict:

        """
        - it retrieves the ONNX data associated with the model name
        - it reads the file-like object with a sound library (e.g. soundfile) to get a numpy array
        - it performs some Whisper-specific preprocessing on the client-side
        - it calls “predict” to get an prediction object from the server
        - it performs some post-processing to get a string and returns that string
        """

        # Get `model` from OpenAI's Whisper service
        torch_model = whisper.load_model(model)

        # Convert audio into numpy array
        input_array = whisper.audio.load_audio(file)

        # Convert model to ONNX with `torch_to_onnx`
        onnx_file_path = torch_to_onnx(torch_model)

        # Upload ONNX model to BlindAI server
        response = cls.blindai_connection.upload_model(onnx_file_path, model_name=model, optimize=False)

        cls.blindai_connection.run_model(model_id=response.model_id, input_tensors=input_array)

        return dict(model=onnx_file_path, array=input_array, model_id=response.model_id)
