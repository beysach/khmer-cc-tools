import os
from speech_recognition.audio import AudioData
import subprocess
import speech_recognition as sr
import gradio as gr



def generate_output_filename(input_filename):
    base_name = os.path.splitext(input_filename)[0]  # Get the base name without extension
    output_filename = f"{base_name}_converted.wav"   # Append '_converted.wav'
    return output_filename


def convert_to_wav(input_audio_file: str):
    output_wav_file = generate_output_filename(input_audio_file)
    command = [
        "ffmpeg",
        "-y",
        "-i",
        input_audio_file,
        "-ac",
        "1",
        "-ar",
        "16000",
        output_wav_file,
    ]
    subprocess.run(command, check=True)
    return output_wav_file


# Function to transcribe audio file
def transcribe_audio(input_audio_file):
    recognizer = sr.Recognizer()

    # Load audio file
    with sr.AudioFile(input_audio_file) as source:
        audio_data = recognizer.record(source)

    # Transcribe audio
    try:
        text = recognizer.recognize_google(audio_data, language="km-KH")
        return text, input_audio_file
    except sr.UnknownValueError:
        raise gradio.Error("Speech recognition could not understand audio 💥!", duration=5)
        return "Speech recognition could not understand audio"
    except sr.RequestError as e:
        raise gradio.Error(f"Could not request results from Google Speech Recognition service; {e}", duration=5)
        return f"Could not request results from Google Speech Recognition service; {e}"


# Main function
def transcribe_audio_to_text(input_audio_file):
    gr.Info("Converting to .wav with 16000 Hz sample rate...")
    converted_file = convert_to_wav(input_audio_file)

    gr.Info("Starting transcription process...")
    return  transcribe_audio(converted_file)


    
