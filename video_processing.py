# video_processing.py

from moviepy.editor import VideoFileClip
import subprocess
import google.generativeai as genai


def extract_audio_from_video(video_path, audio_output_path):
    """Extracts audio from a video and saves it to an MP3 file."""
    try:
        video_clip = VideoFileClip(video_path)
        audio_clip = video_clip.audio
        audio_clip.write_audiofile(audio_output_path)
        print(f"Audio extracted successfully and saved to: {audio_output_path}")
    except Exception as e:
        print(f"Error extracting audio: {e}")


def extract_text_from_audio(audio_file_path):
    """Extracts text from an MP3 file using Whisper."""
    try:
        command = f"whisper '{audio_file_path}' --model large"
        process = subprocess.run(command, shell=True, check=True, text=True, capture_output=True)
        output = process.stdout
        lines = output.split('\n')

        timestamps = []
        texts = []
        for line in lines:
            if '] ' in line:
                timestamp, text = line.split('] ', 1)
                timestamp = timestamp[1:]
                timestamps.append(timestamp)
                texts.append(text)

        text_string = ' '.join(texts)
        return text_string
    except Exception as e:
        print(f"Error extracting text from audio: {e}")
        return ""


def generate_text_from_prompt(prompt):
    genai.configure(api_key='AIzaSyAass-uhtkfBxUWwOY4yvrhYaqGrfrEN8I')
    model = genai.GenerativeModel('gemini-pro')

    instruction1 = '''Analyze the given conversation data and classify it as either "toxic" or "non-toxic".'''
    instruction2 = '''Only  if the conversation is "toxic", provide a detailed extraction of the toxic content.'''
    text_prompt = prompt + " " + instruction1 + " " + instruction2
    try:
        response = model.generate_content(text_prompt)
        return response.text
    except Exception as e:
        print(f"Error generating text: {e}")
        return ""
