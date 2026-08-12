from .device_profile import DeviceProfile
from .image_analyzer import ImageAnalysisResult
from .condition_analyzer import ConditionAnalyzer
from .component_analyzer import ComponentAnalyzer
from .reuse_scorer import ReuseScorer
from .component_recovery import ComponentRecoveryEstimator
from typing import Optional, Dict, Any, List

class DeviceAnalyzer:
    """
    Main orchestrator for the Device Analysis system.
    Runs physical/functional evaluation, component salvage audit, scoring,
    and produces recommendations and circular economy impact summaries.
    """
    def __init__(self, scorer: Optional[ReuseScorer] = None):
        self.condition_analyzer = ConditionAnalyzer()
        self.component_analyzer = ComponentAnalyzer()
        self.scorer = scorer or ReuseScorer()
        self.recovery_estimator = ComponentRecoveryEstimator()

    def analyze_device(
        self, 
        profile: DeviceProfile, 
        image_result: Optional[ImageAnalysisResult] = None
    ) -> Dict[str, Any]:
        """
        Processes a DeviceProfile and produces an explainable, structured analysis output.
        Allows incorporating computer-vision insights if available.
        """
        # Integrate image-analysis findings if provided (e.g., merging detected visible damages)
        if image_result:
            merged_damage = list(set(profile.visible_damage + image_result.visible_damage))
            profile = profile.model_copy(update={"visible_damage": merged_damage})
            if not profile.subcategory and image_result.detected_subcategory:
                profile = profile.model_copy(update={"subcategory": image_result.detected_subcategory})

        # 1. Condition Analysis
        cond_res = self.condition_analyzer.analyze(profile)
        
        # 2. Component Analysis
        comp_res = self.component_analyzer.analyze(profile)
        
        # 2b. Component Recovery Estimation
        recovery_res = self.recovery_estimator.estimate_recovery(profile)
        
        # 3. Reuse Potential Score
        score_res = self.scorer.evaluate(profile, comp_res)

        # 4. Repairability Sub-analysis
        repair_score = score_res["factor_scores"]["repairability"]
        if repair_score >= 80:
            repair_level = "HIGH"
            repair_reason = "Device has zero to one minor faulty component with simple replacement requirements."
        elif repair_score >= 50:
            repair_level = "MODERATE"
            repair_reason = "Device requires professional parts replacement or moderate maintenance."
        else:
            repair_level = "LOW"
            repair_reason = "Device suffers from multiple critical failures or is non-modular."

        # 5. Recommendation Generation
        overall_g = cond_res.overall_grade
        reusable_comps = [c for c in comp_res if c["reusable"]]
        high_potential_comps = [c for c in recovery_res if c["potential_score"] >= 75]
        
        is_obsolete = profile.estimated_age > 6.0
        is_integrated_device = profile.category in ("Smartphone", "Tablet")
        main_board_damaged = is_integrated_device and any(
            c in [dc.lower().strip() for dc in profile.damaged_components]
            for c in ["logic board", "motherboard"]
        )

        if not profile.power_status:
            # Completely dead - no power
            if len(high_potential_comps) >= 2 and not is_obsolete and not main_board_damaged:
                rec_action = "COMPONENT_REUSE"
                rec_reason = "The complete device is not currently suitable for direct reuse because it does not power on. However, several components have high estimated recovery potential and may be suitable for component reuse."
            else:
                rec_action = "RECYCLING"
                rec_reason = "The device is entirely non-functional or obsolete with minimal salvageable value. Reclaimed materials should be recycled safely."
        elif not profile.working_status:
            # Powers on but not working. If it's repairable (repairability_score >= 50), recommend REPAIR
            if repair_score >= 50:
                rec_action = "REPAIR"
                rec_reason = "The device powers on but fails key operational tests. Replacing the faulty components will restore full utility."
            elif len(high_potential_comps) >= 2 and not is_obsolete and not main_board_damaged:
                rec_action = "COMPONENT_REUSE"
                rec_reason = "The complete device is not currently suitable for direct reuse because key functional tests failed. However, several components have high estimated recovery potential and may be suitable for component reuse."
            else:
                rec_action = "RECYCLING"
                rec_reason = "The device is entirely non-functional or obsolete with minimal salvageable value. Reclaimed materials should be recycled safely."
        else:
            # Fully functional and powers on
            if overall_g in ("EXCELLENT", "GOOD"):
                rec_action = "DIRECT_REUSE"
                rec_reason = "The device functions perfectly with no major physical flaws. It can be redeployed immediately."
            else:
                rec_action = "REFURBISHMENT"
                rec_reason = "The device is functional but requires software wiping, OS installation, or deep cleaning."

        # 6. Circular Economy Impact Calculation
        weight_estimates = {
            "Laptop": 2.2,
            "Desktop": 9.5,
            "Monitor": 4.5,
            "Smartphone": 0.2,
            "Tablet": 0.5,
        }
        device_weight = weight_estimates.get(profile.category, 1.5)
        
        if rec_action in ("DIRECT_REUSE", "REFURBISHMENT"):
            diversion = "TOTAL_LANDFILL_AVOIDANCE"
            landfill_avoided_kg = device_weight
            life_extension = "SIGNIFICANT (2-3 years)"
        elif rec_action == "REPAIR":
            diversion = "TOTAL_LANDFILL_AVOIDANCE"
            landfill_avoided_kg = device_weight
            life_extension = "MODERATE (1-2 years)"
        elif rec_action == "COMPONENT_REUSE":
            diversion = "PARTIAL_RECOVERY"
            # Assume 40% of physical mass is recovered as spare parts
            landfill_avoided_kg = round(device_weight * 0.4, 2)
            life_extension = "EXTENDED VIA HARVESTED SUBPARTS"
        else:
            diversion = "MATERIAL_RECYCLING"
            landfill_avoided_kg = 0.0
            life_extension = "NONE"

        # 7. Simplified Analysis Summary Object
        summary_text = (
            f"{profile.brand} {profile.model} ({profile.category}) - Graded overall as {overall_g}. "
            f"Suggested action: {rec_action}."
        )

        analysis_summary = {
            "summary": summary_text,
            "condition": overall_g,
            "reuse_score": score_res["total_score"],
            "reuse_level": score_res["reuse_level"],
            "repairability": repair_score,
            "reusable_component_count": len(reusable_comps),
            "recommended_action": rec_action,
            "explanation": [
                f"Overall Condition: {overall_g} - {cond_res.overall_explanation}",
                f"Repairability: {repair_level} - {repair_reason}",
                f"Recommendation: {rec_action} - {rec_reason}",
                f"Impact: {diversion} with {landfill_avoided_kg} kg diverted."
            ],
            "component_recovery": recovery_res
        }

        return {
            "item_id": profile.item_id,
            "device_profile": profile.model_dump(),
            "condition_analysis": cond_res.to_dict(),
            "component_analysis": comp_res,
            "component_recovery": recovery_res,
            "repairability": {
                "repairability_score": repair_score,
                "repairability_level": repair_level,
                "repair_reason": repair_reason
            },
            "reuse_score": score_res,
            "recommendation": {
                "recommended_action": rec_action,
                "explanation": rec_reason
            },
            "circular_economy_impact": {
                "landfill_diversion_status": diversion,
                "estimated_weight_diverted_kg": landfill_avoided_kg,
                "estimated_product_life_extension": life_extension
            },
            "analysis_summary": analysis_summary
        }
