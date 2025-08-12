import os
from flask import Flask, request, render_template_string, send_file
from TTS.api import TTS
from pydub import AudioSegment

# -------------- CONFIG --------------
VOICE_SAMPLE = "audio [vocals].mp3"  # Your clean voice sample
OUTPUT_WAV = "output.wav"
MODEL_NAME = "tts_models/multilingual/multi-dataset/your_voice_hindi"
# -------------------------------------

# Step 1: Train voice cloning model (Transfer Learning from multilingual model)
print("[1/3] Loading base multilingual model (Hindi-capable)...")
tts = TTS(model_name="tts_models/multilingual/multi-dataset/your_tts", progress_bar=True, gpu=False)

print("[2/3] Fine-tuning on your voice sample...")
tts.tts_to_file(
    text="यह एक नमूना वाक्य है।",  # Sample Hindi text to help adaptation
    file_path=OUTPUT_WAV,
    speaker_wav=VOICE_SAMPLE,
    language="hi"
)
# NOTE: Coqui TTS does not need heavy 'training' for voice cloning — it adapts instantly from sample

# Step 3: Setup Flask Web UI
print("[3/3] Starting Web UI...")

app = Flask(__name__)
HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>Hindi Voice Clone TTS</title>
</head>
<body style="font-family:sans-serif;">
    <h2>Type Hindi text below and generate speech in your cloned voice</h2>
    <form action="/" method="post">
        <textarea name="text" rows="4" cols="60" placeholder="हिन्दी में लिखें..." required></textarea><br><br>
        <button type="submit">Generate Speech</button>
    </form>
    {% if audio_file %}
        <h3>Generated Audio:</h3>
        <audio controls>
            <source src="{{ audio_file }}" type="audio/wav">
        </audio>
    {% endif %}
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    audio_file = None
    if request.method == "POST":
        text = request.form["text"]
        output_file = OUTPUT_WAV
        tts.tts_to_file(
            text=text,
            file_path=output_file,
            speaker_wav=VOICE_SAMPLE,
            language="hi"
        )
        audio_file = "output.wav"
    return render_template_string(HTML_PAGE, audio_file=audio_file)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)
