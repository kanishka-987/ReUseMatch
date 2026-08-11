from datetime import datetime
from typing import Dict, Any, List
from .passport import DigitalReusePassport, StatusHistoryEntry
from .passport_status import PassportStatus

class PassportGenerator:
    """
    Constructs and registers new DigitalReusePassport objects from DeviceAnalyzer output reports.
    """
    _counter: int = 1  # In-memory counter for mock ID generation

    def __init__(self):
        pass

    @classmethod
    def _generate_unique_id(cls) -> str:
        """
        Builds a unique passport ID following the scheme: RM-PASS-YYYY-XXXXXX
        """
        current_year = datetime.utcnow().year
        formatted_counter = f"{cls._counter:06d}"
        cls._counter += 1
        return f"RM-PASS-{current_year}-{formatted_counter}"

    def generate_passport(self, analysis_report: Dict[str, Any]) -> DigitalReusePassport:
        """
        Translates raw analysis output into a validated DigitalReusePassport structure.
        """
        summary = analysis_report["analysis_summary"]
        profile = analysis_report["device_profile"]
        cond = analysis_report["condition_analysis"]
        impact = analysis_report["circular_economy_impact"]
        
        passport_id = self._generate_unique_id()
        current_time = datetime.utcnow().isoformat() + "Z"
        
        # Determine some suggested recipient segments based on recommended action
        rec_action = summary["recommended_action"]
        if rec_action == "DIRECT_REUSE":
            recipients = ["Schools", "Community Centers", "Low-income Families"]
        elif rec_action == "REFURBISHMENT":
            recipients = ["Refurbishers", "Vocational Training Labs"]
        elif rec_action == "REPAIR":
            recipients = ["Local Maker Spaces", "Repair Cafes"]
        elif rec_action == "COMPONENT_REUSE":
            recipients = ["Hardware Spare Parts Library", "Electronics Hobbyists"]
        else:
            recipients = ["Certified E-Waste Recycler"]

        # Prepare initial history log
        initial_history = [
            StatusHistoryEntry(
                status=PassportStatus.ANALYZED,
                timestamp=current_time,
                description="Device analysis completed; passport registered."
            )
        ]

        passport = DigitalReusePassport(
            passport_id=passport_id,
            item_id=analysis_report["item_id"],
            device_name=f"{profile['brand']} {profile['model']}",
            category=profile["category"],
            brand=profile["brand"],
            model=profile["model"],
            estimated_age=profile["estimated_age"],
            
            # Condition parameters
            physical_condition=profile["physical_condition"],
            functional_condition=profile["functional_condition"],
            damage_description=cond["physical_explanation"] + " " + cond["functional_explanation"],
            repairability_score=analysis_report["repairability"]["repairability_score"],
            
            # Reusable components
            reusable_components=analysis_report["component_analysis"],
            
            # Sustainability
            reuse_score=summary["reuse_score"],
            reuse_level=summary["reuse_level"],
            estimated_remaining_life=impact["estimated_product_life_extension"],
            recyclability_status=f"Landfill Diversion: {impact['landfill_diversion_status']}",
            
            # Recommendations
            recommended_reuse_path=rec_action,
            possible_recipients=recipients,
            
            # Lifecycle
            current_status=PassportStatus.ANALYZED,
            analysis_date=current_time,
            last_updated_date=current_time,
            
            # Verification & Logs
            analysis_confidence=round(profile.get("confidence_score", 0.90), 2),
            validation_status="VERIFIED",
            status_history=initial_history
        )
        
        return passport
