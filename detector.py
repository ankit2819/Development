"""
Object detection using YOLO
Handles all AI model operations
"""

import cv2
from ultralytics import YOLO
import config

class ObjectDetector:
    def __init__(self):
        """Initialize YOLO model"""
        print(f"[Detector] Loading model: {config.MODEL_PATH}")
        self.model = YOLO(config.MODEL_PATH)
        self.confidence = config.CONFIDENCE_THRESHOLD
        
        # Class IDs for COCO dataset
        self.PERSON_CLASS = 0
        self.VEHICLE_CLASSES = [2, 3, 5, 7]  # Car, Motorcycle, Bus, Truck
        
    def detect(self, frame):
        """
        Detect objects in frame
        Returns: (pedestrians, vehicles, annotated_frame)
        """
        pedestrians = []
        vehicles = []
        
        # Run inference on EVERY frame (no skipping)
        results = self.model(frame, verbose=False, conf=self.confidence)[0]
        
        if results.boxes is not None:
            for box in results.boxes:
                class_id = int(box.cls[0])
                confidence = float(box.conf[0])
                
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                
                detection = {
                    'bbox': (x1, y1, x2, y2),
                    'confidence': confidence,
                    'center': ((x1 + x2) // 2, (y1 + y2) // 2)
                }
                
                if class_id == self.PERSON_CLASS:
                    pedestrians.append(detection)
                    print(f"🚶 Detected pedestrian! Confidence: {confidence:.2f}")  # Debug print
                elif class_id in self.VEHICLE_CLASSES:
                    detection['class_id'] = class_id
                    vehicles.append(detection)
                    print(f" Detected vehicle! Confidence: {confidence:.2f}")  # Debug print
        
        # Get annotated frame
        annotated_frame = results.plot() if results.boxes is not None else frame
        
        return pedestrians, vehicles, annotated_frame
    
    def get_performance_stats(self):
        """Return model performance metrics"""
        return {
            'model': config.MODEL_PATH,
            'confidence': self.confidence
        }