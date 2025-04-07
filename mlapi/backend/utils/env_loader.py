"""
Environment variable loader utility.
Provides consistent environment loading from anywhere in the project.
"""

import os
from dotenv import load_dotenv
import logging

logger = logging.getLogger(__name__)

_ENVIRONMENT_LOADED = False

def find_mlapi_root():
    """
    Find the mlapi root directory by traversing upward from the current file.
    
    Returns:
        str: Path to the mlapi root directory
    """
    mlapi_dir = os.path.dirname(os.path.dirname((os.path.abspath(__file__))))
    return mlapi_dir
    

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
