import unittest
import blindai_preview


class TestWhisperAudio(unittest.TestCase):
    def test_whisper_transcribe(self):
        # Create connection to BlindAi
        connection = blindai_preview.connect("localhost", hazmat_http_on_untrusted_port=True, simulation_mode=False)
        res = blindai_preview.Audio.transcribe(
            connection=connection,
            model="tiny.en",
            file="taunt.wav"
        )

        print(res)
