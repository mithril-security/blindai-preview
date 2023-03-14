import whisper
from typing import Optional, Dict
from .utils import torch_to_onnx
from .client import BlindAiConnection
from transformers import WhisperProcessor


class Audio:
    blindai_connection: "BlindAiConnection"

    @classmethod
    def transcribe(
        cls,
        model: str,
        file: str,
        transformer: str = "openai/whisper-tiny.en",
    ) -> Dict:
        """
        BlindAI Whisper API which converts speech to text based on the model passed.

        Args:
            model: str
                The Whisper model
            file: str
                Audio file to transcribe
            transformer:
                HuggingFace Whisper Transformer to use.
        Returns:
            Dict:
                The transcription object containing, text and the tokens
        """

        # Get `model` from OpenAI's Whisper service
        torch_model = whisper.load_model(model)

        # Convert audio into numpy array
        audio = whisper.load_audio(file).flatten()

        # Trim/pad audio to 30s with `pad_or_trim`
        audio = whisper.pad_or_trim(audio)

        # Convert loaded audio to log_mel_spectrogram
        input_mel = whisper.log_mel_spectrogram(audio).unsqueeze(0)

        # Convert model to ONNX with `torch_to_onnx`
        onnx_file_path = torch_to_onnx(torch_model)

        # Upload ONNX model to BlindAI server
        response = cls.blindai_connection.upload_model(
            onnx_file_path, model_name=model, optimize=False
        )

        # Run ONNX model with `input_array` on BlindAI server
        res = cls.blindai_connection.run_model(
            model_id=response.model_id, input_tensors=input_mel
        )

        # Convert each output BlindAI Tensor object into PyTorch Tensor
        res = [t.as_torch() for t in res.output]

        # Load the Whisper Transformer object.
        tokenizer = WhisperProcessor.from_pretrained(transformer)

        # Extract tokens from result
        tokens = res[0][0].numpy()

        # Use transform to decode tokens
        text = tokenizer.batch_decode(tokens, skip_special_tokens=True)

        # Create transcription object
        transcription = dict(text=text, tokens=tokens)

        return transcription
