# AI Smart Pedestrian Crossing System

This project is a Python-based computer vision prototype for a smart pedestrian crossing system. It uses a YOLOv8 model to detect pedestrians and vehicles from a webcam or video file, applies simple crossing-state logic, and renders a live dashboard with detections, crossing status, virtual signals, screenshots, and session reports.

## What It Does

- Detects pedestrians and vehicles in each frame using YOLOv8
- Watches for pedestrians entering the crossing zone
- Delays crossing activation when vehicles are present
- Switches through `IDLE`, `DELAYING`, `ACTIVE`, and `COOLDOWN` states
- Displays a live annotated video feed with:
  - bounding boxes
  - status panel
  - FPS
  - crossing zone highlight
  - virtual pedestrian and vehicle signals
- Saves screenshots and end-of-session reports in `outputs/`

## Project Structure

- [main.py](/Users/akash/ankit-1/main.py): application entry point and video loop
- [detector.py](/Users/akash/ankit-1/detector.py): YOLO-based object detection
- [crossing_logic.py](/Users/akash/ankit-1/crossing_logic.py): pedestrian crossing decision logic
- [visualizer.py](/Users/akash/ankit-1/visualizer.py): UI overlays and visualization
- [stats_tracker.py](/Users/akash/ankit-1/stats_tracker.py): statistics, screenshots, and reports
- [config.py](/Users/akash/ankit-1/config.py): tunable configuration values
- [yolov8n.pt](/Users/akash/ankit-1/yolov8n.pt): local YOLOv8 model weights

## Requirements

- Python 3.10+ recommended
- Webcam access for live camera mode
- macOS, Linux, or Windows with OpenCV-compatible camera support

The project depends on:

- `opencv-python`
- `ultralytics`
- `numpy`

## Run Locally

### 1. Open the project folder

```bash
cd /Users/akash/ankit-1
```

### 2. Create a virtual environment

```bash
python3 -m venv .venv
```

### 3. Install dependencies

```bash
.venv/bin/python -m pip install opencv-python ultralytics numpy
```

### 4. Start the app with webcam input

```bash
python3 main.py --source 0
```

You can also run:

```bash
python3 main.py -- source 0
```

The app now auto-switches into the local `.venv` if you launch it with a system `python3` that does not have `cv2` installed.

### 5. Run with a video file instead of webcam

```bash
python3 main.py --source path/to/video.mp4
```

### 6. Use a different YOLO model

```bash
python3 main.py --source 0 --model yolov8s.pt
```

## Controls

- `Q`: quit
- `S`: save screenshot
- `R`: reset statistics
- `H`: toggle bounding boxes
- `Space`: pause or resume

## Output Files

When the app runs, it can create files inside `outputs/`:

- screenshots as `.png`
- text reports as `.txt`
- statistics as `.json`

## Configuration

You can adjust behavior in [config.py](/Users/akash/ankit-1/config.py), including:

- detection confidence threshold
- frame skipping
- crossing duration
- vehicle delay
- cooldown duration
- crossing zone settings
- UI display settings

## macOS Camera Permission Note

If webcam mode does not start on macOS, make sure camera access is enabled for the terminal app you are using.

1. Open `System Settings > Privacy & Security > Camera`
2. Enable camera access for `Terminal` or `iTerm`
3. Fully close and reopen the terminal app
4. Run the command again

## Current Workflow Summary

1. Open a webcam or video source
2. Detect pedestrians and vehicles with YOLOv8
3. Apply crossing control logic
4. Draw overlays and live status information
5. Track statistics and save reports at shutdown
