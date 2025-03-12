import os
import tempfile
import shutil
import glob
import uuid
import logging
from typing import Optional, List

# Configure logging
logger = logging.getLogger(__name__)

# Project name for temp directory naming
PROJECT_NAME = "mlapi"


class TempFileManager:
    """
    Manages temporary files for the application, ensuring consistent locations
    and proper cleanup.
    """

    # Singleton instance
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(TempFileManager, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        """Initialize the temporary directories"""
        # Base temp directory
        self.base_temp_dir = tempfile.gettempdir()

        # Project specific temp directory
        self.project_temp_dir = os.path.join(self.base_temp_dir, PROJECT_NAME)

        # Subdirectories for different file types
        self.data_dir = os.path.join(self.project_temp_dir, "data")
        self.video_dir = os.path.join(self.project_temp_dir, "video")
        self.audio_dir = os.path.join(self.project_temp_dir, "audio")
        self.output_dir = os.path.join(self.project_temp_dir, "output")

        # Create all directories
        for directory in [
            self.project_temp_dir,
            self.data_dir,
            self.video_dir,
            self.audio_dir,
            self.output_dir,
        ]:
            os.makedirs(directory, exist_ok=True)
            logger.debug(f"Ensured directory exists: {directory}")

    def get_temp_dir(self) -> str:
        """Get the base temporary directory for the project"""
        return self.project_temp_dir

    def get_data_dir(self) -> str:
        """Get the data directory for CSV files and other data"""
        return self.data_dir

    def get_video_dir(self) -> str:
        """Get the directory for video files"""
        return self.video_dir

    def get_audio_dir(self) -> str:
        """Get the directory for audio files"""
        return self.audio_dir

    def get_output_dir(self) -> str:
        """Get the directory for processed output files"""
        return self.output_dir

    def get_temp_file_path(
        self, prefix: str = "", suffix: str = "", directory: Optional[str] = None
    ) -> str:
        """
        Generate a unique temporary file path

        Args:
            prefix: Optional prefix for the filename
            suffix: Optional file extension (e.g., '.mp4')
            directory: Specific directory to use, otherwise uses base temp dir

        Returns:
            str: Full path to a new temporary file
        """
        if directory is None:
            directory = self.project_temp_dir

        filename = f"{prefix}{uuid.uuid4()}{suffix}"
        return os.path.join(directory, filename)

    def get_video_path(self, filename: Optional[str] = None) -> str:
        """Get a path for a video file, either with provided name or a new unique name"""
        if filename is None:
            return self.get_temp_file_path(
                prefix="video_", suffix=".mp4", directory=self.video_dir
            )
        return os.path.join(self.video_dir, filename)

    def get_audio_path(self, filename: Optional[str] = None) -> str:
        """Get a path for an audio file, either with provided name or a new unique name"""
        if filename is None:
            return self.get_temp_file_path(
                prefix="audio_", suffix=".mp3", directory=self.audio_dir
            )
        return os.path.join(self.audio_dir, filename)

    def get_output_path(self, filename: Optional[str] = None) -> str:
        """Get a path for an output file, either with provided name or a new unique name"""
        if filename is None:
            return self.get_temp_file_path(
                prefix="output_", suffix="", directory=self.output_dir
            )
        return os.path.join(self.output_dir, filename)

    def cleanup_temp_files(self, directories: Optional[List[str]] = None):
        """
        Clean up temporary files in specified directories

        Args:
            directories: List of directories to clean, or None to clean all
        """
        if directories is None:
            directories = [
                self.data_dir,
                self.video_dir,
                self.audio_dir,
                self.output_dir,
            ]

        for directory in directories:
            try:
                for item in os.listdir(directory):
                    item_path = os.path.join(directory, item)
                    try:
                        if os.path.isdir(item_path):
                            shutil.rmtree(item_path)
                        else:
                            os.remove(item_path)
                        logger.debug(f"Removed temporary item: {item_path}")
                    except OSError as e:
                        logger.error(f"Error removing {item_path}: {str(e)}")
            except OSError as e:
                logger.error(f"Error cleaning directory {directory}: {str(e)}")

    def move_misplaced_files(self):
        """
        Find and move misplaced temporary files to their proper directories
        """
        # Define file patterns and their target directories
        patterns = {
            "*.mp4": self.video_dir,
            "*.mp3": self.audio_dir,
            "*.wav": self.audio_dir,
            "*.csv": self.data_dir,
            "output*.*": self.output_dir,
        }

        # Look in common directories where files might be misplaced
        search_dirs = [
            os.path.dirname(os.path.dirname(self.project_temp_dir)),  # backend dir
            os.path.dirname(
                os.path.dirname(os.path.dirname(self.project_temp_dir))
            ),  # project root
        ]

        for search_dir in search_dirs:
            if not os.path.exists(search_dir):
                continue

            for pattern, target_dir in patterns.items():
                for file_path in glob.glob(os.path.join(search_dir, pattern)):
                    if os.path.isfile(file_path):
                        filename = os.path.basename(file_path)
                        dest_path = os.path.join(target_dir, filename)
                        try:
                            shutil.move(file_path, dest_path)
                            logger.info(
                                f"Moved misplaced file: {file_path} → {dest_path}"
                            )
                        except (OSError, shutil.Error) as e:
                            logger.error(f"Error moving file {file_path}: {str(e)}")


# Create a global instance for easy access
temp_manager = TempFileManager()


# Convenience functions
def get_temp_dir() -> str:
    """Get the base temporary directory for the project"""
    return temp_manager.get_temp_dir()


def get_data_dir() -> str:
    """Get the data directory for CSV files and other data"""
    return temp_manager.get_data_dir()


def get_video_dir() -> str:
    """Get the directory for video files"""
    return temp_manager.get_video_dir()


def get_audio_dir() -> str:
    """Get the directory for audio files"""
    return temp_manager.get_audio_dir()


def get_output_dir() -> str:
    """Get the directory for processed output files"""
    return temp_manager.get_output_dir()


def get_temp_file_path(
    prefix: str = "", suffix: str = "", directory: Optional[str] = None
) -> str:
    """Generate a unique temporary file path"""
    return temp_manager.get_temp_file_path(prefix, suffix, directory)


def get_video_path(filename: Optional[str] = None) -> str:
    """Get a path for a video file"""
    return temp_manager.get_video_path(filename)


def get_audio_path(filename: Optional[str] = None) -> str:
    """Get a path for an audio file"""
    return temp_manager.get_audio_path(filename)


def get_output_path(filename: Optional[str] = None) -> str:
    """Get a path for an output file"""
    return temp_manager.get_output_path(filename)


def cleanup_temp_files(directories: Optional[List[str]] = None):
    """Clean up temporary files"""
    temp_manager.cleanup_temp_files(directories)


def move_misplaced_files():
    """Find and move misplaced temporary files"""
    temp_manager.move_misplaced_files()
