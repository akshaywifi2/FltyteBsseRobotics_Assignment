import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from data.sample_missions import create_sample_missions
from src.conflict_detector import ConflictDetector


def get_all_positions(detector, missions, t):
    """Get positions of all drones at time t"""
    positions = []
    for m in missions:
        positions.append(detector.get_position_at_time(m, t))
    return positions


def find_conflicts_at_time(detector, missions, t):
    """Return list of positions where conflicts occur at time t"""
    conflict_positions = []
    for i in range(len(missions)):
        for j in range(i + 1, len(missions)):
            pos1 = detector.get_position_at_time(missions[i], t)
            pos2 = detector.get_position_at_time(missions[j], t)
            dist = detector.distance_2d(pos1, pos2)
            if dist < detector.safety_distance:
                # Use the midpoint of the two positions to mark conflict
                mid_x = (pos1[0] + pos2[0]) / 2
                mid_y = (pos1[1] + pos2[1]) / 2
                conflict_positions.append((mid_x, mid_y))
    return conflict_positions


if __name__ == "__main__":
    missions = create_sample_missions()
    detector = ConflictDetector(safety_distance=5.0, time_step=1.0)

    # Time range for animation
    t_min = min(m.start_time for m in missions)
    t_max = max(m.end_time for m in missions)

    fig, ax = plt.subplots()
    colors = ['r', 'g', 'b', 'm', 'c']

    # Create scatter handles for each drone
    scatters = [ax.plot([], [], 'o', color=c, label=m.drone_id)[0]
                for c, m in zip(colors, missions)]

    # Scatter for conflict markers (black X)
    conflict_scatter, = ax.plot([], [], 'x', color='black', markersize=10, label='Conflict')

    # Draw static planned paths
    for m, c in zip(missions, colors):
        xs = [wp.x for wp in m.waypoints]
        ys = [wp.y for wp in m.waypoints]
        ax.plot(xs, ys, '--', color=c, alpha=0.3)

    def init():
        ax.set_xlim(0, 15)
        ax.set_ylim(0, 35)
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.legend()
        return scatters + [conflict_scatter]

    def update(frame_t):
        positions = get_all_positions(detector, missions, frame_t)

        # Update drone positions
        for scatter, pos in zip(scatters, positions):
            scatter.set_data(pos[0], pos[1])

        # Update conflict markers
        conflicts = find_conflicts_at_time(detector, missions, frame_t)
        if conflicts:
            xs = [c[0] for c in conflicts]
            ys = [c[1] for c in conflicts]
            conflict_scatter.set_data(xs, ys)
        else:
            conflict_scatter.set_data([], [])

        ax.set_title(f"Time = {frame_t:.1f}s")
        return scatters + [conflict_scatter]

    ani = FuncAnimation(
        fig,
        update,
        frames=range(int(t_min), int(t_max) + 1),
        init_func=init,
        blit=False,
        interval=500
    )

    plt.show()
