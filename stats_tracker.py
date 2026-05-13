"""
Track statistics and generate reports
"""

import cv2  # ← THIS WAS MISSING - ADD THIS LINE
import json
import os
from datetime import datetime
import config

class StatsTracker:
    def __init__(self):
        """Initialize statistics tracking"""
        self.reset()
        self.last_was_active = False  # Add this missing attribute
        
        # Create output directory
        if not os.path.exists(config.OUTPUT_DIR):
            os.makedirs(config.OUTPUT_DIR)
    
    def reset(self):
        """Reset all statistics"""
        self.stats = {
            'crossing_events': 0,
            'total_pedestrians_crossed': 0,
            'total_vehicles_stopped': 0,
            'detection_log': [],
            'session_start': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'peak_pedestrian_count': 0,
            'peak_vehicle_count': 0
        }
    
    def update(self, pedestrians, vehicles, action):
        """Update statistics with new frame data"""
        ped_count = len(pedestrians)
        vehicle_count = len(vehicles)
        
        # Update peaks
        if ped_count > self.stats['peak_pedestrian_count']:
            self.stats['peak_pedestrian_count'] = ped_count
        
        if vehicle_count > self.stats['peak_vehicle_count']:
            self.stats['peak_vehicle_count'] = vehicle_count
        
        # Log crossing events (once per transition to ACTIVE)
        if action == "ACTIVE" and not self.last_was_active:
            self.stats['crossing_events'] += 1
            self.stats['total_pedestrians_crossed'] += ped_count
            if vehicle_count > 0:
                self.stats['total_vehicles_stopped'] += vehicle_count

            self.stats['detection_log'].append({
                'timestamp': datetime.now().strftime("%H:%M:%S"),
                'pedestrians': ped_count,
                'vehicles': vehicle_count,
                'action': 'CROSSING_ACTIVATED'
            })

        self.last_was_active = (action == "ACTIVE")
    
    def get_current_stats(self):
        """Get current statistics for display"""
        return {
            'pedestrians': 0,  # Will be updated by caller
            'vehicles': 0,
            'crossing_events': self.stats['crossing_events'],
            'total_crossed': self.stats['total_pedestrians_crossed'],
            'vehicles_stopped': self.stats['total_vehicles_stopped']
        }
    
    def save_report(self):
        """Generate and save comprehensive report"""
        if not config.GENERATE_REPORT:
            return
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = os.path.join(config.OUTPUT_DIR, f"report_{timestamp}.txt")
        json_file = os.path.join(config.OUTPUT_DIR, f"stats_{timestamp}.json")
        
        # Text report
        with open(report_file, 'w') as f:
            f.write("="*60 + "\n")
            f.write("AI SMART PEDESTRIAN CROSSING SYSTEM\n")
            f.write("PERFORMANCE REPORT\n")
            f.write("="*60 + "\n\n")
            
            f.write(f"Session Start: {self.stats['session_start']}\n")
            f.write(f"Session End: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            f.write("CROSSING STATISTICS\n")
            f.write("-"*40 + "\n")
            f.write(f"Total Crossing Events: {self.stats['crossing_events']}\n")
            f.write(f"Total Pedestrians Crossed: {self.stats['total_pedestrians_crossed']}\n")
            f.write(f"Total Vehicles Stopped: {self.stats['total_vehicles_stopped']}\n\n")
            
            f.write("PEAK VALUES\n")
            f.write("-"*40 + "\n")
            f.write(f"Peak Pedestrians at Once: {self.stats['peak_pedestrian_count']}\n")
            f.write(f"Peak Vehicles at Once: {self.stats['peak_vehicle_count']}\n\n")
            
            f.write("DETECTION LOG\n")
            f.write("-"*40 + "\n")
            for log in self.stats['detection_log'][-20:]:  # Last 20 events
                f.write(f"{log['timestamp']} - {log['action']} "
                       f"(P:{log['pedestrians']}, V:{log['vehicles']})\n")
        
        # JSON for data analysis
        with open(json_file, 'w') as f:
            json.dump(self.stats, f, indent=2)
        
        print(f"\n📊 Reports saved:")
        print(f"   Text: {report_file}")
        print(f"   JSON: {json_file}")
        
        return report_file
    
    def save_screenshot(self, frame):
        """Save screenshot if enabled"""
        if not config.SAVE_SCREENSHOTS:
            return None
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = os.path.join(config.OUTPUT_DIR, f"screenshot_{timestamp}.png")
        cv2.imwrite(filename, frame)  # Now cv2 is defined!
        print(f"📸 Screenshot saved: {filename}")
        return filename