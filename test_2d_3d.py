from src.models import waypoint, Mission

# Test 2D waypoints (backward compatible)
print("=== 2D Mode (like before) ===")
point2d_1 = waypoint(0, 0, time=0)      # z defaults to 0
point2d_2 = waypoint(3, 4, time=10)     # z defaults to 0

print(f"2D point1: ({point2d_1.x},{point2d_1.y}) at time {point2d_1.time}s")
print(f"2D point2: ({point2d_2.x},{point2d_2.y}) at time {point2d_2.time}s")
print(f"2D distance: {point2d_1.distance_to_2d(point2d_2):.2f} meters")
print(f"3D distance: {point2d_1.distance_to(point2d_2):.2f} meters")

mission_2d = Mission(
    waypoints=[point2d_1, point2d_2],
    start_time=0,
    end_time=30,
    drone_id="drone_2d"
)
print(f"Is 3D mission? {mission_2d.is_3d_mission()}")

print("\n=== 3D Mode (new feature) ===")
# Test 3D waypoints
point3d_1 = waypoint(0, 0, 10, 0)       # At altitude 10m
point3d_2 = waypoint(3, 4, 20, 10)      # At altitude 20m

print(f"3D point1: ({point3d_1.x},{point3d_1.y},{point3d_1.z}) at time {point3d_1.time}s")
print(f"3D point2: ({point3d_2.x},{point3d_2.y},{point3d_2.z}) at time {point3d_2.time}s")
print(f"2D distance: {point3d_1.distance_to_2d(point3d_2):.2f} meters")
print(f"3D distance: {point3d_1.distance_to(point3d_2):.2f} meters")

mission_3d = Mission(
    waypoints=[point3d_1, point3d_2],
    start_time=0,
    end_time=30,
    drone_id="drone_3d"
)
print(f"Is 3D mission? {mission_3d.is_3d_mission()}")