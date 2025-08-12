import gradio as gr
import os
from TTS.api import TTS

# Pretrained multi-speaker TTS model
model_name = TTS.list_models()[0]  # पहला मॉडल ले रहा हूँ, आप चाहें तो specific चुनें
tts = TTS(model_name=model_name, progress_bar=False, gpu=False)

def clone_and_tts(text, speaker_wav):
    if not text.strip():
        return "Error: टेक्स्ट खाली है!"
    if not speaker_wav:
        return "Error: आवाज़ की फ़ाइल अपलोड करें!"

    # आउटपुट फाइल
    output_path = "output.wav"

    # हिंदी टेक्स्ट को आपकी आवाज़ में कन्वर्ट करें
    tts.tts_to_file(
        text=text,
        speaker_wav=speaker_wav,
        language="hi",
        file_path=output_path
    )
    return output_path

# Gradio WebUI
with gr.Blocks() as demo:
    gr.Markdown("## 🎤 Voice Cloning Hindi TTS WebUI")
    with gr.Row():
        text = gr.Textbox(label="हिंदी टेक्स्ट दर्ज करें", placeholder="यहाँ अपना हिंदी टेक्स्ट लिखें...")
        speaker_wav = gr.Audio(label="आपकी आवाज़ की WAV फ़ाइल", type="filepath")
    btn = gr.Button("Generate Speech")
    output_audio = gr.Audio(label="Output Speech", type="filepath")

    btn.click(fn=clone_and_tts, inputs=[text, speaker_wav], outputs=output_audio)

demo.launch()
