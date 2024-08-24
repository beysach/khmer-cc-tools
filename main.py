
import gradio as gr
from speech_to_text.transcribe import transcribe_audio_to_text
from khmer_force_aligner import create_srt

def download_srt(cc_text: str):
    file_path = "downloaded_text.srt"
    with open(file_path, "w") as file:
        file.write(cc_text)
    return file_path


def render_ui():
    with gr.Blocks(theme=gr.themes.Soft(font=[gr.themes.GoogleFont("Noto Sans Khmer"), "Arial", "sans-serif"]), title='Khmer CC tools') as app:
        gr.HTML("<h1> [facebook.com/kleykley.dev]  Khmer CC tools </h1>")
        with gr.Tabs():
            with gr.Row():
                with gr.Column():
                    upload_file = gr.File(label='Audio file', file_types=['audio', '.mp4'])
                    audio_output = gr.Audio(label='Audio Output')
                    button_transcribe = gr.Button('ប្រតិចារិក 👂', variant='primary')

                with gr.Column():
                    transcript_text = gr.Text(label='Transcript Text', info='ddd',interactive=True)
                    button_to_srt = gr.Button('ទៅអក្សររត់',variant='primary')
                    cc_text = gr.Text(label='លទ្ធផល​', info='closed caption result')

                    button_download = gr.Button('ទាញយក')

                    
                button_transcribe.click(transcribe_audio_to_text, inputs=[upload_file], outputs=[transcript_text,audio_output])
                button_to_srt.click(create_srt, inputs=[transcript_text, upload_file], outputs=[cc_text])
                button_download.click(download_srt, inputs=[cc_text], outputs=gr.File(label='Download'))
                # with gr.Column():
                #     video = gr.Video()
                # but0.click(fn=text_to_speech_ai, inputs=[model, text, speaker], outputs=[audio])
    app.queue().launch(share=True)


if __name__ == '__main__':
    render_ui()

