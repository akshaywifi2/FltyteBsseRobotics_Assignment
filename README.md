Drone Mission Conflict Detection System

This project implements a Drone Mission Conflict Detection System to ensure safe operations in shared airspace.
It detects conflicts between drone flight paths using both 2D and 3D trajectories, provides recommendations, and includes visualization tools.
Features

    Continuous conflict detection using interpolation (2D and 3D)

    Safety distance checks between missions

    Recommendations for route changes or time delays

    Visualization tools for:

        2D mission animation

        3D mission visualization and animation

        Comparison of 2D vs 3D conflict detection
        
      Project structure
      
drone_deconfliction/
│
├── src/
│   ├── models.py                # Data models for waypoints and missions
│   ├── conflict_detector.py     # Interpolation-based conflict detection
│
├── data/
│   ├── sample_missions.py       # Example 2D and 3D missions
│
├── visualizations/
│   ├── visualize_2d_animation.py  # 2D animation with conflict markers
│   ├── visualize_3d.py            # 3D animation with altitude
│   ├── compare_2d_3d.py           # Compare 2D vs 3D conflict detection
│   ├── visualize_missions.py      # Static visualization of missions
│
├── main_deconfliction_system.py   # Final authority for mission safety
├── query_test.py                  # Initial mission safety query test
├── test_basic.py                  # Basic waypoint test (2D)`
├── test_2d_3d.py                  # Demonstrates 2D and 3D functionality
└── README.md

How to Run

Navigate to the root folder:

cd drone_deconfliction

1. Basic Test

python3 test_basic.py

    Tests 2D waypoints, calculates distances, and prints mission info.

2. 2D and 3D Mode Test

python3 test_2d_3d.py

    Compares 2D and 3D coordinates and checks conflict detection.

3. Main Deconfliction System

python3 main_deconfliction_system.py

    Runs the UAV Strategic Deconfliction System, approves/rejects missions, and shows recommendations.

Visualization Tools

From visualizations/ folder:

    2D Animation:

python3 visualize_2d_animation.py

3D Visualization and Animation:

python3 visualize_3d.py

Compare 2D vs 3D:

python3 compare_2d_3d.py

Static Visualization:

    python3 visualize_missions.py

Data

From data/:

python3 sample_missions.py

Generates and prints sample 2D and 3D missions for testing.

Core Logic

    conflict_detector.py: Interpolation-based conflict detection algorithm.

    models.py: Defines waypoints and missions.
