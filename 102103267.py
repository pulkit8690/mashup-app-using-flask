import os
import sys
import shutil
from pytube import YouTube
from moviepy.editor import VideoFileClip
from pydub import AudioSegment
from fast_youtube_search import search_youtube

def download_videos(singer_name, num_videos):
    print(f"Downloading {num_videos} videos of {singer_name}...")
    try:
        results = search_youtube([singer_name + " songs"])

        for i, video in enumerate(results):
            if i == num_videos:
                break
            yt = YouTube(f"https://www.youtube.com/watch?v={video['id']}")
            yt.streams.first().download(output_path="temp", filename=f"video_{i+1}.mp4")  # Ensure .mp4 extension
        print("Videos downloaded successfully.")
    except Exception as e:
        print("Error downloading videos:", str(e))
        sys.exit(1)


        
def convert_to_audio(duration):
    print("Converting videos to audio...")
    try:
        for filename in os.listdir("temp"):
            if filename.endswith(".mp4"):
                video_path = os.path.join("temp", filename)
                audio_path = os.path.join("temp", f"{os.path.splitext(filename)[0]}.mp3")
                clip = VideoFileClip(video_path)
                clip = clip.subclip(0, duration)  # Take first 'duration' seconds of video
                audio = clip.audio
                audio.write_audiofile(audio_path)
                clip.close()  # Close the video clip to release resources
        print("Conversion to audio completed.")
    except Exception as e:
        print("Error converting to audio:", str(e))
        sys.exit(1)



def merge_audios(output_file):
    print("Merging audio files...")
    try:
        audio_files = [file for file in os.listdir("temp") if file.endswith(".mp3")]
        combined = None
        for file in audio_files:
            sound = AudioSegment.from_mp3(os.path.join("temp", file))
            if combined is None:
                combined = sound
            else:
                combined += sound
        
        if combined:
            combined.export(output_file, format="mp3")
            print("Audio files merged successfully.")
        else:
            print("No audio files found to merge.")
            sys.exit(1)
    except Exception as e:
        print("Error merging audio files:", str(e))
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: python <program.py> <SingerName> <NumberOfVideos> <AudioDuration> <OutputFileName>")
        sys.exit(1)

    singer_name = sys.argv[1]
    num_videos = int(sys.argv[2])
    audio_duration = int(sys.argv[3])
    output_file = sys.argv[4]

    if num_videos <= 0 or audio_duration <= 0:
        print("Number of videos and audio duration must be positive integers.")
        sys.exit(1)

    if not output_file.endswith(".mp3"):
        output_file += ".mp3"

    try:
        os.makedirs("temp", exist_ok=True)
        download_videos(singer_name, num_videos)
        convert_to_audio(audio_duration)
        merge_audios(output_file)
        shutil.rmtree("temp")
        print("Mashup completed successfully. Output saved as", output_file)
    except Exception as e:
        print("An error occurred:", str(e))
