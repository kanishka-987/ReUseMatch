from agents.evidence_agent.agent import EvidenceAgent
from agents.diagnosis_agent.agent import DiagnosisAgent
from agents.decision_agent.agent import DecisionAgent
from agents.need_agent.agent import NeedAgent
from agents.logistics_agent.agent import LogisticsAgent


try:
    from agents.object_agent import ObjectAgent
except ImportError:
    class ObjectAgent:
        def identify_item(self, description: str, image_url: str = None):
            return {
                "identified_name": description,
                "category": "Electronics",
                "detected_attributes": {}
            }


try:
    from agents.condition_agent import ConditionAgent
except ImportError:
    class ConditionAgent:
        def evaluate_condition(self, description: str, attributes: dict = None):
            return {
                "condition_grade": "Good",
                "usability_score": 0.85
            }


class CoordinatorOrchestrator:
    """
    Coordinates the complete ReUseMatch agent pipeline:

    1. Evidence Agent
    2. Diagnosis Agent
    3. Decision Agent
    4. Need Agent
    5. Logistics Agent

    Also returns structured intermediate results for the frontend UI.
    """

    def __init__(self):
        self.evidence_agent = EvidenceAgent()
        self.diagnosis_agent = DiagnosisAgent()
        self.decision_agent = DecisionAgent()
        self.need_agent = NeedAgent()
        self.logistics_agent = LogisticsAgent()

    def process_item_submission(
        self,
        description: str,
        location: str,
        image_url: str = None
    ) -> dict:
        """
        Runs the complete 5-agent workflow.

        Handles:
        - input validation
        - evidence extraction
        - condition diagnosis
        - lifecycle decision
        - recipient matching
        - logistics evaluation
        - structured frontend response
        """

        # ---------------------------------------------------------
        # Validate inputs
        # ---------------------------------------------------------
        if not description or not location:
            missing = []

            if not description:
                missing.append("description")

            if not location:
                missing.append("location")

            return {
                "status": "error",
                "error_message": (
                    "Missing required input fields: "
                    "description and location are mandatory."
                ),
                "missing_information": missing
            }

        # ---------------------------------------------------------
        # 1. Evidence Agent
        # ---------------------------------------------------------
        evidence_res = self.evidence_agent.run(
            description,
            image_url
        )

        item_details_from_evidence = evidence_res.get(
            "item_details",
            {}
        )

        observed_evidence = evidence_res.get(
            "observed_evidence",
            []
        )

        category = item_details_from_evidence.get(
            "category",
            "General"
        )

        identified_name = item_details_from_evidence.get(
            "identified_name",
            "Unknown Item"
        )

        detected_attributes = item_details_from_evidence.get(
            "detected_attributes",
            {}
        )

        # ---------------------------------------------------------
        # 2. Diagnosis Agent
        # ---------------------------------------------------------
        diagnosis_res = self.diagnosis_agent.run(
            description,
            detected_attributes=(
                observed_evidence
                if observed_evidence
                else detected_attributes
            )
        )

        condition_score = diagnosis_res.get(
            "condition_score",
            5.0
        )

        repairability = diagnosis_res.get(
            "repairability",
            True
        )

        reuse_potential = diagnosis_res.get(
            "reuse_potential",
            True
        )

        condition_info = diagnosis_res.get(
            "condition_info",
            {}
        )

        condition_grade = condition_info.get(
            "condition_grade",
            diagnosis_res.get(
                "condition_grade",
                "Good"
            )
        )

        # ---------------------------------------------------------
        # 3. Decision Agent
        # ---------------------------------------------------------
        decision_res = self.decision_agent.run(
            condition_score=condition_score,
            repairability=repairability,
            reuse_potential=reuse_potential
        )

        lifecycle_action = decision_res.get(
            "best_lifecycle_action",
            "REUSE"
        )

        # ---------------------------------------------------------
        # Common item details
        # ---------------------------------------------------------
        item_details = {
            "name": identified_name,
            "category": category,
            "condition": condition_grade
        }

        # ---------------------------------------------------------
        # 4. Need Agent
        # ---------------------------------------------------------
        need_res = self.need_agent.run(
            category=category,
            condition_grade=condition_grade,
            lifecycle_action=lifecycle_action
        )

        need_matches = need_res.get(
            "matches",
            []
        )

        # ---------------------------------------------------------
        # RECYCLE handling
        # ---------------------------------------------------------
        if lifecycle_action == "RECYCLE":
            return {
                "status": "recycled",
                "item_details": item_details,
                "evidence": evidence_res,
                "diagnosis": diagnosis_res,
                "decision": decision_res,
                "need": need_res,
                "logistics": [],
                "matches": [],
                "final_recommendation": {
                    "item_name": identified_name,
                    "category": category,
                    "condition": condition_grade,
                    "recommended_lifecycle_action": lifecycle_action,
                    "recipient_organizations": [
                        "N/A (Recycled)"
                    ],
                    "estimated_logistics": "Skipped (Recycling)"
                },
                "decision_reasoning": decision_res.get(
                    "reasoning",
                    ""
                )
            }

        # ---------------------------------------------------------
        # 5. Logistics Agent
        # ---------------------------------------------------------
        final_matches = []
        logistics_routes = []

        for match in need_matches:
            recipient_loc = match.get("location")

            if recipient_loc:
                logistics_info = self.logistics_agent.run(
                    donor_location=location,
                    recipient_location=recipient_loc
                )
            else:
                logistics_info = {
                    "origin": location,
                    "destination": None,
                    "distance_km": 0.0,
                    "estimated_cost_usd": 0.0,
                    "recommended_mode": "Unknown",
                    "route_status": "error"
                }

                missing_info = match.get(
                    "missing_information",
                    []
                )

                if "recipient_location" not in missing_info:
                    missing_info.append(
                        "recipient_location"
                    )

                match["missing_information"] = missing_info

            logistics_routes.append(logistics_info)

            final_matches.append({
                "recipient": match,
                "logistics": logistics_info,
                "score": condition_score
            })

        # ---------------------------------------------------------
        # Sort matches
        # ---------------------------------------------------------
        final_matches.sort(
            key=lambda x: x["score"],
            reverse=True
        )

        # ---------------------------------------------------------
        # Status
        # ---------------------------------------------------------
        if final_matches:
            status_str = "matched"
        else:
            status_str = "no_match_found"

        # ---------------------------------------------------------
        # Recommendation summary
        # ---------------------------------------------------------
        rec_orgs = [
            match.get("organization_name")
            for match in need_matches
            if match.get("organization_name")
        ]

        if logistics_routes:
            first_route = logistics_routes[0]

            logistics_summary = (
                f"{first_route.get('recommended_mode', 'Unknown')} "
                f"(${first_route.get('estimated_cost_usd', 0.0)}, "
                f"{first_route.get('distance_km', 0.0)} km)"
            )
        else:
            logistics_summary = "Skipped (No match found)"

        final_recommendation = {
            "item_name": identified_name,
            "category": category,
            "condition": condition_grade,
            "recommended_lifecycle_action": lifecycle_action,
            "recipient_organizations": (
                rec_orgs
                if rec_orgs
                else ["N/A (No match)"]
            ),
            "estimated_logistics": logistics_summary
        }

        # ---------------------------------------------------------
        # Final structured response
        # ---------------------------------------------------------
        return {
            "status": status_str,

            "item_details": item_details,

            "evidence": evidence_res,

            "diagnosis": diagnosis_res,

            "decision": decision_res,

            "need": need_res,

            "logistics": logistics_routes,

            "matches": final_matches,

            "final_recommendation": final_recommendation,

            "decision_reasoning": decision_res.get(
                "reasoning",
                ""
            )
        }