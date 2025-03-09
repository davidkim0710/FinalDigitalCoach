import os
import nltk
import logging
from backend.utils import get_temp_dir, get_data_dir, get_video_dir, get_audio_dir, get_output_dir
from backend.utils.env_loader import load_environment

# Load environment variables when helpers are imported
load_environment()

# Configure logger
logger = logging.getLogger(__name__)

# Use absolute path from the current file
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__)) # helpers/
ROOT_DIR = os.path.dirname(CURRENT_DIR)  # tasks/
PARENT_DIR = os.path.dirname(ROOT_DIR)  # backend/

# Initialize NLTK resources with proper error handling
def download_nltk_resources():
    """Download all required NLTK resources"""
    required_resources = [
        "omw-1.4",
        "stopwords",
        "punkt_tab",
        "averaged_perceptron_tagger_eng",
        "wordnet"
    ]
    
    for resource in required_resources:
        try:
            nltk.download(resource, quiet=True)
            logger.debug(f"Downloaded NLTK resource: {resource}")
        except Exception as e:
            logger.warning(f"Failed to download NLTK resource {resource}: {str(e)}")

# Download NLTK resources on module import
download_nltk_resources()