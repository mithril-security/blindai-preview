import blindai_preview as blindai
import os

# Set up connection to BlindAI
connection = blindai.connect("localhost", hazmat_http_on_untrusted_port=True)

# Download audio file
output = os.path.join(os.path.dirname(__file__), "taunt.wav")
os.system(f"wget https://www2.cs.uic.edu/~i101/SoundFiles/taunt.wav -O {output}")

# Transcribe audio file
transcript = blindai.Audio.transcribe(output, connection=connection)
assert transcript == " Now go away, or I shall taunt you a second timer!"
