"""
Main entry point for AI Smart Pedestrian Crossing System
"""

import cv2
import argparse
import sys
import time
import os

from detector import ObjectDetector
from crossing_logic import CrossingController
from visualizer import Visualizer
from stats_tracker import StatsTracker
import config

class PedestrianCrossingSystem:
    def __init__(self):
        """Initialize all system components"""
        print("\n" + "="*50)
        print("AI SMART PEDESTRIAN CROSSING SYSTEM")
        print("="*50)
        
        print("\n[Initializing components...]")
        self.detector = ObjectDetector()
        self.controller = CrossingController()
        self.visualizer = Visualizer()
        self.stats = StatsTracker()
        
        self.paused = False
        self.last_frame = None
        print("[✓] System ready!\n")
    
    def run(self, source=0):
        """Main execution loop"""
        # Open video source
        cap = self._open_source(source)
        if cap is None:
            return
        
        fps_counter = FPSCounter()
        
        print("🎮 Controls:")
        print("   Q - Quit | S - Screenshot | R - Reset Stats")
        print("   H - Toggle Boxes | SPACE - Pause")
        print("-"*50)
        print("🎥 Move in front of camera to test detection!")
        print("-"*50)
        
        while True:
            if not self.paused:
                ret, frame = cap.read()
                if not ret:
                    print("[Video] Restarting...")
                    cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                    continue
                
                # Process frame
                pedestrians, vehicles, annotated = self.detector.detect(frame)
                
                # Update controller
                action, status = self.controller.update(pedestrians, vehicles)
                
                # Update statistics
                self.stats.update(pedestrians, vehicles, action)
                
                # Get current stats for display
                current_stats = self.stats.get_current_stats()
                current_stats['pedestrians'] = len(pedestrians)
                current_stats['vehicles'] = len(vehicles)
                
                # Draw everything
                fps = fps_counter.update()
                display_frame = self.visualizer.draw_detections(annotated, pedestrians, vehicles)
                display_frame = self.visualizer.draw_status_panel(
                    display_frame, current_stats, self.controller, fps
                )
                
                self.last_frame = display_frame
            
            else:
                # Show paused frame
                display_frame = self.last_frame if self.last_frame is not None else frame
                cv2.putText(display_frame, "PAUSED", (display_frame.shape[1]//2-50, 50),
                           cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
            
            # Display
            cv2.imshow('AI Smart Pedestrian Crossing System', display_frame)
            
            # Handle keyboard input
            key = cv2.waitKey(1) & 0xFF
            
            if key == config.KEY_QUIT:
                print("\n[Shutting down...]")
                break
            
            elif key == config.KEY_SCREENSHOT:
                filename = self.stats.save_screenshot(display_frame)
                if filename:
                    print(f"📸 Screenshot saved: {filename}")
            
            elif key == config.KEY_RESET_STATS:
                self.stats.reset()
                print("[Stats] Reset successfully!")
            
            elif key == config.KEY_TOGGLE_BOXES:
                show = self.visualizer.toggle_boxes()
                print(f"[UI] Bounding boxes: {'ON' if show else 'OFF'}")
            
            elif key == config.KEY_PAUSE:
                self.paused = not self.paused
                print(f"[System] {'Paused' if self.paused else 'Resumed'}")
        
        # Cleanup
        cap.release()
        cv2.destroyAllWindows()
        self.stats.save_report()
        print("\n System shutdown complete!")

    def _open_source(self, source):
        """Open video source (webcam or file)"""
        try:
            if isinstance(source, int) or source.isdigit():
                cap = cv2.VideoCapture(int(source))
                source_type = "Webcam"
            else:
                if not os.path.exists(source):
                    print(f" Error: File not found - {source}")
                    return None
                cap = cv2.VideoCapture(source)
                source_type = f"Video: {os.path.basename(source)}"
            
            if not cap.isOpened():
                print(f" Error: Cannot open source - {source}")
                return None
            
            print(f"📹 Source: {source_type}")
            return cap
        
        except Exception as e:
            print(f" Error opening source: {e}")
            return None

class FPSCounter:
    """Simple FPS counter"""
    def __init__(self):
        self.frame_count = 0
        self.start_time = time.time()
        self.fps = 0
    
    def update(self):
        self.frame_count += 1
        if self.frame_count % 30 == 0:
            elapsed = time.time() - self.start_time
            self.fps = 30 / elapsed if elapsed > 0 else 0
            self.start_time = time.time()
        return self.fps

def main():
    parser = argparse.ArgumentParser(
        description='AI Smart Pedestrian Crossing System',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 main.py --source 0              # Use webcam
  python3 main.py --source video.mp4      # Use video file
        """
    )
    
    parser.add_argument('--source', type=str, default='0',
                       help='Video source: 0 for webcam or path to video file')
    parser.add_argument('--model', type=str, default=config.MODEL_PATH,
                       help='YOLO model path (default: yolov8n.pt)')
    
    args = parser.parse_args()
    
    # Update config if different model specified
    if args.model != config.MODEL_PATH:
        config.MODEL_PATH = args.model
    
    # Run system
    system = PedestrianCrossingSystem()
    
    try:
        system.run(source=args.source)
    except KeyboardInterrupt:
        print("\n\n[Interrupted by user]")
        system.stats.save_report()
    except Exception as e:
        print(f"\n Fatal error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()