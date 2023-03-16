import whisper
from typing import Optional
from .utils import torch_to_onnx
from .client import BlindAiConnection, connect
from transformers import WhisperProcessor
import torch


DEFAULT_BLINDAI_ADDR = "https://mithrilsecurity/blindai/"
DEFAULT_WHISPER_MODEL = "medium.en"
DEFAULT_TEE_OPTIONS = ["sgx", "bento"]
DEFAULT_TEE = "sgx"
DEFAULT_TRANSFORMER = f"openai/whisper-{DEFAULT_WHISPER_MODEL}"


def _preprocess_audio(file) -> torch.Tensor:
    """
    Preprocess audio file to be used with Whisper model.

    Args:
        file: str
            Audio file to preprocess

    Returns:
        torch.Tensor:
            The preprocessed audio file
    """
    # Convert audio into numpy array
    audio = whisper.load_audio(file).flatten()

    # Trim/pad audio to 30s with `pad_or_trim`
    audio = whisper.pad_or_trim(audio)

    # Convert loaded audio to log_mel_spectrogram
    return whisper.log_mel_spectrogram(audio).unsqueeze(0)


def _get_connection(
    connection: Optional["BlindAiConnection"], tee: Optional[str]
) -> "BlindAiConnection":
    """
    Get the BlindAI connection object.

    Args:
        connection: Optional[BlindAiConnection]
            The BlindAI connection object

    Returns:
        BlindAiConnection:
            The BlindAI connection object
    """
    if connection is None:
        addr = f"{DEFAULT_BLINDAI_ADDR}/{tee}"
        connection = connect(addr)

    return connection


class Audio:
    @classmethod
    def transcribe(
        cls,
        file: str,
        model: str = DEFAULT_WHISPER_MODEL,
        connection: Optional["BlindAiConnection"] = None,
        tee: Optional[str] = DEFAULT_TEE,
    ) -> str:
        """
        BlindAI Whisper API which converts speech to text based on the model passed.

        Args:

            file: str
                Audio file to transcribe.
            model: str
                The Whisper model. Defaults to "medium".
            connection: Optional[BlindAiConnection]
                The BlindAI connection object. Defaults to None.
            tee: Optional[str]
                The Trusted Execution Environment to use. Defaults to "sgx".
        Returns:
            Dict:
                The transcription object containing, text and the tokens
        """

        # Check which TEE to use
        if tee not in DEFAULT_TEE_OPTIONS:
            raise ValueError(f"tee must be one of {DEFAULT_TEE_OPTIONS}")

        # Get `model` from OpenAI's Whisper service
        torch_model = whisper.load_model(model)

        # Preprocess audio file
        input_mel = _preprocess_audio(file)

        # Convert model to ONNX with `torch_to_onnx`
        onnx_file_path = torch_to_onnx(torch_model)

        # Get BlindAI connection object
        with _get_connection(connection, tee) as connection:
            # Upload ONNX model to BlindAI server
            response = connection.upload_model(
                onnx_file_path, model_name=model, optimize=True
            )

            # Run ONNX model with `input_array` on BlindAI server
            res = connection.run_model(
                model_id=response.model_id, input_tensors=input_mel
            )

            # Convert each output BlindAI Tensor object into PyTorch Tensor
            res = [t.as_torch() for t in res.output]  # type: ignore

            # Load the Whisper Transformer object.
            tokenizer = WhisperProcessor.from_pretrained(DEFAULT_TRANSFORMER)

            # Extract tokens from result
            tokens = res[0][0].numpy()  # type: ignore

            # Use transform to decode tokens
            text = tokenizer.batch_decode(tokens, skip_special_tokens=True).pop()

            return text
