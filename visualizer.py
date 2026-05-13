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
        self.last_frame_cache = None  # Cache for stable display
        
    def draw_detections(self, frame, pedestrians, vehicles):
        """Draw bounding boxes around detected objects"""
        if not self.show_boxes:
            return frame
        
        # Draw pedestrians (green)
        for ped in pedestrians:
            x1, y1, x2, y2 = ped['bbox']
            # Draw filled rectangle with transparency
            overlay = frame.copy()
            cv2.rectangle(overlay, (x1, y1), (x2, y2), self.colors['pedestrian'], 2)
            cv2.addWeighted(overlay, 0.7, frame, 0.3, 0, frame)
            
            # Add label
            label = f"Pedestrian {ped['confidence']:.2f}"
            label_size = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 2)[0]
            cv2.rectangle(frame, (x1, y1-25), (x1+label_size[0], y1), self.colors['pedestrian'], -1)
            cv2.putText(frame, label, (x1, y1-5), cv2.FONT_HERSHEY_SIMPLEX, 
                       0.5, (0, 0, 0), 2)
        
        # Draw vehicles (red)
        for vehicle in vehicles:
            x1, y1, x2, y2 = vehicle['bbox']
            overlay = frame.copy()
            cv2.rectangle(overlay, (x1, y1), (x2, y2), self.colors['vehicle'], 2)
            cv2.addWeighted(overlay, 0.7, frame, 0.3, 0, frame)
            
            label = f"Vehicle {vehicle['confidence']:.2f}"
            label_size = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 2)[0]
            cv2.rectangle(frame, (x1, y1-25), (x1+label_size[0], y1), self.colors['vehicle'], -1)
            cv2.putText(frame, label, (x1, y1-5), cv2.FONT_HERSHEY_SIMPLEX, 
                       0.5, (255, 255, 255), 2)
        
        return frame
    
    def draw_status_panel(self, frame, stats, controller, fps):
        """Draw main status panel with all information"""
        h, w = frame.shape[:2]
        
        # Create a clean overlay (not transparent to reduce flickering)
        overlay = frame.copy()
        
        # Main panel (left side) - solid background for stability
        cv2.rectangle(overlay, (10, 10), (450, 200), (0, 0, 0), -1)
        
        # Title - bright yellow
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
        
        # Detection counts - HIGHLIGHTED in bright green/red
        ped_count = stats.get('pedestrians', 0)
        vehicle_count = stats.get('vehicles', 0)
        
        cv2.putText(frame, f"👥 PEDESTRIANS: {ped_count}", (20, 110),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, self.colors['pedestrian'], 3)
        cv2.putText(frame, f"🚗 VEHICLES: {vehicle_count}", (20, 145),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, self.colors['vehicle'], 3)
        
        # Performance
        if config.UI_SETTINGS['show_fps']:
            cv2.putText(frame, f"FPS: {fps:.1f}", (20, 180),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        
        # Apply the overlay (less transparency = less flickering)
        frame = cv2.addWeighted(overlay, 0.2, frame, 0.8, 0)
        
        # Statistics panel (right side)
        if config.UI_SETTINGS['show_stats_panel']:
            stats_x = w - 280
            cv2.rectangle(overlay, (stats_x-10, 10), (w-10, 180), (0, 0, 0), -1)
            frame = cv2.addWeighted(overlay, 0.2, frame, 0.8, 0)
            
            cv2.putText(frame, "STATISTICS", (stats_x, 35),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 255, 255), 2)
            cv2.putText(frame, f"Events: {stats.get('crossing_events', 0)}", (stats_x, 65),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            cv2.putText(frame, f"Pedestrians Crossed: {stats.get('total_crossed', 0)}", (stats_x, 90),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            cv2.putText(frame, f"Vehicles Stopped: {stats.get('vehicles_stopped', 0)}", (stats_x, 115),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        
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
        frame = cv2.addWeighted(overlay, 0.3, frame, 0.7, 0)
        
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
        cv2.circle(frame, (ped_x, ped_y), 30, color, -1)
        cv2.circle(frame, (ped_x, ped_y), 30, (255, 255, 255), 3)
        cv2.putText(frame, signals['pedestrian'], (ped_x-35, ped_y+5),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        
        # Vehicle signal (right)
        vehicle_x, vehicle_y = w - 80, h - 80
        color = (0, 255, 0) if signals['vehicle_color'] == 'green' else (0, 0, 255)
        cv2.circle(frame, (vehicle_x, vehicle_y), 30, color, -1)
        cv2.circle(frame, (vehicle_x, vehicle_y), 30, (255, 255, 255), 3)
        cv2.putText(frame, signals['vehicle'], (vehicle_x-30, vehicle_y+5),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
    
    def _draw_controls_legend(self, frame):
        """Draw keyboard controls at bottom"""
        h, w = frame.shape[:2]
        controls = [
            "Q: Quit", "S: Screenshot", "R: Reset Stats",
            "H: Hide Boxes", "Space: Pause"
        ]
        
        y_pos = h - 20
        x_start = 20
        
        # Dark background for controls
        cv2.rectangle(frame, (10, h-40), (w-10, h-10), (0, 0, 0), -1)
        
        for i, control in enumerate(controls):
            cv2.putText(frame, control, (x_start + i*130, y_pos),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.4, (200, 200, 200), 1)
    
    def toggle_boxes(self):
        """Toggle bounding box visibility"""
        self.show_boxes = not self.show_boxes
        return self.show_boxes