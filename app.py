from flask import Flask, render_template, request
from video_processing import extract_audio_from_video, extract_text_from_audio, generate_text_from_prompt
from werkzeug.utils import secure_filename

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    # Get the input type from the dropdown menu
    input_type = request.form['input_type']

    if input_type == 'text':
        text_file = request.files['text_file']
        text = text_file.read().decode('utf-8')  # Read the text file content
        generated_text = generate_text_from_prompt(text)
        return generated_text
    elif input_type == 'audio':
        audio_file = request.files['audio']
        audio_path = f"media/audio/{secure_filename(audio_file.filename)}"
        audio_file.save(audio_path)
        text_from_audio = extract_text_from_audio(audio_path)
        generated_text = generate_text_from_prompt(text_from_audio)
        return generated_text
    elif input_type == 'video':
        video_file = request.files['video']
        video_path = f"media/videos/{secure_filename(video_file.filename)}"
        video_file.save(video_path)
        audio_output_path = f"media/audio/{secure_filename(video_file.filename.replace('.mp4', '.mp3'))}"
        extract_audio_from_video(video_path, audio_output_path)
        text_from_audio = extract_text_from_audio(audio_output_path)
        generated_text = generate_text_from_prompt(text_from_audio)
        return generated_text


if __name__ == '__main__':
    app.run(debug=True)



