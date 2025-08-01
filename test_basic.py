from src.models import waypoint,Mission

point1=waypoint(0,0,0)
point2=waypoint(3,4,10)

print(f"point1 :({point1.x},{point1.y}) at time {point1.time}s") #showcase x,y pose at time 
print(f"point2 :({point2.x},{point2.y})at time {point2.time}s")
print(f"distance : {point1.distance_to(point2)}")

mission=Mission(

    waypoints=[point1,point2],
    start_time=0,
    end_time=30,
    drone_id="test_drone"
)
print(f"mission has {len(mission.waypoints)} waypoints")