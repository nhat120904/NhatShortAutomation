import wave

from google import genai
from google.genai import types


# Set up the wave file to save the output:
def wave_file(filename, pcm, channels=1, rate=24000, sample_width=2):
    with wave.open(filename, "wb") as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(sample_width)
        wf.setframerate(rate)
        wf.writeframes(pcm)


client = genai.Client(api_key="AIzaSyCo9l_kCdlF2Z_trC5gv2hri8SIZKOwasg")

response = client.models.generate_content(
    model="gemini-2.5-flash-preview-tts",
    contents="Have a wonderful day!",
    config=types.GenerateContentConfig(
        response_modalities=["AUDIO"],
        speech_config=types.SpeechConfig(
            voice_config=types.VoiceConfig(
                prebuilt_voice_config=types.PrebuiltVoiceConfig(
                    voice_name="Sulafat",
                )
            )
        ),
    ),
)

data = response.candidates[0].content.parts[0].inline_data.data

file_name = "out_sulafat.wav"
wave_file(file_name, data)  # Saves the file to current directory
