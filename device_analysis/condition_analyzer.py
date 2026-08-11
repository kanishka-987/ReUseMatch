from .device_profile import DeviceProfile
from .validators import validate_condition_string

class ConditionAnalysisResult:
    def __init__(
        self,
        physical_grade: str,
        physical_explanation: str,
        functional_grade: str,
        functional_explanation: str,
        overall_grade: str,
        overall_explanation: str
    ):
        self.physical_grade = validate_condition_string(physical_grade)
        self.physical_explanation = physical_explanation
        self.functional_grade = validate_condition_string(functional_grade)
        self.functional_explanation = functional_explanation
        self.overall_grade = validate_condition_string(overall_grade)
        self.overall_explanation = overall_explanation

    def to_dict(self) -> dict:
        return {
            "physical_grade": self.physical_grade,
            "physical_explanation": self.physical_explanation,
            "functional_grade": self.functional_grade,
            "functional_explanation": self.functional_explanation,
            "overall_grade": self.overall_grade,
            "overall_explanation": self.overall_explanation
        }

class ConditionAnalyzer:
    """
    Evaluates physical, functional, and component indicators to assign explainable condition grades.
    """
    def __init__(self):
        pass

    def analyze(self, profile: DeviceProfile) -> ConditionAnalysisResult:
        """
        Analyzes the DeviceProfile to evaluate condition and generate descriptive explanations.
        """
        # 1. Physical Condition Analysis
        phys = profile.physical_condition.upper()
        phys_damage = profile.visible_damage
        
        if phys == "EXCELLENT" and not phys_damage:
            phys_expl = "The device displays no visible casing wear, blemishes, or scratches."
        elif phys in ("EXCELLENT", "GOOD") and len(phys_damage) <= 1:
            phys_expl = f"The device is physically stable with minor cosmetic wear: {', '.join(phys_damage) or 'minor blemishes'}."
        elif phys == "FAIR":
            phys_expl = f"The device displays noticeable cosmetic wear or moderate damage: {', '.join(phys_damage) or 'surface scratches'}."
        else:
            phys_expl = f"The device shows severe physical wear or critical damage: {', '.join(phys_damage) or 'cracked or loose parts'}."

        # 2. Functional Condition Analysis
        func = profile.functional_condition.upper()
        working = profile.working_status
        power = profile.power_status
        damaged = profile.damaged_components
        missing = profile.missing_components

        if not power:
            func_grade = "NON_FUNCTIONAL"
            func_expl = "The device does not boot or draw power."
        elif not working:
            func_grade = "NON_FUNCTIONAL"
            func_expl = f"The device powers on but fails key operational tests. Damaged: {', '.join(damaged) or 'None'}."
        elif len(damaged) > 0 or len(missing) > 0:
            func_grade = "FAIR" if len(damaged) <= 2 else "POOR"
            func_expl = (
                f"Device is operational but has degraded components. "
                f"Damaged: {', '.join(damaged) or 'None'}. Missing: {', '.join(missing) or 'None'}."
            )
        else:
            func_grade = func
            if func_grade == "EXCELLENT":
                func_expl = "All core functionalities and interfaces passed functional testing."
            else:
                func_expl = "Device functions within standard limits with normal performance characteristics."

        # 3. Overall composite rating
        # If not booting/working overall must be NON_FUNCTIONAL
        if func_grade == "NON_FUNCTIONAL" or not power or not working:
            overall_grade = "NON_FUNCTIONAL"
            overall_expl = "Device is non-functional due to power/operational test failures."
        elif phys == "POOR" or func_grade == "POOR":
            overall_grade = "POOR"
            overall_expl = "Device has severe degradation in functional capacity or physical frame integrity."
        elif phys == "FAIR" or func_grade == "FAIR":
            overall_grade = "FAIR"
            overall_expl = "Device is functional but has visible cosmetic defects or minor damaged/missing subparts."
        elif phys == "GOOD" and func_grade in ("GOOD", "EXCELLENT"):
            overall_grade = "GOOD"
            overall_expl = "Device is fully functional with minimal casing wear and no critical component failures."
        else:
            overall_grade = "EXCELLENT"
            overall_expl = "Device is in pristine cosmetic and operational condition."

        return ConditionAnalysisResult(
            physical_grade=phys,
            physical_explanation=phys_expl,
            functional_grade=func_grade,
            functional_explanation=func_expl,
            overall_grade=overall_grade,
            overall_explanation=overall_expl
        )
