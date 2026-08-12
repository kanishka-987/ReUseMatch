from .device_profile import DeviceProfile
from typing import List, Dict, Any

class ComponentRecoveryDetail:
    def __init__(
        self,
        component_name: str,
        potential_score: float,
        potential_level: str,
        confidence_score: float,
        confidence_level: str,
        assessment_status: str,
        reason: str
    ):
        self.component_name = component_name
        self.potential_score = potential_score
        self.potential_level = potential_level
        self.confidence_score = confidence_score
        self.confidence_level = confidence_level
        self.assessment_status = assessment_status
        self.reason = reason

    def to_dict(self) -> dict:
        return {
            "component": self.component_name,
            "potential_score": self.potential_score,
            "potential_level": self.potential_level,
            "confidence_score": self.confidence_score,
            "confidence_level": self.confidence_level,
            "assessment_status": self.assessment_status,
            "reason": self.reason
        }

class ComponentRecoveryEstimator:
    """
    Analyzes and estimates the salvage/recovery potential of individual components
    when a device is non-functional or cannot power on.
    """
    CATEGORY_COMPONENTS: Dict[str, List[str]] = {
        "Laptop": [
            "RAM", "SSD", "HDD", "Display", "Keyboard", 
            "Touchpad", "Wi-Fi module", "Camera", "Speakers", 
            "Charger/adapter", "Battery", "Motherboard"
        ],
        "Desktop": ["RAM", "CPU", "GPU", "Storage", "Power supply", "Motherboard", "Case"],
        "Monitor": ["Display panel", "Stand", "Power adapter", "Control board", "Ports"],
        "Smartphone": ["Display screen", "Battery", "Camera module", "Logic board", "Speaker"],
        "Tablet": ["Display screen", "Battery", "Logic board", "Charger"],
    }

    def __init__(self):
        pass

    def estimate_recovery(self, profile: DeviceProfile) -> List[dict]:
        """
        Runs component recovery estimations based on age, specifications, physical/functional condition,
        power status, and visible damage reports.
        """
        category = profile.category
        components = self.CATEGORY_COMPONENTS.get(category, ["Main board", "Chassis", "Power supply"])
        
        damaged = {c.lower().strip() for c in profile.damaged_components}
        missing = {c.lower().strip() for c in profile.missing_components}
        verified = {c.lower().strip() for c in profile.verified_components}
        
        # Spec key checking
        known_specs = {k.lower().strip(): v for k, v in profile.known_components.items()}

        results = []
        for comp in components:
            comp_lower = comp.lower().strip()
            
            # 1. Base Score calculation (calibrated to hit user's target examples)
            if comp == "RAM":
                base_score = 90.0
            elif comp in ("SSD", "HDD", "Storage", "CPU", "GPU", "Storage"):
                base_score = 86.0
            elif comp in ("Display", "Display panel", "Display screen"):
                base_score = 78.0
            elif comp == "Battery":
                base_score = 48.0
            elif comp in ("Motherboard", "Logic board", "Control board", "Main board"):
                base_score = 28.0
            elif comp in ("Stand", "Case", "Chassis", "Ports"):
                base_score = 80.0
            else:
                base_score = 70.0

            # 2. Adjustments based on Age (electronics degrade slowly; use 2.0 per year)
            age_deduction = min(40.0, profile.estimated_age * 2.0)
            score = base_score - age_deduction

            # 3. Adjustments for Physical Condition (highly affects components)
            phys_cond_map = {
                "EXCELLENT": 10.0,
                "GOOD": 5.0,
                "FAIR": -5.0,
                "POOR": -20.0,
                "NON_FUNCTIONAL": -40.0
            }
            score += phys_cond_map.get(profile.physical_condition.upper(), -5.0)

            # 4. Confidence Base Score
            confidence = 85.0
            
            # Deduct confidence if the device cannot power on or is not functional
            has_power_issue = not profile.power_status
            has_functional_issue = not profile.working_status
            
            if has_power_issue or has_functional_issue:
                confidence -= 20.0  # Cannot verify functional status

            # Increase confidence and potential score if component specifications are explicitly known
            is_known = False
            spec_detail = ""
            for k_spec, v_spec in known_specs.items():
                if k_spec in comp_lower or comp_lower in k_spec:
                    confidence += 10.0
                    score += 5.0  # Spec bonus
                    is_known = True
                    spec_detail = v_spec
                    break

            # Cap scores
            score = max(0.0, min(100.0, score))
            confidence = max(0.0, min(100.0, confidence))

            # 5. Overrides for Missing/Damaged/Verified states
            is_missing = comp_lower in missing
            is_damaged = comp_lower in damaged
            is_verified = comp_lower in verified

            if is_missing:
                score = 0.0
                confidence = 0.0
                potential_level = "VERY LOW / UNKNOWN"
                confidence_level = "LOW"
                status = "UNKNOWN"
                reason = f"Functionality of {comp} cannot be evaluated because the component is missing from the device."
            elif is_damaged:
                score = min(10.0, score)
                potential_level = "VERY LOW / UNKNOWN" if score < 10.0 else "LOW"
                confidence_level = "HIGH" if confidence > 75.0 else "MEDIUM"
                status = "ESTIMATED"
                reason = f"Recovery potential of {comp} is low because it is reported as damaged."
            elif is_verified:
                score = 100.0
                confidence = 100.0
                potential_level = "HIGH"
                confidence_level = "HIGH"
                status = "VERIFIED"
                reason = f"{comp} is physically verified as working through functional testing."
            else:
                # Normal estimation case
                # Set assessment levels
                if score >= 75:
                    potential_level = "HIGH"
                elif score >= 50:
                    potential_level = "MEDIUM"
                elif score >= 25:
                    potential_level = "LOW"
                else:
                    potential_level = "VERY LOW / UNKNOWN"

                if confidence >= 75:
                    confidence_level = "HIGH"
                elif confidence >= 50:
                    confidence_level = "MEDIUM"
                else:
                    confidence_level = "LOW"

                status = "ESTIMATED"
                
                # Dynamic User Friendly Reasons
                spec_str = f" ({spec_detail})" if is_known else ""
                if has_power_issue:
                    reason = (
                        f"{comp}{spec_str} has {potential_level.lower()} recovery potential based on device category and specs, "
                        f"but functionality cannot be confirmed because the device does not power on."
                    )
                elif has_functional_issue:
                    reason = (
                        f"{comp}{spec_str} has {potential_level.lower()} recovery potential based on specs, "
                        f"but functional testing failed for the overall device."
                    )
                else:
                    reason = f"{comp}{spec_str} is estimated to have {potential_level.lower()} recovery potential based on overall functional condition."

            # Force final constraint check for non-functional image-only claims:
            # "Internal component functionality cannot be confirmed from an image alone."
            if (has_power_issue or has_functional_issue) and status == "ESTIMATED" and "image" in reason.lower():
                reason += " Internal component functionality cannot be confirmed from an image alone."

            results.append(ComponentRecoveryDetail(
                component_name=comp,
                potential_score=round(score, 1),
                potential_level=potential_level,
                confidence_score=round(confidence, 1),
                confidence_level=confidence_level,
                assessment_status=status,
                reason=reason
            ).to_dict())

        return results
