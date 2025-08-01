import sys
import os
# Add the parent directory to Python path so we can import from src
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.models import Mission, waypoint
from typing import List, Tuple
import math


class ConflictDetector:
    """
    Enhanced conflict detector for both 2D and 3D missions
    """

    def __init__(self, safety_distance: float = 10.0, time_step: float = 1.0, mode: str = "auto"):
        """
        :param safety_distance: Minimum safe distance between drones in meters.
        :param time_step: Interval in seconds to check positions.
        :param mode: "2d", "3d", or "auto" (auto-detect based on mission data)
        """
        self.safety_distance = safety_distance
        self.time_step = time_step
        self.mode = mode

    @staticmethod
    def interpolate_position_3d(wp1: waypoint, wp2: waypoint, t: float) -> Tuple[float, float, float]:
        """
        Linearly interpolate between wp1 and wp2 to get (x, y, z) at time t.
        """
        if wp2.time == wp1.time:
            return (wp1.x, wp1.y, wp1.z)
        ratio = (t - wp1.time) / (wp2.time - wp1.time)
        x = wp1.x + ratio * (wp2.x - wp1.x)
        y = wp1.y + ratio * (wp2.y - wp1.y)
        z = wp1.z + ratio * (wp2.z - wp1.z)
        return (x, y, z)

    @staticmethod
    def interpolate_position_2d(wp1: waypoint, wp2: waypoint, t: float) -> Tuple[float, float]:
        """
        Linearly interpolate between wp1 and wp2 to get (x, y) at time t.
        """
        if wp2.time == wp1.time:
            return (wp1.x, wp1.y)
        ratio = (t - wp1.time) / (wp2.time - wp1.time)
        x = wp1.x + ratio * (wp2.x - wp1.x)
        y = wp1.y + ratio * (wp2.y - wp1.y)
        return (x, y)

    def get_position_at_time(self, mission: Mission, t: float) -> Tuple:
        """
        Get drone position at time t. Returns (x,y) for 2D or (x,y,z) for 3D
        """
        wps = mission.waypoints
        
        # Determine if this is 3D mission
        is_3d = self.mode == "3d" or (self.mode == "auto" and mission.is_3d_mission())
        
        # If before first waypoint
        if t <= wps[0].time:
            return (wps[0].x, wps[0].y, wps[0].z) if is_3d else (wps[0].x, wps[0].y)
        
        # If after last waypoint
        if t >= wps[-1].time:
            return (wps[-1].x, wps[-1].y, wps[-1].z) if is_3d else (wps[-1].x, wps[-1].y)

        # Find segment [wp_i, wp_{i+1}] that contains t
        for i in range(len(wps) - 1):
            if wps[i].time <= t <= wps[i + 1].time:
                if is_3d:
                    return self.interpolate_position_3d(wps[i], wps[i + 1], t)
                else:
                    return self.interpolate_position_2d(wps[i], wps[i + 1], t)

        # Default
        return (wps[-1].x, wps[-1].y, wps[-1].z) if is_3d else (wps[-1].x, wps[-1].y)

    @staticmethod
    def distance_3d(p1: Tuple[float, float, float], p2: Tuple[float, float, float]) -> float:
        return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2 + (p1[2] - p2[2]) ** 2)
    
    @staticmethod
    def distance_2d(p1: Tuple[float, float], p2: Tuple[float, float]) -> float:
        return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)

    def check_conflicts_between_missions(self, mission1: Mission, mission2: Mission) -> List[str]:
        """
        Enhanced conflict detection for both 2D and 3D missions
        """
        conflicts = []
        
        # Determine if we're working in 3D
        is_3d = (self.mode == "3d" or 
                (self.mode == "auto" and (mission1.is_3d_mission() or mission2.is_3d_mission())))
        
        # Find overlapping time window
        start = max(mission1.start_time, mission2.start_time)
        end = min(mission1.end_time, mission2.end_time)

        t = start
        while t <= end:
            pos1 = self.get_position_at_time(mission1, t)
            pos2 = self.get_position_at_time(mission2, t)
            
            if is_3d:
                d = self.distance_3d(pos1, pos2)
                conflict_msg = (
                    f"CONFLICT: {mission1.drone_id} and {mission2.drone_id} "
                    f"too close at time {t:.1f}s "
                    f"({pos1[0]:.1f}, {pos1[1]:.1f}, {pos1[2]:.1f}) vs "
                    f"({pos2[0]:.1f}, {pos2[1]:.1f}, {pos2[2]:.1f}), "
                    f"3D distance {d:.2f}m"
                )
            else:
                d = self.distance_2d(pos1, pos2)
                conflict_msg = (
                    f"CONFLICT: {mission1.drone_id} and {mission2.drone_id} "
                    f"too close at time {t:.1f}s "
                    f"({pos1[0]:.1f}, {pos1[1]:.1f}) vs ({pos2[0]:.1f}, {pos2[1]:.1f}), "
                    f"2D distance {d:.2f}m"
                )

            if d < self.safety_distance:
                conflicts.append(conflict_msg)
            
            t += self.time_step
        
        return conflicts

    def check_mission_against_others(self, primary: Mission, others: List[Mission]) -> List[str]:
        """
        Check primary mission against a list of other missions.
        """
        all_conflicts = []
        for other in others:
            if primary.drone_id != other.drone_id:
                all_conflicts.extend(
                    self.check_conflicts_between_missions(primary, other)
                )
        return all_conflicts


# Test both 2D and 3D conflict detection
if __name__ == "__main__":
    from data.sample_missions import create_sample_missions_2d, create_sample_missions_3d

    print("=== Testing 2D Conflict Detection ===")
    missions_2d = create_sample_missions_2d()
    detector_2d = ConflictDetector(safety_distance=5.0, time_step=1.0, mode="2d")

    primary_2d = missions_2d[0]
    others_2d = missions_2d[1:]

    conflicts_2d = detector_2d.check_mission_against_others(primary_2d, others_2d)
    
    print(f"Checking conflicts for {primary_2d.drone_id}:")
    if conflicts_2d:
        print("2D CONFLICTS DETECTED:")
        for c in conflicts_2d[:3]:  # Show first 3 conflicts
            print(f"  - {c}")
        if len(conflicts_2d) > 3:
            print(f"  ... and {len(conflicts_2d) - 3} more conflicts")
    else:
        print("No 2D conflicts detected!")

    print("\n" + "="*60)
    print("=== Testing 3D Conflict Detection ===")
    missions_3d = create_sample_missions_3d()
    detector_3d = ConflictDetector(safety_distance=5.0, time_step=1.0, mode="3d")

    primary_3d = missions_3d[0]
    others_3d = missions_3d[1:]

    conflicts_3d = detector_3d.check_mission_against_others(primary_3d, others_3d)
    
    print(f"Checking conflicts for {primary_3d.drone_id}:")
    if conflicts_3d:
        print("3D CONFLICTS DETECTED:")
        for c in conflicts_3d[:3]:  # Show first 3 conflicts
            print(f"  - {c}")
        if len(conflicts_3d) > 3:
            print(f"  ... and {len(conflicts_3d) - 3} more conflicts")
    else:
        print("No 3D conflicts detected!")