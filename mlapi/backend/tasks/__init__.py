# Import task modules to expose at the package level
from backend.tasks import starPredictions
from backend.tasks import score
from backend.tasks import videoProcess
from backend.tasks import bigFiveScores
from backend.tasks import models
from backend.tasks import helpers
import os
import logging

# Import our utility for temporary file management
from backend.utils import move_misplaced_files
from backend.utils.env_loader import load_environment

# Configure logging
logging.basicConfig(
    level=logging.INFO, 
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Export all task modules
__all__ = [
    "starPredictions",
    "score",
    "videoProcess",
    "bigFiveScores",
    "models",
    "helpers",
]

# Load environment variables when the package is imported
load_environment()

# Try to find and move any misplaced temporary files
move_misplaced_files()

