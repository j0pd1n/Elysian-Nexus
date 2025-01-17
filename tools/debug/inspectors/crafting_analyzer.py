"""
Crafting System Analyzer Tool

This tool provides real-time analysis and debugging of the crafting system.
"""

import json
import time
from typing import Dict, Any, Optional, List, Tuple
from dataclasses import dataclass
from pathlib import Path
from datetime import datetime

@dataclass
class CraftingAttempt:
    timestamp: float
    recipe_id: str
    category: str
    quality_achieved: float
    resources_used: Dict[str, int]
    success: bool
    crafting_time: float
    dimensional_energy: Optional[float] = None
    dimensional_type: Optional[str] = None

@dataclass
class ResourceUsage:
    material_id: str
    quantity_used: int
    recovery_rate: float
    total_cost: float

class CraftingAnalyzer:
    def __init__(self, config_path: str = "config/features/crafting_system.json"):
        self.config_path = Path(config_path)
        self.attempts: List[CraftingAttempt] = []
        self.resource_usage: Dict[str, ResourceUsage] = {}
        self.load_config()
        
    def load_config(self) -> None:
        """Load crafting system configuration."""
        with open(self.config_path) as f:
            self.config = json.load(f)
            
    def record_attempt(self, attempt: CraftingAttempt) -> None:
        """Record a crafting attempt."""
        self.attempts.append(attempt)
        self._update_resource_usage(attempt)
        
    def _update_resource_usage(self, attempt: CraftingAttempt) -> None:
        """Update resource usage statistics."""
        for material_id, quantity in attempt.resources_used.items():
            if material_id not in self.resource_usage:
                self.resource_usage[material_id] = ResourceUsage(
                    material_id=material_id,
                    quantity_used=0,
                    recovery_rate=0.0,
                    total_cost=0.0
                )
            
            usage = self.resource_usage[material_id]
            usage.quantity_used += quantity
            
            # Update recovery rate based on success/failure
            if not attempt.success:
                recovery_rate = self._calculate_resource_recovery(attempt)
                usage.recovery_rate = (
                    (usage.recovery_rate * (usage.quantity_used - quantity) +
                     recovery_rate * quantity) / usage.quantity_used
                )
                
    def _calculate_resource_recovery(self, attempt: CraftingAttempt) -> float:
        """Calculate resource recovery rate for failed attempt."""
        base_rate = self.config["failure_mechanics"]["resource_return"]["base_rate"]
        quality_penalty = (
            self.config["failure_mechanics"]["resource_return"]["quality_penalty"] *
            attempt.quality_achieved
        )
        return max(0.0, base_rate - quality_penalty)
        
    def analyze_success_rates(
        self,
        time_window: Optional[float] = None
    ) -> Dict[str, Any]:
        """Analyze crafting success rates."""
        relevant_attempts = self._get_relevant_attempts(time_window)
        
        if not relevant_attempts:
            return {"error": "No crafting attempts recorded"}
            
        categories = {}
        for attempt in relevant_attempts:
            if attempt.category not in categories:
                categories[attempt.category] = {
                    "total_attempts": 0,
                    "successful_attempts": 0,
                    "average_quality": 0.0,
                    "dimensional_attempts": 0
                }
                
            cat_stats = categories[attempt.category]
            cat_stats["total_attempts"] += 1
            if attempt.success:
                cat_stats["successful_attempts"] += 1
                cat_stats["average_quality"] += attempt.quality_achieved
            if attempt.dimensional_type:
                cat_stats["dimensional_attempts"] += 1
                
        # Calculate averages
        for cat_stats in categories.values():
            if cat_stats["successful_attempts"] > 0:
                cat_stats["average_quality"] /= cat_stats["successful_attempts"]
                
        return {
            "time_period": time_window if time_window else "all_time",
            "categories": categories
        }
        
    def analyze_resource_efficiency(
        self,
        time_window: Optional[float] = None
    ) -> Dict[str, Any]:
        """Analyze resource usage efficiency."""
        relevant_attempts = self._get_relevant_attempts(time_window)
        
        if not relevant_attempts:
            return {"error": "No crafting attempts recorded"}
            
        resource_stats = {}
        for attempt in relevant_attempts:
            for material_id, quantity in attempt.resources_used.items():
                if material_id not in resource_stats:
                    resource_stats[material_id] = {
                        "total_used": 0,
                        "wasted": 0,
                        "successful_crafts": 0
                    }
                    
                stats = resource_stats[material_id]
                stats["total_used"] += quantity
                if not attempt.success:
                    recovered = int(
                        quantity * self._calculate_resource_recovery(attempt)
                    )
                    stats["wasted"] += quantity - recovered
                else:
                    stats["successful_crafts"] += 1
                    
        return {
            "time_period": time_window if time_window else "all_time",
            "resource_stats": resource_stats
        }
        
    def analyze_dimensional_crafting(
        self,
        time_window: Optional[float] = None
    ) -> Dict[str, Any]:
        """Analyze dimensional crafting statistics."""
        relevant_attempts = self._get_relevant_attempts(time_window)
        dimensional_attempts = [
            a for a in relevant_attempts if a.dimensional_type
        ]
        
        if not dimensional_attempts:
            return {"error": "No dimensional crafting attempts recorded"}
            
        dimension_stats = {}
        for attempt in dimensional_attempts:
            dim_type = attempt.dimensional_type
            if dim_type not in dimension_stats:
                dimension_stats[dim_type] = {
                    "total_attempts": 0,
                    "successful_attempts": 0,
                    "average_quality": 0.0,
                    "total_energy_used": 0.0
                }
                
            stats = dimension_stats[dim_type]
            stats["total_attempts"] += 1
            stats["total_energy_used"] += attempt.dimensional_energy or 0
            if attempt.success:
                stats["successful_attempts"] += 1
                stats["average_quality"] += attempt.quality_achieved
                
        # Calculate averages
        for stats in dimension_stats.values():
            if stats["successful_attempts"] > 0:
                stats["average_quality"] /= stats["successful_attempts"]
                stats["energy_per_attempt"] = (
                    stats["total_energy_used"] / stats["total_attempts"]
                )
                
        return {
            "time_period": time_window if time_window else "all_time",
            "dimension_stats": dimension_stats
        }
        
    def _get_relevant_attempts(
        self,
        time_window: Optional[float]
    ) -> List[CraftingAttempt]:
        """Get attempts within the specified time window."""
        if not time_window:
            return self.attempts
            
        current_time = time.time()
        return [
            a for a in self.attempts
            if current_time - a.timestamp <= time_window
        ]
        
    def get_recommendations(self) -> Dict[str, str]:
        """Generate crafting recommendations based on analysis."""
        success_analysis = self.analyze_success_rates()
        resource_analysis = self.analyze_resource_efficiency()
        dimensional_analysis = self.analyze_dimensional_crafting()
        
        recommendations = {
            "focus_areas": self._recommend_focus_areas(success_analysis),
            "resource_management": self._recommend_resource_usage(resource_analysis),
            "dimensional_crafting": self._recommend_dimensional_approach(
                dimensional_analysis
            )
        }
        
        return recommendations
        
    def _recommend_focus_areas(self, analysis: Dict[str, Any]) -> str:
        """Recommend which crafting areas to focus on."""
        if "error" in analysis:
            return "Insufficient data for recommendations"
            
        lowest_success = ("none", 1.0)
        for category, stats in analysis["categories"].items():
            success_rate = (
                stats["successful_attempts"] / stats["total_attempts"]
                if stats["total_attempts"] > 0 else 0.0
            )
            if success_rate < lowest_success[1]:
                lowest_success = (category, success_rate)
                
        return f"Focus on improving {lowest_success[0]} crafting techniques"
        
    def _recommend_resource_usage(self, analysis: Dict[str, Any]) -> str:
        """Recommend resource usage improvements."""
        if "error" in analysis:
            return "Insufficient data for recommendations"
            
        highest_waste = ("none", 0.0)
        for material, stats in analysis["resource_stats"].items():
            waste_rate = stats["wasted"] / stats["total_used"]
            if waste_rate > highest_waste[1]:
                highest_waste = (material, waste_rate)
                
        return f"Work on reducing waste of {highest_waste[0]}"
        
    def _recommend_dimensional_approach(self, analysis: Dict[str, Any]) -> str:
        """Recommend dimensional crafting improvements."""
        if "error" in analysis:
            return "Insufficient data for dimensional crafting recommendations"
            
        return "Dimensional crafting recommendations based on analysis"
        
    def log_state(self, log_path: Optional[str] = None) -> None:
        """Log current crafting analysis to file."""
        if not log_path:
            log_path = f"logs/debug/crafting_analysis_{int(time.time())}.json"
            
        if not self.attempts:
            return
            
        analysis_data = {
            "timestamp": datetime.now().isoformat(),
            "success_rates": self.analyze_success_rates(),
            "resource_efficiency": self.analyze_resource_efficiency(),
            "dimensional_crafting": self.analyze_dimensional_crafting(),
            "recommendations": self.get_recommendations()
        }
        
        with open(log_path, 'w') as f:
            json.dump(analysis_data, f, indent=2)
            
def main():
    """Main function for running the analyzer independently."""
    analyzer = CraftingAnalyzer()
    
    # Example usage
    attempt = CraftingAttempt(
        timestamp=time.time(),
        recipe_id="weapon_sword_basic",
        category="weaponry",
        quality_achieved=0.75,
        resources_used={"iron": 5, "wood": 2},
        success=True,
        crafting_time=8.0
    )
    
    analyzer.record_attempt(attempt)
    
    # Generate and save analysis
    analyzer.log_state()
    
if __name__ == "__main__":
    main() 