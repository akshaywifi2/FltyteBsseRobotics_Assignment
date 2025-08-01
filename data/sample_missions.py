import sys
import os
# Add the parent directory to Python path so we can import from src
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.models import waypoint, Mission

def create_sample_missions_2d():
    """Create 2D sample missions (your original data)"""
    
    # Drone 1 waypoints and mission initialization
    drone1_waypoints = [
        waypoint(0, 0, time=0),
        waypoint(5, 5, time=15),
        waypoint(10, 10, time=30)
    ]

    drone1_mission = Mission(
        waypoints=drone1_waypoints,
        start_time=0,
        end_time=35,
        drone_id="DRONE_001_2D"
    )

    # Drone 2 waypoints and mission initialization
    drone2_waypoints = [
        waypoint(10, 0, time=5),
        waypoint(5, 5, time=20),
        waypoint(0, 10, time=35)
    ]

    drone2_mission = Mission(
        waypoints=drone2_waypoints,
        start_time=5,
        end_time=40,
        drone_id="DRONE_002_2D"
    )

    return [drone1_mission, drone2_mission]

def create_sample_missions_3d():
    """Create 3D sample missions with altitude conflicts"""
    
    # Drone 1: Flying at low altitude
    drone1_waypoints = [
        waypoint(0, 0, 10, 0),      # Start at 10m altitude
        waypoint(5, 5, 15, 15),     # Middle at 15m altitude
        waypoint(10, 10, 20, 30)    # End at 20m altitude
    ]

    drone1_mission = Mission(
        waypoints=drone1_waypoints,
        start_time=0,
        end_time=35,
        drone_id="DRONE_001_3D"
    )

    # Drone 2: Flying at high altitude - SAME PATH but different altitude
    drone2_waypoints = [
        waypoint(0, 0, 50, 0),      # Start at 50m altitude
        waypoint(5, 5, 55, 15),     # Middle at 55m altitude  
        waypoint(10, 10, 60, 30)    # End at 60m altitude
    ]

    drone2_mission = Mission(
        waypoints=drone2_waypoints,
        start_time=0,
        end_time=35,
        drone_id="DRONE_002_3D"
    )

    # Drone 3: Conflicting altitude - will cross Drone 1's path
    drone3_waypoints = [
        waypoint(10, 0, 12, 5),     # Start at 12m altitude (close to Drone 1)
        waypoint(5, 5, 17, 20),     # Middle at 17m altitude (CONFLICT!)
        waypoint(0, 10, 22, 35)     # End at 22m altitude
    ]

    drone3_mission = Mission(
        waypoints=drone3_waypoints,
        start_time=5,
        end_time=40,
        drone_id="DRONE_003_3D"
    )

    return [drone1_mission, drone2_mission, drone3_mission]

def create_sample_missions():
    """Original function - returns 2D missions for backward compatibility"""
    return create_sample_missions_2d()

if __name__ == "__main__":
    print("=== 2D Sample Missions ===")
    missions_2d = create_sample_missions_2d()
    
    for mission in missions_2d:
        print(f"\n{mission.drone_id}:")
        print(f"Duration: {mission.start_time}s to {mission.end_time}s")
        print(f"Is 3D: {mission.is_3d_mission()}")
        print(f"Waypoints: {len(mission.waypoints)}")
        for i, wp in enumerate(mission.waypoints):
            print(f"  {i}: ({wp.x},{wp.y}) at time {wp.time}s")
    
    print("\n" + "="*50)
    print("=== 3D Sample Missions ===")
    missions_3d = create_sample_missions_3d()
    
    for mission in missions_3d:
        print(f"\n{mission.drone_id}:")
        print(f"Duration: {mission.start_time}s to {mission.end_time}s")
        print(f"Is 3D: {mission.is_3d_mission()}")
        print(f"Waypoints: {len(mission.waypoints)}")
        for i, wp in enumerate(mission.waypoints):
            print(f"  {i}: ({wp.x},{wp.y},{wp.z}) at time {wp.time}s")