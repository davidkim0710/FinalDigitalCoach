import os
from typing import Optional
import ffmpeg
import requests
from backend.utils import get_video_path, get_output_path, get_audio_path
from backend.utils.logger_config import get_logger

# Configure logger
logger = get_logger(__name__)


def _download_video(video_url) -> Optional[str]:
    """Download the video from the URL and save it to a temporary file."""
    temp_video_path = get_video_path()  # Generates a unique video path
    response = requests.get(video_url, stream=True)
    if response.status_code == 200:
        with open(temp_video_path, "wb") as f:
            while True:
                chunk = response.raw.read(1024)
                if not chunk:
                    break
                f.write(chunk)
        logger.debug(f"Downloaded video to {temp_video_path}")
        return temp_video_path
    raise Exception("Failed to download video")


def _preprocess_video(video_file, output_name) -> str:
    """Preprocess the video by changing the resolution and frame rate for AssemblyAI."""
    output_file = get_output_path(output_name)
    try:
        input_stream = ffmpeg.input(video_file)  # type: ignore
        audio_stream = input_stream.audio
        video_stream = input_stream.video.filter("fps", fps=30, round="up")
        output_stream = ffmpeg.output(video_stream, audio_stream, output_file)  # type: ignore
        ffmpeg.run(output_stream)  # type: ignore
        logger.debug(f"Preprocessed video saved to {output_file}")
        return output_file
    except Exception as e:
        logger.error(f"Error preprocessing video: {str(e)}")
        raise


def output_video(video_url):
    """Transcribe the video using AssemblyAI. Exported to package."""
    video_file = None
    _output_file = None

    try:
        video_file = _download_video(video_url)
        output_name = "output.mp4"
        _output_file = _preprocess_video(video_file, output_name)
        rename_path = get_audio_path()  # Generates a unique audio path

        content = {"fname": output_name, "rename": os.path.basename(rename_path)}
        return content
    finally:
        # Clean up temporary files
        if video_file and os.path.exists(video_file):
            try:
                os.remove(video_file)
                logger.debug(f"Cleaned up temporary video file: {video_file}")
            except OSError as e:
                logger.error(f"Error deleting temporary video file: {e}")

def output_video(video_path):
    try:
        output_file = _preprocess_video(video_path, "output.mp4")
        rename_path = get_audio_path()  # Generates a unique audio path
        content = {"fname": "output.mp4", "rename": os.path.basename(rename_path)}
        return content
    finally:
        # Clean up temporary files
        if video_path and os.path.exists(video_path):
            try:
                os.remove(video_path)
                logger.debug(f"Cleaned up temporary video file: {video_path}")
            except OSError as e:
                logger.error(f"Error deleting temporary video file: {e}")