from .device_profile import DeviceProfile
from .validators import validate_score_range
from typing import Dict, Any, List

DEFAULT_WEIGHTS: Dict[str, float] = {
    "functionality": 0.30,
    "physical_condition": 0.20,
    "repairability": 0.15,
    "component_recovery": 0.20,
    "remaining_life": 0.10,
    "recyclability": 0.05
}

class ReuseScorer:
    """
    Computes a transparent, configurable, and explainable Reuse Potential Score (0-100)
    for devices based on weighted contribution factors.
    """
    def __init__(self, weights: Dict[str, float] = None, thresholds: Dict[str, str] = None):
        # Enforce configurable weights configuration
        self.weights = weights or DEFAULT_WEIGHTS.copy()
        
        # Verify that weights sum to exactly 100% (1.0)
        total_weight = sum(self.weights.values())
        if not abs(total_weight - 1.0) < 1e-4:
            raise ValueError(f"Scoring weights must sum to exactly 1.0 (100%). Current sum: {total_weight}")

        # Configurable thresholds
        self.thresholds = thresholds or {
            "80": "HIGH REUSE POTENTIAL",
            "60": "MODERATE REUSE POTENTIAL",
            "40": "LOW REUSE POTENTIAL",
            "0": "RECYCLING / RESPONSIBLE DISPOSAL"
        }

    def compute_factor_scores(self, profile: DeviceProfile, analyzed_components: List[dict]) -> Dict[str, float]:
        """
        Calculates distinct scores for each factor from 0 to 100.
        """
        # 1. Functionality Score
        if not profile.power_status:
            func_score = 0.0
        elif not profile.working_status:
            func_score = 30.0
        else:
            # Deduct points for each damaged and missing component
            total_comps = len(analyzed_components)
            damaged_count = len(profile.damaged_components)
            missing_count = len(profile.missing_components)
            deduction = (damaged_count * 15.0) + (missing_count * 10.0)
            func_score = max(40.0, 100.0 - deduction)
            
        # 2. Physical Condition Score
        phys_map = {
            "EXCELLENT": 100.0,
            "GOOD": 80.0,
            "FAIR": 50.0,
            "POOR": 20.0,
            "NON_FUNCTIONAL": 0.0
        }
        phys_score = phys_map.get(profile.physical_condition.upper(), 50.0)

        # 3. Repairability Score
        # High modularity = high score. Deduct for severe damage, add if components are listed as repairable.
        damaged_count = len(profile.damaged_components)
        if damaged_count == 0:
            repair_score = 100.0
        else:
            # Estimate modularity: Laptop/Desktop are modular (80+), Smartphone is harder (60), Tablet (50)
            modularity = 85.0 if profile.category in ("Laptop", "Desktop") else 60.0
            complexity_deduction = damaged_count * 20.0
            
            # Compensation for repairable components
            repairable_count = sum(1 for c in analyzed_components if c["repairable"])
            compensation = repairable_count * 10.0
            
            repair_score = max(10.0, min(100.0, modularity - complexity_deduction + compensation))

        # 4. Component Recovery Score
        # Proportion of components that are reusable out of total components
        total_comps = len(analyzed_components)
        if total_comps == 0:
            comp_score = 50.0
        else:
            reusable_count = sum(1 for c in analyzed_components if c["reusable"])
            comp_score = (reusable_count / total_comps) * 100.0

        # 5. Remaining Useful Life Score
        # Assume standard lifespan is 8 years.
        max_lifespan = 8.0
        remaining_years = max(0.0, max_lifespan - profile.estimated_age)
        remaining_life_score = (remaining_years / max_lifespan) * 100.0

        # 6. Recyclability Score
        # Obsolescence decreases recyclability value (older components have less demand, though base metals exist).
        # Blob/damaged battery reduces recyclability safety.
        has_battery_issue = any(
            c["component_name"].lower() in ("battery", "power adapter") and c["condition"] == "DAMAGED"
            for c in analyzed_components
        )
        base_recycle = 90.0
        if has_battery_issue:
            base_recycle -= 25.0
        if profile.estimated_age > 6:
            base_recycle -= 15.0
            
        recyclability_score = max(30.0, base_recycle)

        return {
            "functionality": validate_score_range(func_score, "functionality"),
            "physical_condition": validate_score_range(phys_score, "physical_condition"),
            "repairability": validate_score_range(repair_score, "repairability"),
            "component_recovery": validate_score_range(comp_score, "component_recovery"),
            "remaining_life": validate_score_range(remaining_life_score, "remaining_life"),
            "recyclability": validate_score_range(recyclability_score, "recyclability")
        }

    def evaluate(self, profile: DeviceProfile, analyzed_components: List[dict]) -> dict:
        """
        Runs scoring calculations and returns a dictionary with scores, weights, contributions, and explanations.
        """
        factor_scores = self.compute_factor_scores(profile, analyzed_components)
        
        weighted_contributions = {}
        total_score = 0.0
        
        for factor, score in factor_scores.items():
            weight = self.weights[factor]
            contribution = score * weight
            weighted_contributions[factor] = round(contribution, 2)
            total_score += contribution

        total_score = round(total_score, 2)
        
        # Categorize level based on thresholds
        reuse_level = "RECYCLING / RESPONSIBLE DISPOSAL"
        sorted_thresholds = sorted([int(k) for k in self.thresholds.keys()], reverse=True)
        for val in sorted_thresholds:
            if total_score >= val:
                reuse_level = self.thresholds[str(val)]
                break

        # Build detailed explainability report
        explanation_lines = [
            f"Overall Reuse Potential Score is {total_score}/100 ({reuse_level}).",
            f"Functionality score ({factor_scores['functionality']}/100) contributes {weighted_contributions['functionality']} points based on working state.",
            f"Physical condition ({factor_scores['physical_condition']}/100) contributes {weighted_contributions['physical_condition']} points based on surface wear.",
            f"Repairability index ({factor_scores['repairability']}/100) contributes {weighted_contributions['repairability']} points.",
            f"Estimated remaining lifespan ({round(max(0.0, 8.0 - profile.estimated_age), 1)} years) contributes {weighted_contributions['remaining_life']} points.",
            f"Component recovery potential contributes {weighted_contributions['component_recovery']} points based on parts harvestable."
        ]
        
        return {
            "total_score": total_score,
            "reuse_level": reuse_level,
            "factor_scores": factor_scores,
            "weights": self.weights,
            "weighted_contributions": weighted_contributions,
            "explanation": " ".join(explanation_lines)
        }
