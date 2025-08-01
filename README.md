

* Project Name - Drone Mission Conflict Detection System 

* Project Structure

drone_deconfliction/
│
├── src/
│   ├── models.py                # Data models for waypoints and missions
│   ├── conflict_detector.py     # Interpolation-Based Continuous Conflict Detection
│
├── data/
│   ├── sample_missions.py       # Example missions for testing
│
├── visualizations/
│   ├── visualize_2d_animation.py   # 2D animation with conflict markers
│   ├── visualize_3d .py    # (Bonus) 3D animation with  altitude
│   ├── compare_2d_3d.py     #  compares conflict detection results in 2D vs 3D 
├── visualize_missions.py     # Visualize path 
│
├── test_2d_3d.py                # Demonstrates 2D and 3D data support
├── main_deconfliction_system.py # Final authority for verifying drone mission safety in shared airspace
├── query_test.py                # initial query ytest before takeoff
├── test_2d_3d.py 
├── test_basic.py
├── README.md

* Test Models  and Code Execution commands 

FOlder - root folder -:  drone_deconflication

1. test_basic.py 

shows 
 -> tested 2d waypoints at time instant 
 -> distnace between two waypoints
 -> no of waypoints

 run - python3 test_basic.py

 2. test_2d_3d.py
 shows
 -> 2d subcordinates
 -> 3d subcordinates (by adding z)
 -> check conflicts - gave descision Ttrue /False

 run -> python3 test_2d_3d.py

 3. main_deconfliction_system.py 
 (Final authority for verifying drone mission )
-> Genrates Query for UAV STRATEGIC DECONFLICTION SYSTEM (2D dn 3D Mission)

run-> main_deconfliction_system.py 

OUTPUT :->

================================================================================
UAV STRATEGIC DECONFLICTION SYSTEM - DEMONSTRATION
================================================================================


* Folder - drone_deconflication/visualization 

* visualization

1. visualize_2d_animation.py
- > visualizae 2d Deconflication animation

run -> python3  visualize_2d_animation.py

2. visualize_3d.py
-> Visualize 3d Deconflication animation

run -> python3 visualize_3d.py

3. visualize_mission.py
-> visualize static graphical representation of mission path and conflict

run -> python3 visualize_mission.py

4. compare_2d_3d.py
-> final report and comparision between 2d and 3d subcordinate dron conflicts

run -> python3 compare_2d_3d.py

******************************************************************************
* FOlder - drone_deconflication/data

1. sample_missions.py
- >  Hardcordate mission co-ordinates

run-> Python3 sample_missions.py

Ouput-> sampple co-ordinates

***********************************************************************************
*folder- drone_deconflication/src
1. Conflict_detector.py
 -> conflict detector logic implimentation 







