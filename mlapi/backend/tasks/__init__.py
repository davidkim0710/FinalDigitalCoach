from backend.tasks import starPredictions
from backend.tasks import score
from backend.tasks import videoProcess
from backend.tasks import bigFiveScores
from backend.tasks import models
from backend.tasks import helpers
import logging

from backend.utils import move_misplaced_files
from backend.utils.env_loader import load_environment
# TODO
# from types import EmotionDetectionResult, AudioSentimentResult, Error

logging.basicConfig(
    level=logging.INFO, 
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

__all__ = [
    "starPredictions",
    "score",
    "videoProcess",
    "bigFiveScores",
    "models",
    "helpers",
]

load_environment()

move_misplaced_files()

