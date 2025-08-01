import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data.sample_missions import create_sample_missions_2d, create_sample_missions_3d
from src.conflict_detector import ConflictDetector
import matplotlib.pyplot as plt

def analyze_conflicts(missions, detector_mode, safety_distance=5.0):
    """Analyze conflicts for given missions and detector mode"""
    detector = ConflictDetector(safety_distance=safety_distance, time_step=1.0, mode=detector_mode)
    
    all_conflicts = []
    mission_pairs = []
    
    # Check all pairs of missions
    for i in range(len(missions)):
        for j in range(i + 1, len(missions)):
            conflicts = detector.check_conflicts_between_missions(missions[i], missions[j])
            if conflicts:
                all_conflicts.extend(conflicts)
                mission_pairs.append((missions[i].drone_id, missions[j].drone_id))
    
    return all_conflicts, mission_pairs

def create_comparison_report():
    """Generate comprehensive comparison between 2D and 3D conflict detection"""
    
    print("="*80)
    print("UAV DECONFLICTION SYSTEM - 2D vs 3D COMPARISON REPORT")
    print("="*80)
    
    # Test 2D missions
    print("\n1. TESTING 2D MISSIONS")
    print("-" * 40)
    missions_2d = create_sample_missions_2d()
    
    # 2D analysis on 2D missions
    conflicts_2d_on_2d, pairs_2d_on_2d = analyze_conflicts(missions_2d, "2d")
    print(f"2D Detector on 2D missions: {len(conflicts_2d_on_2d)} conflicts found")
    
    if conflicts_2d_on_2d:
        print("Sample 2D conflicts:")
        for conflict in conflicts_2d_on_2d[:2]:
            print(f"  - {conflict}")
    
    # Test 3D missions
    print("\n2. TESTING 3D MISSIONS")
    print("-" * 40)
    missions_3d = create_sample_missions_3d()
    
    # 2D analysis on 3D missions (ignoring altitude)
    conflicts_2d_on_3d, pairs_2d_on_3d = analyze_conflicts(missions_3d, "2d")
    print(f"2D Detector on 3D missions: {len(conflicts_2d_on_3d)} conflicts found")
    
    # 3D analysis on 3D missions (considering altitude)
    conflicts_3d_on_3d, pairs_3d_on_3d = analyze_conflicts(missions_3d, "3d")
    print(f"3D Detector on 3D missions: {len(conflicts_3d_on_3d)} conflicts found")
    
    print("\n3. KEY INSIGHTS")
    print("-" * 40)
    
    if len(conflicts_2d_on_3d) > len(conflicts_3d_on_3d):
        print("✅ 3D ADVANTAGE DETECTED!")
        print(f"   - 2D detector found {len(conflicts_2d_on_3d)} conflicts")
        print(f"   - 3D detector found {len(conflicts_3d_on_3d)} conflicts")
        print(f"   - {len(conflicts_2d_on_3d) - len(conflicts_3d_on_3d)} conflicts resolved by altitude separation!")
    else:
        print("ℹ️  Similar conflict levels detected")
    
    # Show example of altitude separation resolving conflicts
    print("\n4. ALTITUDE SEPARATION EXAMPLES")
    print("-" * 40)
    
    # Find mission pairs that conflict in 2D but not in 3D
    resolved_pairs = set(pairs_2d_on_3d) - set(pairs_3d_on_3d)
    if resolved_pairs:
        print("Mission pairs with conflicts resolved by altitude separation:")
        for pair in resolved_pairs:
            print(f"  - {pair[0]} vs {pair[1]}")
    else:
        print("No conflicts were resolved by altitude separation in this example")
    
    print("\n5. MISSION ALTITUDES")
    print("-" * 40)
    for mission in missions_3d:
        altitudes = [wp.z for wp in mission.waypoints]
        print(f"{mission.drone_id}: {min(altitudes):.1f}m - {max(altitudes):.1f}m altitude range")
    
    return {
        'conflicts_2d_on_2d': len(conflicts_2d_on_2d),
        'conflicts_2d_on_3d': len(conflicts_2d_on_3d),
        'conflicts_3d_on_3d': len(conflicts_3d_on_3d),
        'altitude_resolved': len(conflicts_2d_on_3d) - len(conflicts_3d_on_3d)
    }

def create_comparison_chart(results):
    """Create a bar chart comparing conflict detection results"""
    
    categories = ['2D Missions\n(2D Detector)', '3D Missions\n(2D Detector)', '3D Missions\n(3D Detector)']
    conflict_counts = [results['conflicts_2d_on_2d'], results['conflicts_2d_on_3d'], results['conflicts_3d_on_3d']]
    
    plt.figure(figsize=(10, 6))
    bars = plt.bar(categories, conflict_counts, color=['blue', 'orange', 'green'])
    
    # Add value labels on bars
    for bar, count in zip(bars, conflict_counts):
        plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1, 
                str(count), ha='center', va='bottom', fontsize=12, fontweight='bold')
    
    plt.title('Conflict Detection: 2D vs 3D Comparison', fontsize=16, fontweight='bold')
    plt.ylabel('Number of Conflicts Detected', fontsize=12)
    plt.xlabel('Detection Method', fontsize=12)
    
    # Add annotation showing altitude advantage
    if results['altitude_resolved'] > 0:
        plt.annotate(f'{results["altitude_resolved"]} conflicts\nresolved by\naltitude separation', 
                    xy=(1.5, max(conflict_counts) * 0.7), 
                    xytext=(2.2, max(conflict_counts) * 0.8),
                    arrowprops=dict(arrowstyle='->', color='red', lw=2),
                    fontsize=12, ha='center',
                    bbox=dict(boxstyle="round,pad=0.3", facecolor="yellow", alpha=0.7))
    
    plt.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    # Generate comparison report
    results = create_comparison_report()
    
    # Create visualization
    print("\n6. GENERATING COMPARISON CHART")
    print("-" * 40)
    create_comparison_chart(results)
    
    print("\n" + "="*80)
    print("CONCLUSION: 3D conflict detection provides more accurate")
    print("conflict assessment by considering altitude separation!")
    print("="*80)