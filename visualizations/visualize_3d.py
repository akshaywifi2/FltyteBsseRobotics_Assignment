import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import numpy as np
from data.sample_missions import create_sample_missions_2d, create_sample_missions_3d
from src.conflict_detector import ConflictDetector

def plot_3d_missions(missions, conflicts=None, title="3D Drone Missions"):
    """
    Create interactive 3D plot of drone missions
    """
    fig = go.Figure()
    
    colors = ['red', 'blue', 'green', 'orange', 'purple', 'brown', 'pink']
    
    for idx, mission in enumerate(missions):
        color = colors[idx % len(colors)]
        
        # Extract coordinates
        xs = [wp.x for wp in mission.waypoints]
        ys = [wp.y for wp in mission.waypoints]
        zs = [wp.z for wp in mission.waypoints]
        times = [wp.time for wp in mission.waypoints]
        
        # Plot flight path as line
        fig.add_trace(go.Scatter3d(
            x=xs, y=ys, z=zs,
            mode='lines+markers',
            name=f'{mission.drone_id} Path',
            line=dict(color=color, width=4),
            marker=dict(size=6, color=color),
            text=[f'Time: {t}s' for t in times],
            hovertemplate='<b>%{fullData.name}</b><br>' +
                         'X: %{x}<br>Y: %{y}<br>Z: %{z}<br>%{text}<extra></extra>'
        ))
        
        # Add waypoint labels
        for i, (x, y, z, t) in enumerate(zip(xs, ys, zs, times)):
            fig.add_trace(go.Scatter3d(
                x=[x], y=[y], z=[z],
                mode='text',
                text=[f'WP{i}<br>{t}s'],
                textposition='top center',
                showlegend=False,
                textfont=dict(size=10, color=color)
            ))
    
    # Add conflict markers if provided
    if conflicts:
        conflict_positions = extract_3d_positions_from_conflicts(conflicts)
        if conflict_positions:
            xs_conf, ys_conf, zs_conf = zip(*conflict_positions)
            fig.add_trace(go.Scatter3d(
                x=xs_conf, y=ys_conf, z=zs_conf,
                mode='markers',
                name='Conflicts',
                marker=dict(
                    size=12,
                    color='black',
                    symbol='x',
                    line=dict(width=2, color='red')
                ),
                hovertemplate='<b>CONFLICT ZONE</b><br>' +
                             'X: %{x}<br>Y: %{y}<br>Z: %{z}<extra></extra>'
            ))
    
    # Update layout
    fig.update_layout(
        title=title,
        scene=dict(
            xaxis_title='X (meters)',
            yaxis_title='Y (meters)',
            zaxis_title='Altitude (meters)',
            camera=dict(
                eye=dict(x=1.5, y=1.5, z=1.5)
            )
        ),
        width=900,
        height=700
    )
    
    return fig

def extract_3d_positions_from_conflicts(conflicts):
    """Extract 3D positions from conflict messages"""
    positions = []
    for conflict in conflicts:
        try:
            # Parse conflict string to extract positions
            if "(" in conflict and "vs" in conflict:
                parts = conflict.split("vs")
                if len(parts) >= 2:
                    # Extract first position
                    pos1_part = parts[0].split("(")[-1].split(")")[0]
                    coords1 = [float(x.strip()) for x in pos1_part.split(",")]
                    if len(coords1) >= 3:
                        positions.append((coords1[0], coords1[1], coords1[2]))
        except:
            continue
    return positions
def create_3d_animation(missions, detector, time_range=None):
    """
    Create animated 3D plot showing drone movements over time
    """
    if time_range is None:
        t_min = min(m.start_time for m in missions)
        t_max = max(m.end_time for m in missions)
        time_range = np.arange(t_min, t_max + 1, 1)
    
    frames = []
    colors = ['red', 'blue', 'green', 'orange', 'purple']
    
    for t in time_range:
        frame_data = []
        
        # Add drone positions at time t
        for idx, mission in enumerate(missions):
            pos = detector.get_position_at_time(mission, t)
            if len(pos) >= 3:  # 3D position
                x, y, z = pos
                frame_data.append(go.Scatter3d(
                    x=[x], y=[y], z=[z],
                    mode='markers',
                    name=mission.drone_id,
                    marker=dict(size=10, color=colors[idx % len(colors)]),
                    showlegend=bool(t == time_range[0])  # Convert numpy.bool_ to Python bool
                ))
        
        frames.append(go.Frame(data=frame_data, name=str(t)))
    
    # CREATE THE FIGURE - This was missing!
    fig = go.Figure(data=frames[0].data, frames=frames)
    
    # Add static flight paths
    for idx, mission in enumerate(missions):
        xs = [wp.x for wp in mission.waypoints]
        ys = [wp.y for wp in mission.waypoints]
        zs = [wp.z for wp in mission.waypoints]
        
        fig.add_trace(go.Scatter3d(
            x=xs, y=ys, z=zs,
            mode='lines',
            name=f'{mission.drone_id} Path',
            line=dict(color=colors[idx % len(colors)], width=2, dash='dash'),
            opacity=0.3,
            showlegend=False
        ))
    
    # Add animation controls
    fig.update_layout(
        title="3D Drone Animation",
        scene=dict(
            xaxis_title='X (meters)',
            yaxis_title='Y (meters)',
            zaxis_title='Altitude (meters)',
        ),
        updatemenus=[{
            'type': 'buttons',
            'showactive': False,
            'buttons': [
                {
                    'label': 'Play',
                    'method': 'animate',
                    'args': [None, {'frame': {'duration': 500}, 'fromcurrent': True}]
                },
                {
                    'label': 'Pause',
                    'method': 'animate',
                    'args': [[None], {'frame': {'duration': 0}, 'mode': 'immediate'}]
                }
            ]
        }],
        sliders=[{
            'steps': [
                {
                    'args': [[str(t)], {'frame': {'duration': 0}, 'mode': 'immediate'}],
                    'label': f'{t}s',
                    'method': 'animate'
                } for t in time_range
            ],
            'active': 0,
            'currentvalue': {'prefix': 'Time: '},
            'len': 0.9,
            'x': 0.1,
            'xanchor': 'left',
            'y': 0,
            'yanchor': 'bottom'
        }]
    )
    
    return fig  # Now this line works!
    


if __name__ == "__main__":
    print("Creating 3D visualizations...")
    
    # Test with 3D missions
    missions_3d = create_sample_missions_3d()
    detector = ConflictDetector(safety_distance=5.0, time_step=1.0, mode="3d")
    
    # Check conflicts
    primary = missions_3d[0]
    others = missions_3d[1:]
    conflicts = detector.check_mission_against_others(primary, others)
    
    print(f"Found {len(conflicts)} conflicts")
    
    # Create static 3D plot
    fig1 = plot_3d_missions(missions_3d, conflicts, "3D Drone Missions with Conflicts")
    fig1.show()
    
    # Create animated 3D plot
    print("Creating 3D animation...")
    fig2 = create_3d_animation(missions_3d, detector)
    fig2.show()
    
    print("3D visualizations complete!")