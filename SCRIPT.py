from pytube import Playlist, YouTube
from moviepy.editor import *
import os
import re

def sanitize_filename(filename):
    # Replace any non-alphanumeric characters with underscores
    return re.sub(r'\W+', '_', filename)

def download_playlist_as_mp3(playlist_url, output_root_folder):
    # Get the playlist ID from the URL
    playlist_id = playlist_url.split("list=")[1]
    
    # Create the output folder for the playlist
    output_playlist_folder = os.path.join(output_root_folder, sanitize_filename(playlist_id))
    if not os.path.exists(output_playlist_folder):
        os.makedirs(output_playlist_folder)
    
    # Load the playlist
    playlist = Playlist(playlist_url)
    
    # Iterate over each video in the playlist
    for video_url in playlist.video_urls:
        try:
            # Get the YouTube video
            video = YouTube(video_url)
            
            # Get the first three words of the video title
            title_words = video.title.split()[:3]
            title = " ".join(title_words)
            
            # Get the audio stream
            audio_stream = video.streams.filter(only_audio=True).first()
            
            # Download the audio
            audio_file_path = os.path.join(output_playlist_folder, f"{sanitize_filename(title)}.mp3")
            audio_stream.download(output_playlist_folder)
            
            # Convert the downloaded video to audio
            video_path = os.path.join(output_playlist_folder, f"{sanitize_filename(title)}.mp4") # Temporary mp4 file
            audio_clip = AudioFileClip(audio_file_path.encode('utf-8'))
            audio_clip.write_videofile(video_path.encode('utf-8'), codec='libx264', audio_codec='aac')
            audio_clip.close()  # Close the audio clip
            os.remove(audio_file_path)  # Remove the original audio file
            
            # Rename the converted video to mp3
            mp3_file_path = os.path.join(output_playlist_folder, f"{sanitize_filename(title)}.mp3")
            os.rename(video_path, mp3_file_path)
            
            # Encode title to ASCII, ignoring any characters that can't be encoded
            printable_title = title.encode('ascii', 'ignore').decode('ascii')
            
            print(f"Downloaded and converted {printable_title} to MP3")
        
        except Exception as e:
            printable_video_url = video_url.encode('ascii', 'ignore').decode('ascii')
            print(f"Error downloading {printable_video_url}: {str(e)}")

# Example usage
playlist_url = "https://youtube.com/playlist?list=PLV5U_eQm8CS-6tvHVHQpl7ISd_yEIP-2o&si=R29C73tZlCnUtKvn"
output_root_folder = "mp3D"

download_playlist_as_mp3(playlist_url, output_root_folder)
