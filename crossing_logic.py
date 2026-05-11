"""
State machine and decision logic for pedestrian crossing
"""

import time
import config

class CrossingController:
    def __init__(self):
        """Initialize crossing controller"""
        self.crossing_active = False
        self.cross_start_time = 0
        self.pedestrians_waiting = False
        self.vehicle_count = 0
        
        # State tracking
        self.current_state = "IDLE"  # IDLE, DELAYING, ACTIVE, COOLDOWN
        self.state_history = []
        
    def update(self, pedestrians, vehicles):
        """
        Main decision logic
        Returns: (action, status_message)
        """
        self.pedestrians_waiting = len(pedestrians) > 0
        self.vehicle_count = len(vehicles)
        
        current_time = time.time()
        
        # State machine
        if self.current_state == "IDLE":
            return self._handle_idle(pedestrians, vehicles, current_time)
        
        elif self.current_state == "DELAYING":
            return self._handle_delaying(current_time)
        
        elif self.current_state == "ACTIVE":
            return self._handle_active(current_time)
        
        elif self.current_state == "COOLDOWN":
            return self._handle_cooldown(current_time)
        
        return "IDLE", "System ready"
    
    def _handle_idle(self, pedestrians, vehicles, current_time):
        """Normal operation - waiting for pedestrians"""
        if len(pedestrians) == 0:
            return "IDLE", "No pedestrians detected"
        
        # Check if pedestrians are in crossing zone
        in_zone = self._check_crossing_zone(pedestrians)
        
        if not in_zone:
            return "IDLE", "Pedestrians not in crossing zone"
        
        # Decision based on vehicles
        if len(vehicles) > 0:
            self.current_state = "DELAYING"
            self.delay_start_time = current_time
            return "DELAYING", f"Vehicles detected, delaying {config.VEHICLE_DELAY}s"
        else:
            self.current_state = "ACTIVE"
            self.cross_start_time = current_time
            return "ACTIVE", "Crossing activated - Road clear"
    
    def _handle_delaying(self, current_time):
        """Waiting for vehicles to pass"""
        elapsed = current_time - self.delay_start_time
        
        if elapsed >= config.VEHICLE_DELAY:
            self.current_state = "ACTIVE"
            self.cross_start_time = current_time
            return "ACTIVE", "Delay complete - Crossing activated"
        else:
            remaining = config.VEHICLE_DELAY - elapsed
            return "DELAYING", f"Waiting for vehicles ({remaining:.1f}s)"
    
    def _handle_active(self, current_time):
        """Pedestrians are crossing"""
        elapsed = current_time - self.cross_start_time
        
        if elapsed >= config.CROSSING_DURATION:
            self.current_state = "COOLDOWN"
            self.cooldown_start_time = current_time
            return "COOLDOWN", f"Crossing complete - Resetting"
        else:
            remaining = config.CROSSING_DURATION - elapsed
            return "ACTIVE", f"Crossing ({remaining:.1f}s remaining)"
    
    def _handle_cooldown(self, current_time):
        """Short pause after crossing"""
        elapsed = current_time - self.cooldown_start_time
        
        if elapsed >= config.COOLDOWN_DURATION:
            self.current_state = "IDLE"
            return "IDLE", "System reset - Ready for next pedestrian"
        else:
            remaining = config.COOLDOWN_DURATION - elapsed
            return "COOLDOWN", f"Cooldown ({remaining:.1f}s)"
    
    def _check_crossing_zone(self, pedestrians):
        """Check if pedestrians are in the designated crossing zone"""
        for ped in pedestrians:
            center_x, center_y = ped['center']
            frame_center = 320  # Default, will be updated from actual frame
            
            # Simplified check - can be enhanced
            if center_y > config.CROSSING_ZONE['y_min']:
                return True
        return False
    
    def get_state_info(self):
        """Get current state information for display"""
        return {
            'state': self.current_state,
            'crossing_active': self.current_state == "ACTIVE",
            'pedestrians_waiting': self.pedestrians_waiting,
            'vehicle_count': self.vehicle_count
        }
    
    def reset(self):
        """Force reset the system"""
        self.current_state = "IDLE"
        self.crossing_active = False
        print("[Controller] System reset manually")
    
    def get_signal_status(self):
        """Get traffic signal status (virtual)"""
        if self.current_state == "ACTIVE":
            return {
                'pedestrian': 'WALK',
                'pedestrian_color': 'green',
                'vehicle': 'STOP',
                'vehicle_color': 'red'
            }
        else:
            return {
                'pedestrian': 'WAIT',
                'pedestrian_color': 'red',
                'vehicle': 'GO',
                'vehicle_color': 'green'
            }