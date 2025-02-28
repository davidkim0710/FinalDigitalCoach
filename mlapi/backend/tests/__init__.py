# Initialize tests package
import os
import sys

# Add parent directory to path to make imports work correctly for tests
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
