from dataclasses import dataclass
from typing import List
import math

@dataclass
class waypoint:
    """ x,y,z coordinate where drone needs to go (z is optional for 2D mode)"""
    x: float
    y: float
    z: float = 0.0  # <-- ADD THIS with default value 0 for 2D compatibility
    time: float = 0.0
    
    def distance_to(self, other):
        "calculating euclidean distance in 2D or 3D"
        return math.sqrt(
            (self.x - other.x)**2 + 
            (self.y - other.y)**2 + 
            (self.z - other.z)**2
        )
    
    def distance_to_2d(self, other):
        "calculating euclidean distance in 2D only (ignoring altitude)"
        return math.sqrt(
            (self.x - other.x)**2 + 
            (self.y - other.y)**2
        )
    
    def is_3d(self):
        "check if this waypoint has meaningful altitude data"
        return self.z != 0.0

@dataclass
class Mission:
    """A complete drone mission with multiple waypoints"""
    waypoints: List[waypoint] ## list of all waypoints to visit
    start_time: float # when mission starts in seconds
    end_time: float #when mission must finish in seconds
    drone_id: str = "unknown"
    
    def is_3d_mission(self):
        "check if this mission uses 3D coordinates"
        return any(wp.is_3d() for wp in self.waypoints)