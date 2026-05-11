"""
Handles all visualization and UI drawing
"""

import cv2
import numpy as np
import config
from datetime import datetime

class Visualizer:
    def __init__(self):
        """Initialize visualizer"""
        self.show_boxes = config.UI_SETTINGS['show_boxes']
        self.colors = config.COLORS
        
    def draw_detections(self, frame, pedestrians, vehicles):
        """Draw bounding boxes around detected objects"""
        if not self.show_boxes:
            return frame
        
        # Draw pedestrians (green)
        for ped in pedestrians:
            x1, y1, x2, y2 = ped['bbox']
            cv2.rectangle(frame, (x1, y1), (x2, y2), 
                         self.colors['pedestrian'], 2)
            cv2.putText(frame, f"Person {ped['confidence']:.2f}", 
                       (x1, y1-5), cv2.FONT_HERSHEY_SIMPLEX, 
                       0.5, self.colors['pedestrian'], 2)
        
        # Draw vehicles (red)
        for vehicle in vehicles:
            x1, y1, x2, y2 = vehicle['bbox']
            cv2.rectangle(frame, (x1, y1), (x2, y2), 
                         self.colors['vehicle'], 2)
            cv2.putText(frame, f"Vehicle {vehicle['confidence']:.2f}", 
                       (x1, y1-5), cv2.FONT_HERSHEY_SIMPLEX, 
                       0.5, self.colors['vehicle'], 2)
        
        return frame
    
    def draw_status_panel(self, frame, stats, controller, fps):
        """Draw main status panel with all information"""
        h, w = frame.shape[:2]
        
        # Create overlay for transparency
        overlay = frame.copy()
        
        # Main panel (left side)
        cv2.rectangle(overlay, (10, 10), (450, 200), (0, 0, 0), -1)
        
        # Title
        cv2.putText(frame, "AI SMART PEDESTRIAN CROSSING SYSTEM", (20, 40),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 255, 255), 2)
        
        # Status with color coding
        state_info = controller.get_state_info()
        status_text = f"Status: {state_info['state']}"
        
        if state_info['crossing_active']:
            status_color = self.colors['crossing_active']
        else:
            status_color = self.colors['crossing_inactive']
        
        cv2.putText(frame, status_text, (20, 75),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, status_color, 2)
        
        # Detection counts
        cv2.putText(frame, f"Pedestrians: {stats.get('pedestrians', 0)}", (20, 105),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.55, self.colors['pedestrian'], 2)
        cv2.putText(frame, f"Vehicles: {stats.get('vehicles', 0)}", (20, 130),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.55, self.colors['vehicle'], 2)
        
        # Performance
        if config.UI_SETTINGS['show_fps']:
            cv2.putText(frame, f"FPS: {fps:.1f}", (20, 160),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        
        # Statistics panel (right side)
        if config.UI_SETTINGS['show_stats_panel']:
            stats_x = w - 280
            cv2.rectangle(overlay, (stats_x-10, 10), (w-10, 180), (0, 0, 0), -1)
            
            cv2.putText(frame, "STATISTICS", (stats_x, 35),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 255, 255), 2)
            cv2.putText(frame, f"Events: {stats.get('crossing_events', 0)}", (stats_x, 65),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            cv2.putText(frame, f"Pedestrians: {stats.get('total_crossed', 0)}", (stats_x, 90),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            cv2.putText(frame, f"Vehicles stopped: {stats.get('vehicles_stopped', 0)}", (stats_x, 115),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        
        # Apply transparency
        frame = cv2.addWeighted(overlay, 0.3, frame, 0.7, 0)
        
        # Draw crossing zone
        self._draw_crossing_zone(frame)
        
        # Draw virtual traffic signals
        self._draw_traffic_signals(frame, controller)
        
        # Draw controls legend
        self._draw_controls_legend(frame)
        
        return frame
    
    def _draw_crossing_zone(self, frame):
        """Highlight the pedestrian crossing zone"""
        h, w = frame.shape[:2]
        zone_y = h - 100
        
        # Draw semi-transparent zone
        overlay = frame.copy()
        cv2.rectangle(overlay, (w//2-150, zone_y-30), 
                     (w//2+150, zone_y+30), (0, 255, 255), -1)
        frame = cv2.addWeighted(overlay, 0.2, frame, 0.8, 0)
        
        # Draw border
        cv2.rectangle(frame, (w//2-150, zone_y-30), 
                     (w//2+150, zone_y+30), (0, 255, 255), 2)
        cv2.putText(frame, "CROSSING ZONE", (w//2-60, zone_y-40),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 1)
    
    def _draw_traffic_signals(self, frame, controller):
        """Draw virtual traffic lights"""
        h, w = frame.shape[:2]
        signals = controller.get_signal_status()
        
        # Pedestrian signal (left)
        ped_x, ped_y = 50, h - 80
        color = (0, 255, 0) if signals['pedestrian_color'] == 'green' else (0, 0, 255)
        cv2.circle(frame, (ped_x, ped_y), 25, color, -1)
        cv2.circle(frame, (ped_x, ped_y), 25, (255, 255, 255), 2)
        cv2.putText(frame, signals['pedestrian'], (ped_x-30, ped_y+5),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        
        # Vehicle signal (right)
        vehicle_x, vehicle_y = w - 80, h - 80
        color = (0, 255, 0) if signals['vehicle_color'] == 'green' else (0, 0, 255)
        cv2.circle(frame, (vehicle_x, vehicle_y), 25, color, -1)
        cv2.circle(frame, (vehicle_x, vehicle_y), 25, (255, 255, 255), 2)
        cv2.putText(frame, signals['vehicle'], (vehicle_x-25, vehicle_y+5),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
    
    def _draw_controls_legend(self, frame):
        """Draw keyboard controls at bottom"""
        h, w = frame.shape[:2]
        controls = [
            "Q: Quit", "S: Screenshot", "R: Reset Stats",
            "H: Hide Boxes", "Space: Pause"
        ]
        
        y_pos = h - 20
        x_start = 20
        
        for i, control in enumerate(controls):
            cv2.putText(frame, control, (x_start + i*120, y_pos),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.4, (200, 200, 200), 1)
    
    def toggle_boxes(self):
        """Toggle bounding box visibility"""
        self.show_boxes = not self.show_boxes
        return self.show_boxes