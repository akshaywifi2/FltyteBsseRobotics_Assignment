import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import matplotlib.pyplot as plt
from data.sample_missions import create_sample_missions
from src.conflict_detector import ConflictDetector

def plot_missions(missions, conflicts=None):
    colors = ['r', 'g', 'b', 'm', 'c']
    plt.figure(figsize=(8, 8))

    for idx, mission in enumerate(missions):
        xs = [wp.x for wp in mission.waypoints]
        ys = [wp.y for wp in mission.waypoints]

        plt.plot(xs, ys, marker='o', color=colors[idx % len(colors)], label=mission.drone_id)

        # Label each waypoint with its time
        for wp in mission.waypoints:
            plt.text(wp.x, wp.y, f"{wp.time}s", fontsize=8)

    # If conflict points exist, plot them
    if conflicts:
        for conflict in conflicts:
            # Try to extract time and position from conflict string
            if "time" in conflict and "(" in conflict:
                try:
                    # Parse position from the conflict string
                    part = conflict.split("at time")[-1]
                    time_str, coords = part.split("(")
                    coords = coords.split(")")[0]
                    x_str, y_str = coords.split(",")
                    x = float(x_str)
                    y = float(y_str)
                    plt.scatter(x, y, color='black', marker='x', s=80, label='Conflict')
                except:
                    pass

    plt.xlabel('X (meters)')
    plt.ylabel('Y (meters)')
    plt.title('Drone Missions and Conflicts')
    plt.legend()
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    missions = create_sample_missions()
    detector = ConflictDetector(safety_distance=5.0, time_step=1.0)

    primary = missions[0]
    others = missions[1:]

    conflicts = detector.check_mission_against_others(primary, others)

    # Print conflict messages
    if conflicts:
        print("Conflicts:")
        for c in conflicts:
            print(" -", c)
    else:
        print("No conflicts detected")

    # Visualize
    plot_missions(missions, conflicts)
