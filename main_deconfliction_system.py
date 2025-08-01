"""
UAV Strategic Deconfliction System - Main Interface
Final authority for verifying drone mission safety in shared airspace
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.models import waypoint, Mission
from src.conflict_detector import ConflictDetector
from data.sample_missions import create_sample_missions_2d, create_sample_missions_3d
from typing import List, Dict, Tuple
import json

class DeconflictionSystem:
    """
    Main deconfliction system - serves as final authority for mission approval
    """
    
    def __init__(self, safety_distance: float = 10.0, time_step: float = 1.0, mode: str = "auto"):
        """
        Initialize the deconfliction system
        
        Args:
            safety_distance: Minimum safe distance between drones (meters)
            time_step: Time resolution for conflict checking (seconds)  
            mode: "2d", "3d", or "auto" for detection mode
        """
        self.detector = ConflictDetector(safety_distance, time_step, mode)
        self.approved_missions = []  # Store approved missions
        self.rejected_missions = []  # Store rejected missions with reasons
        
    def query_mission_safety(self, primary_mission: Mission, other_missions: List[Mission] = None) -> dict:
        """
        PRIMARY QUERY FUNCTION: Check if a mission is safe to execute
        
        Args:
            primary_mission: The mission requesting approval
            other_missions: List of already approved missions to check against
            
        Returns:
            dict: {
                "status": "APPROVED" or "REJECTED",
                "conflicts": [...],
                "recommendations": [...],
                "mission_id": str,
                "timestamp": float
            }
        """
        if other_missions is None:
            other_missions = self.approved_missions
            
        # Detect conflicts
        conflicts = self.detector.check_mission_against_others(primary_mission, other_missions)
        
        # Generate recommendations
        recommendations = self._generate_recommendations(primary_mission, conflicts)
        
        # Make decision
        status = "APPROVED" if len(conflicts) == 0 else "REJECTED"
        
        result = {
            "status": status,
            "mission_id": primary_mission.drone_id,
            "conflicts_detected": len(conflicts),
            "conflicts": conflicts,
            "recommendations": recommendations,
            "safety_distance": self.detector.safety_distance,
            "detection_mode": self.detector.mode
        }
        
        # Store result
        if status == "APPROVED":
            self.approved_missions.append(primary_mission)
            print(f"✅ MISSION APPROVED: {primary_mission.drone_id}")
        else:
            self.rejected_missions.append((primary_mission, result))
            print(f"❌ MISSION REJECTED: {primary_mission.drone_id} - {len(conflicts)} conflicts detected")
            
        return result
    
    def _generate_recommendations(self, mission: Mission, conflicts: List[str]) -> List[str]:
        """Generate recommendations to resolve conflicts"""
        recommendations = []
        
        if not conflicts:
            recommendations.append("Mission approved - no conflicts detected")
            return recommendations
            
        # Analyze conflict patterns
        altitude_conflicts = sum(1 for c in conflicts if "3D distance" in c)
        spatial_conflicts = sum(1 for c in conflicts if "distance" in c)
        
        if altitude_conflicts > 0 and mission.is_3d_mission():
            recommendations.append("Consider altitude adjustment: fly 20-30m higher or lower")
            
        if spatial_conflicts > 0:
            recommendations.append("Consider route modification to avoid congested areas")
            recommendations.append("Consider time delay: start mission 10-15 seconds later")
            
        # Specific recommendations based on conflict locations
        conflict_times = []
        for conflict in conflicts:
            try:
                if "time" in conflict:
                    time_str = conflict.split("time ")[1].split("s")[0]
                    conflict_times.append(float(time_str))
            except:
                continue
                
        if conflict_times:
            avg_conflict_time = sum(conflict_times) / len(conflict_times)
            recommendations.append(f"Peak conflict time around {avg_conflict_time:.1f}s - consider avoiding this window")
            
        return recommendations
    
    def get_system_status(self) -> dict:
        """Get overall system status"""
        return {
            "approved_missions": len(self.approved_missions),
            "rejected_missions": len(self.rejected_missions),
            "total_queries": len(self.approved_missions) + len(self.rejected_missions),
            "approval_rate": len(self.approved_missions) / max(1, len(self.approved_missions) + len(self.rejected_missions)) * 100
        }
    
    def clear_approved_missions(self):
        """Clear all approved missions (for testing)"""
        self.approved_missions = []
        self.rejected_missions = []
        print("System cleared - all missions removed")

def demo_system():
    """Demonstrate the deconfliction system with various scenarios"""
    
    print("="*80)
    print("UAV STRATEGIC DECONFLICTION SYSTEM - DEMONSTRATION")
    print("="*80)
    
    # Initialize system
    system = DeconflictionSystem(safety_distance=5.0, time_step=1.0, mode="auto")
    
    print("\n1. TESTING 2D MISSIONS")
    print("-" * 50)
    missions_2d = create_sample_missions_2d()
    
    for mission in missions_2d:
        print(f"\nQuerying mission: {mission.drone_id}")
        result = system.query_mission_safety(mission)
        
        if result["conflicts"]:
            print("  Conflicts found:")
            for conflict in result["conflicts"][:2]:  # Show first 2
                print(f"    - {conflict}")
        
        if result["recommendations"]:
            print("  Recommendations:")
            for rec in result["recommendations"]:
                print(f"    - {rec}")
    
    print(f"\n2D Mission Results: {system.get_system_status()}")
    
    # Clear and test 3D missions
    system.clear_approved_missions()
    
    print("\n" + "="*50)
    print("2. TESTING 3D MISSIONS")
    print("-" * 50)
    missions_3d = create_sample_missions_3d()
    
    for mission in missions_3d:
        print(f"\nQuerying mission: {mission.drone_id}")
        result = system.query_mission_safety(mission)
        
        if result["conflicts"]:
            print("  Conflicts found:")
            for conflict in result["conflicts"][:2]:  # Show first 2
                print(f"    - {conflict}")
        
        if result["recommendations"]:
            print("  Recommendations:")
            for rec in result["recommendations"]:
                print(f"    - {rec}")
    
    print(f"\n3D Mission Results: {system.get_system_status()}")
    
    print("\n" + "="*80)
    print("DEMONSTRATION COMPLETE")
    print("The system successfully identified conflicts and provided recommendations!")
    print("="*80)

def create_custom_mission_example():
    """Show how to create and test a custom mission"""
    
    print("\n" + "="*60)
    print("CUSTOM MISSION EXAMPLE")
    print("="*60)
    
    # Create a custom mission
    custom_waypoints = [
        waypoint(0, 0, 25, 0),      # Start at 25m altitude
        waypoint(8, 8, 30, 20),     # Middle point at 30m altitude  
        waypoint(15, 5, 20, 40)     # End at 20m altitude
    ]
    
    custom_mission = Mission(
        waypoints=custom_waypoints,
        start_time=0,
        end_time=45,
        drone_id="CUSTOM_UAV_001"
    )
    
    print(f"Created custom mission: {custom_mission.drone_id}")
    print("Mission details:")
    for i, wp in enumerate(custom_mission.waypoints):
        print(f"  Waypoint {i}: ({wp.x}, {wp.y}, {wp.z}) at {wp.time}s")
    
    # Test against existing missions
    system = DeconflictionSystem(safety_distance=8.0, mode="3d")
    existing_missions = create_sample_missions_3d()[:2]  # Use first 2 as existing
    
    print(f"\nTesting against {len(existing_missions)} existing missions...")
    result = system.query_mission_safety(custom_mission, existing_missions)
    
    print(f"\nResult: {result['status']}")
    print(f"Conflicts detected: {result['conflicts_detected']}")
    
    if result["recommendations"]:
        print("Recommendations:")
        for rec in result["recommendations"]:
            print(f"  - {rec}")

if __name__ == "__main__":
    # Run main demonstration
    demo_system()
    
    # Show custom mission example
    create_custom_mission_example()