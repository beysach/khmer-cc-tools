from kfa import align, create_session
import librosa

from speech_to_text.transcribe import generate_output_filename


def format_time(milliseconds):
    seconds = milliseconds / 1000
    minutes = seconds / 60
    hours = minutes / 60
    return f"{int(hours):02d}:{int(minutes)%60:02d}:{int(seconds)%60:02d},{int(milliseconds)%1000:03d}"


def generate_srt_from_tuples(tuples):
    srt_content = ""
    for idx, tup in enumerate(tuples, start=1):
        start_time = format_time(tup[1] * 1000)  # Convert seconds to milliseconds
        end_time = format_time(tup[2] * 1000)  # Convert seconds to milliseconds
        text = tup[0]
        srt_content += f"{idx}\n"
        srt_content += f"{start_time} --> {end_time}\n"
        srt_content += f"{text}\n\n"
    return srt_content


def create_srt(text: str, audio_file_input):
    input_file = generate_output_filename(audio_file_input)
    y, sr = librosa.load(audio_file_input.name, sr=16000, mono=True)
    session = create_session(providers=["CUDAExecutionProvider"])
    segments = []
    for alignment in align(y, sr, text, session=session):
        print(alignment)
        segments.append(alignment)

    return generate_srt_from_tuples(segments)
