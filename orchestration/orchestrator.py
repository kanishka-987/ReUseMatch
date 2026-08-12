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
        self.diagnosis_agent = DiagnosisAgent()
        self.decision_agent = DecisionAgent()
        self.need_agent = NeedAgent()
        self.logistics_agent = LogisticsAgent()

    def process_item_submission(self, description: str, location: str, image_url: str = None) -> dict:
        """
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
        }
