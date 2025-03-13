from backend.tasks import starPredictions
from backend.tasks import score
from backend.tasks import videoProcess
from backend.tasks import bigFiveScores
from backend.tasks import models
from backend.tasks import helpers
import logging

from backend.utils import move_misplaced_files
from backend.utils.env_loader import load_environment
from backend.utils.logger_config import get_logger
logger = get_logger(__name__)


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

