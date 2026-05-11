"""
Utility functions for the crossing system
"""

import os
import shutil
from datetime import datetime

def setup_project():
    """Create necessary directories and files"""
    
    # Create directories
    dirs = ['outputs', 'logs', 'data']
    for d in dirs:
        os.makedirs(d, exist_ok=True)
    
    print("✓ Project directories created")
    
def clean_outputs():
    """Clean output directory"""
    if os.path.exists('outputs'):
        shutil.rmtree('outputs')
        os.makedirs('outputs')
        print("✓ Outputs cleaned")
    
def get_timestamp():
    """Get formatted timestamp"""
    return datetime.now().strftime("%Y%m%d_%H%M%S")

def log_message(message, level="INFO"):
    """Log message with timestamp"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] [{level}] {message}")

def check_requirements():
    """Check if all required packages are installed"""
    required = ['cv2', 'ultralytics', 'numpy']
    missing = []
    
    for package in required:
        try:
            __import__(package)
        except ImportError:
            missing.append(package)
    
    if missing:
        print(f" Missing packages: {', '.join(missing)}")
        print("Install with: pip install " + " ".join(missing))
        return False
    
    print("✓ All requirements satisfied")
    return True