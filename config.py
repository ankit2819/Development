"""
Configuration file - Change settings here without touching other files
"""

# Detection settings
MODEL_PATH = "yolov8n.pt"  # or 'yolov8s.pt' for better accuracy
CONFIDENCE_THRESHOLD = 0.5
FRAME_SKIP = 2  # Process every 2nd frame for better performance

# Crossing timing (seconds)
CROSSING_DURATION = 15
VEHICLE_DELAY = 3
COOLDOWN_DURATION = 2

# Crossing zone (screen coordinates)
CROSSING_ZONE = {
    'y_min': 240,  # Bottom half of frame
    'x_margin': 300  # Pixels from center
}

# Visualization settings
UI_SETTINGS = {
    'show_boxes': True,
    'show_fps': True,
    'show_stats_panel': True,
    'theme': 'dark'  # 'dark' or 'light'
}

# Colors (BGR format)
COLORS = {
    'pedestrian': (0, 255, 0),      # Green
    'vehicle': (0, 0, 255),         # Red
    'crossing_active': (0, 255, 0), # Green
    'crossing_inactive': (0, 0, 255), # Red
    'text': (255, 255, 255),        # White
    'warning': (0, 255, 255),       # Yellow
    'background': (0, 0, 0)         # Black
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