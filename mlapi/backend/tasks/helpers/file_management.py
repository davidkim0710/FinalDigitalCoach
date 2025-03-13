import os
import shutil
import glob

from backend.utils.filetools import get_temp_dir
from . import (
    ROOT_DIR,
    get_data_dir,
    get_video_dir,
    get_audio_dir,
    get_output_dir,
    get_temp_dir,
)

TEMP_DIR = get_temp_dir()
DATA_DIR = get_data_dir()
VIDEO_DIR = get_video_dir()
AUDIO_DIR = get_audio_dir()
OUTPUT_DIR = get_output_dir()
from backend.utils.logger_config import get_logger
logging = get_logger(__name__)

# TODO: move_cv_files() is not used anywhere. Remove 
def move_cv_files():
    """
    If the data.csv file exists in the root directory, move it to the data directory. If the output
    directory exists in the root directory, move it to the data directory
    """
    data_csv_path = os.path.join(OUTPUT_DIR, "data.csv")
    if os.path.exists(data_csv_path):
        shutil.move(data_csv_path, DATA_DIR)
        logging.info("Moved data.csv file to data directory")

    # Check for misplaced output files in root dir
    root_output_path = os.path.join(ROOT_DIR, "output")
    if os.path.exists(root_output_path):
        shutil.move(root_output_path, TEMP_DIR)
        logging.info("Moved output directory to temporary directory")

    # Also check for any misplaced temporary files in current directory
    for ext in ["*.mp3", "*.mp4", "*.csv"]:
        for file_path in glob.glob(os.path.join(ROOT_DIR, ext)):
            filename = os.path.basename(file_path)
            if ext == "*.mp3" or ext == "*.wav":
                dest = os.path.join(AUDIO_DIR, filename)
            elif ext == "*.mp4":
                dest = os.path.join(VIDEO_DIR, filename)
            else:
                dest = os.path.join(DATA_DIR, filename)
            shutil.move(file_path, dest)
            logging.info(f"Moved misplaced file: {file_path} → {dest}")


def cleanup_temp_files():
    """
    Cleans up all temporary directories
    """
    dirs_to_clean = [DATA_DIR, OUTPUT_DIR, AUDIO_DIR, VIDEO_DIR]

    for dir_path in dirs_to_clean:
        if os.path.exists(dir_path):
            for item in os.listdir(dir_path):
                item_path = os.path.join(dir_path, item)
                try:
                    if os.path.isdir(item_path):
                        shutil.rmtree(item_path)
                    else:
                        os.remove(item_path)
                except OSError as e:
                    print(f"Error while deleting {item_path}: {e}")


