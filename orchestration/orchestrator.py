<<<<<<< HEAD
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
    CoordinatorOrchestrator manages the sequencing and coordination of the 5 agents.
    It passes the output of prior agents into subsequent agents and compiles the final result.
    """
    def __init__(self):
        self.evidence_agent = EvidenceAgent()
=======
from agents.object_agent import ObjectAgent, EvidenceAgent
from agents.condition_agent import ConditionAgent, DiagnosisAgent, DecisionAgent
from agents.need_agent import NeedAgent
from agents.logistics_agent import LogisticsAgent

class CoordinatorOrchestrator:
    """
    CoordinatorOrchestrator manages the sequencing and coordination of the 5 agents:
    1. EvidenceAgent (Gemini-powered / mock fallback)
    2. DiagnosisAgent (Gemini-powered / mock fallback)
    3. DecisionAgent (Gemini-powered / mock fallback)
    4. NeedAgent (deterministic matching)
    5. LogisticsAgent (deterministic logistics)
    """
    def __init__(self):
        self.object_agent = ObjectAgent()
        self.evidence_agent = EvidenceAgent()
        self.condition_agent = ConditionAgent()
>>>>>>> origin/member1-frontend-ui
        self.diagnosis_agent = DiagnosisAgent()
        self.decision_agent = DecisionAgent()
        self.need_agent = NeedAgent()
        self.logistics_agent = LogisticsAgent()

    def process_item_submission(self, description: str, location: str, image_url: str = None) -> dict:
        """
<<<<<<< HEAD
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
=======
        Runs the full 5-agent sequential workflow and returns structured results for each agent.
        """
        # 1. Evidence Agent
        evidence_res = self.evidence_agent.run(description, image_url)
        item_details = evidence_res["item_details"]
        category = item_details["category"]

        # 2. Diagnosis Agent
        diagnosis_res = self.diagnosis_agent.run(description, item_details["detected_attributes"])
        condition_grade = diagnosis_res["condition_grade"]

        # 3. Decision Agent
        decision_res = self.decision_agent.run(description, diagnosis_res)
        lifecycle_action = decision_res["best_lifecycle_action"]

        # 4. Need Agent
        need_res = self.need_agent.run(category, condition_grade, lifecycle_action=lifecycle_action)
        need_matches = need_res.get("matches", [])

        # 5. Logistics Agent
        logistics_res = self.logistics_agent.run(location, need_matches, lifecycle_action=lifecycle_action)
        logistics_routes = logistics_res.get("routes", [])

        # Build legacy matches format for backward compatibility & tests
        final_matches = []
        for i, match in enumerate(need_matches):
            route_info = logistics_routes[i] if i < len(logistics_routes) else self.logistics_agent.evaluate_logistics(
                location, match.get("location", f"{match['organization_name']} Center")
            )
            final_matches.append({
                "recipient": {
                    "organization_id": match["organization_id"],
                    "organization_name": match["organization_name"],
                    "priority": match["priority"]
                },
                "logistics": route_info,
                "score": diagnosis_res["condition_score"]
            })

>>>>>>> origin/member1-frontend-ui
        final_matches.sort(key=lambda x: x["score"], reverse=True)

        # Status calculation
        if lifecycle_action == "RECYCLE":
            status_str = "recycled"
        elif final_matches:
            status_str = "matched"
        else:
            status_str = "no_match_found"

        # Final recommendation summary
        rec_orgs = [m["organization_name"] for m in need_matches] if need_matches else []
        logistics_summary = (
            f"{logistics_routes[0]['recommended_mode']} (${logistics_routes[0]['estimated_cost_usd']}, {logistics_routes[0]['distance_km']} km)"
            if logistics_routes else ("Skipped (Recycling)" if lifecycle_action == "RECYCLE" else "Skipped (No match found)")
        )

        final_recommendation = {
            "item_name": item_details["identified_name"],
            "category": category,
            "condition": condition_grade,
            "recommended_lifecycle_action": lifecycle_action,
            "recipient_organizations": rec_orgs if rec_orgs else ["N/A (Recycled/No match)"],
            "estimated_logistics": logistics_summary
        }

        return {
<<<<<<< HEAD
            "item_details": item_details,
            "matches": final_matches,
            "status": "matched" if final_matches else "no_match_found",
            "decision_reasoning": decision_res.get("reasoning", "")
=======
            "status": status_str,
            "item_details": {
                "name": item_details["identified_name"],
                "category": category,
                "condition": condition_grade
            },
            "evidence": evidence_res,
            "diagnosis": diagnosis_res,
            "decision": decision_res,
            "need": need_res,
            "logistics": logistics_routes,
            "matches": final_matches,
            "final_recommendation": final_recommendation
>>>>>>> origin/member1-frontend-ui
        }
