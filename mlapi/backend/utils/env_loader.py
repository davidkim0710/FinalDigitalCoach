"""
Environment variable loader utility.
Provides consistent environment loading.
"""
import os
from dotenv import load_dotenv
from backend.utils.logger_config import get_logger

logger = get_logger(__name__)

_ENVIRONMENT_LOADED = False

def find_mlapi_root():
    """
    Find the mlapi root directory by traversing upward from the current file.
    
    Returns:
        str: Path to the mlapi root directory
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Go up the directory tree until we find mlapi directory
    while os.path.basename(current_dir) != "mlapi" and current_dir != "/":
        parent = os.path.dirname(current_dir)
        if parent == current_dir:  # We've hit the root directory
            break
        current_dir = parent
    
    # If we didn't find mlapi, return None
    if os.path.basename(current_dir) != "mlapi":
        logger.warning("Could not find mlapi root directory")
        return None
    
    return current_dir


def load_environment(force_reload=False):
    """
    Load environment variables from the .env file in the mlapi directory.
    
    Args:
        force_reload (bool): If True, reload even if already loaded
        
    Returns:
        bool: True if successfully loaded, False otherwise
    """
    global _ENVIRONMENT_LOADED
    
    # Check if already loaded
    if _ENVIRONMENT_LOADED and not force_reload:
        return True
        
    mlapi_dir = find_mlapi_root()
    if not mlapi_dir:
        logger.error("Failed to find mlapi directory to load environment variables")
        return False
        
    env_path = os.path.join(mlapi_dir, '.env')
    if not os.path.exists(env_path):
        logger.warning(f".env file not found at {env_path}")
        return False
        
    load_dotenv(env_path)
    logger.info(f"Loaded environment variables from {env_path}")
    
    _ENVIRONMENT_LOADED = True
    return True
