from .device_profile import DeviceProfile
from typing import List, Dict

class AnalyzedComponent:
    def __init__(
        self,
        component_name: str,
        condition: str,
        reusable: bool,
        repairable: bool,
        estimated_value: float,
        reuse_confidence: float,
        possible_reuse: str,
        explanation: str
    ):
        self.component_name = component_name
        self.condition = condition
        self.reusable = reusable
        self.repairable = repairable
        self.estimated_value = estimated_value
        self.reuse_confidence = reuse_confidence
        self.possible_reuse = possible_reuse
        self.explanation = explanation

    def to_dict(self) -> dict:
        return {
            "component_name": self.component_name,
            "condition": self.condition,
            "reusable": self.reusable,
            "repairable": self.repairable,
            "estimated_value": self.estimated_value,
            "reuse_confidence": self.reuse_confidence,
            "possible_reuse": self.possible_reuse,
            "explanation": self.explanation
        }

class ComponentAnalyzer:
    """
    Evaluates individual hardware components for salvage/reuse feasibility based on the device category.
    """
    CATEGORY_COMPONENTS: Dict[str, List[str]] = {
        "Laptop": ["RAM", "SSD/HDD", "Display", "Keyboard", "Touchpad", "Battery", "Charger", "Motherboard", "Wi-Fi module"],
        "Desktop": ["RAM", "CPU", "GPU", "Storage", "Power supply", "Motherboard", "Case"],
        "Monitor": ["Display panel", "Stand", "Power adapter", "Control board", "Ports"],
        "Smartphone": ["Display screen", "Battery", "Camera module", "Logic board", "Speaker"],
        "Tablet": ["Display screen", "Battery", "Logic board", "Charger"],
    }

    def __init__(self):
        pass

    def analyze(self, profile: DeviceProfile) -> List[dict]:
        """
        Determines component recovery potential and returns a list of component analysis results.
        """
        category = profile.category
        components_to_check = self.CATEGORY_COMPONENTS.get(category, ["Main board", "Chassis", "Power supply"])
        
        damaged = {c.lower().strip() for c in profile.damaged_components}
        missing = {c.lower().strip() for c in profile.missing_components}
        
        analyzed_list = []
        
        # Base factor for pricing/confidence based on age & overall condition
        condition_factors = {
            "EXCELLENT": (1.0, 0.95),
            "GOOD": (0.7, 0.85),
            "FAIR": (0.4, 0.70),
            "POOR": (0.2, 0.50),
            "NON_FUNCTIONAL": (0.1, 0.30)
        }
        val_factor, conf_factor = condition_factors.get(profile.functional_condition.upper(), (0.3, 0.5))

        for comp in components_to_check:
            comp_lower = comp.lower().strip()
            
            # Base values for mock calculations
            base_values = {
                "RAM": 30.0, "SSD/HDD": 40.0, "Display": 80.0, "Keyboard": 15.0, "Touchpad": 10.0,
                "Battery": 25.0, "Charger": 20.0, "Motherboard": 90.0, "Wi-Fi module": 15.0,
                "CPU": 100.0, "GPU": 150.0, "Storage": 40.0, "Power supply": 35.0, "Case": 30.0,
                "Display panel": 90.0, "Stand": 20.0, "Power adapter": 25.0, "Control board": 30.0,
                "Ports": 10.0, "Display screen": 70.0, "Camera module": 30.0, "Logic board": 100.0,
                "Speaker": 10.0, "Main board": 50.0, "Chassis": 20.0
            }
            base_val = base_values.get(comp, 25.0)
            
            # Determine flags
            is_missing = comp_lower in missing
            is_damaged = comp_lower in damaged
            
            if is_missing:
                reusable = False
                repairable = False
                est_val = 0.0
                confidence = 0.0
                condition = "MISSING"
                possible_reuse = "None"
                explanation = f"Component '{comp}' is absent from the device."
            elif is_damaged:
                reusable = False
                # Batterys or logic boards might not be easily repairable, RAM isn't, but casing/screens might be
                repairable = comp not in ["RAM", "CPU", "Wi-Fi module"]
                est_val = round(base_val * 0.1, 2)
                confidence = 0.20
                condition = "DAMAGED"
                possible_reuse = "Material recovery / scrap" if not repairable else f"Refurbish / repair {comp}"
                explanation = f"Component '{comp}' is reported as damaged or faulty. Recommended for {possible_reuse.lower()}."
            else:
                reusable = True
                repairable = False
                est_val = round(base_val * val_factor * max(0.2, (1.0 - (profile.estimated_age * 0.1))), 2)
                confidence = conf_factor
                condition = profile.functional_condition
                
                # Possible reuse recommendation
                if comp in ["SSD/HDD", "Storage"]:
                    possible_reuse = "Wipe and reuse as external secondary storage"
                elif comp in ["RAM", "CPU", "GPU"]:
                    possible_reuse = "Extract for upgrading or repairing compatible machines"
                elif comp in ["Display", "Display panel", "Display screen"]:
                    possible_reuse = "Repurpose as standalone display or repair module"
                elif comp in ["Battery", "Charger", "Power adapter"]:
                    possible_reuse = "Accessory reuse or spare parts library"
                else:
                    possible_reuse = "Harvest as functional replacement parts"
                    
                explanation = f"Component '{comp}' is functional, graded as '{condition}', and suitable for component extraction and reuse."

            analyzed_list.append(AnalyzedComponent(
                component_name=comp,
                condition=condition,
                reusable=reusable,
                repairable=repairable,
                estimated_value=est_val,
                reuse_confidence=confidence,
                possible_reuse=possible_reuse,
                explanation=explanation
            ).to_dict())
            
        return analyzed_list
