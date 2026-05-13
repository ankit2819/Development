"""
Configuration file - Change settings here without touching other files
"""

# Detection settings
MODEL_PATH = 'yolov8n.pt'  # or 'yolov8s.pt' for better accuracy
CONFIDENCE_THRESHOLD = 0.3  # LOWERED from 0.5 to detect more pedestrians
FRAME_SKIP = 1  # CHANGED: Process EVERY frame (no skipping) to reduce flickering

# Crossing timing (seconds)
CROSSING_DURATION = 15
VEHICLE_DELAY = 3
COOLDOWN_DURATION = 2

# Crossing zone (screen coordinates)
CROSSING_ZONE = {
    'y_min': 100,  # LOWERED to detect pedestrians anywhere
    'x_margin': 300
}

# Visualization settings
UI_SETTINGS = {
    'show_boxes': True,
    'show_fps': True,
    'show_stats_panel': True,
    'theme': 'dark'
}

# Colors (BGR format)
COLORS = {
    'pedestrian': (0, 255, 0),      # Green
    'vehicle': (0, 0, 255),         # Red
    'crossing_active': (0, 255, 0),
    'crossing_inactive': (0, 0, 255),
    'text': (255, 255, 255),
    'warning': (0, 255, 255),
    'background': (0, 0, 0)
}

# Output settings
SAVE_SCREENSHOTS = True
GENERATE_REPORT = True
OUTPUT_DIR = 'outputs'

# Keyboard controls
KEY_QUIT = ord('q')
KEY_SCREENSHOT = ord('s')
KEY_RESET_STATS = ord('r')
KEY_TOGGLE_BOXES = ord('h')
KEY_PAUSE = ord(' ')