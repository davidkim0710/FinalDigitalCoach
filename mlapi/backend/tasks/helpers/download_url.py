import urllib.request
import os
import logging
import requests
from backend.utils import get_video_path

# Configure logger
logger = logging.getLogger(__name__)


def download_video_link(url):
    """
    Downloads a video from a given url and saves it to the video directory.
    (Deprecated)

    :param url: The URL of the video you want to download
    :return: the path to the downloaded file.
    """
    dest = get_video_path()
    logger.info(f"Downloading video from {url} to {dest}")
    try:
        urllib.request.urlretrieve(url, dest)
        return dest
    except Exception as e:
        logger.error(f"Error downloading video: {str(e)}")
        return {"errors": e}


def download_video(video_url):
    """
    Downloads a video from a given url and saves it to the video directory.

    :param url: The URL of the video you want to download
    :return: the path to the downloaded file.
    """
    dest = get_video_path()
    
    logger.info(f"Downloading video from {video_url} to {dest}")
    response = requests.get(video_url, stream=True)
    if response.status_code == 200:
        with open(dest, "wb") as f:
            for chunk in response.iter_content(chunk_size=1024):
                f.write(chunk)
        logger.info(f"Video downloaded successfully to {dest}")
        return dest
    else:
        logger.error(f"Failed to download video from {video_url}. Status code: {response.status_code}")
        return None