from agents.evidence_agent.agent import EvidenceAgent
from agents.diagnosis_agent.agent import DiagnosisAgent
from agents.decision_agent.agent import DecisionAgent
from agents.need_agent.agent import NeedAgent
from agents.logistics_agent.agent import LogisticsAgent

class CoordinatorOrchestrator:
    """
    CoordinatorOrchestrator manages the sequencing and coordination of the 5 agents.
    It passes the output of prior agents into subsequent agents and compiles the final result.
    """
    def __init__(self):
        self.evidence_agent = EvidenceAgent()
        self.diagnosis_agent = DiagnosisAgent()
        self.decision_agent = DecisionAgent()
        self.need_agent = NeedAgent()
        self.logistics_agent = LogisticsAgent()

    def process_item_submission(self, description: str, location: str, image_url: str = None) -> dict:
        """
        Runs the full 5-agent sequential workflow.
        Handles missing inputs, recycle logic bypass, and location routing.
        """
        # Validate inputs
        if not description or not location:
            missing = []
            if not description:
                missing.append("description")
            if not location:
                missing.append("location")
            return {
                "status": "error",
                "error_message": "Missing required input fields: description and location are mandatory.",
                "missing_information": missing
            }

        # 1. Evidence Extraction
        evidence_res = self.evidence_agent.run(description, image_url)
        observed_evidence = evidence_res.get("observed_evidence", [])
        category = evidence_res.get("item_details", {}).get("category", "General")

        # 2. Evaluate Condition
        diagnosis_res = self.diagnosis_agent.run(description, detected_attributes=observed_evidence)
        condition_score = diagnosis_res.get("condition_score", 5.0)
        repairability = diagnosis_res.get("repairability", True)
        reuse_potential = diagnosis_res.get("reuse_potential", True)
        condition_grade = diagnosis_res.get("condition_info", {}).get("condition_grade", "Good")

        # 3. Decision Assessment
        decision_res = self.decision_agent.run(
            condition_score=condition_score,
            repairability=repairability,
            reuse_potential=reuse_potential
        )
        lifecycle_action = decision_res.get("best_lifecycle_action", "REUSE")

        # Compile common item details for output
        item_details = {
            "name": evidence_res.get("item_details", {}).get("identified_name", "Unknown Item"),
            "category": category,
            "condition": condition_grade
        }

        # Handle RECYCLE bypass logic
        if lifecycle_action == "RECYCLE":
            return {
                "item_details": item_details,
                "matches": [],
                "status": "recycle",
                "decision_reasoning": decision_res.get("reasoning", "")
            }

        # 4. Find Recipient Needs
        need_res = self.need_agent.run(category=category, condition_grade=condition_grade)
        need_matches = need_res.get("matches", [])

        # 5. Determine Logistics for matches
        final_matches = []
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
                # Track missing recipient location
                missing_info = match.get("missing_information", [])
                if "recipient_location" not in missing_info:
                    missing_info.append("recipient_location")
                match["missing_information"] = missing_info

            final_matches.append({
                "recipient": match,
                "logistics": logistics_info,
                "score": condition_score
            })

        # Sort matches by score descending
        final_matches.sort(key=lambda x: x["score"], reverse=True)

        return {
            "item_details": item_details,
            "matches": final_matches,
            "status": "matched" if final_matches else "no_match_found",
            "decision_reasoning": decision_res.get("reasoning", "")
        }
