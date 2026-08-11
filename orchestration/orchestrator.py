from agents.object_agent import ObjectAgent
from agents.condition_agent import ConditionAgent
from agents.need_agent import NeedAgent
from agents.logistics_agent import LogisticsAgent

class CoordinatorOrchestrator:
    """
    CoordinatorOrchestrator manages the sequencing and coordination of the 4 agents.
    It passes the output of prior agents into subsequent agents and compiles the final result.
    """
    def __init__(self):
        self.object_agent = ObjectAgent()
        self.condition_agent = ConditionAgent()
        self.need_agent = NeedAgent()
        self.logistics_agent = LogisticsAgent()

    def process_item_submission(self, description: str, location: str, image_url: str = None) -> dict:
        """
        Runs the full 4-agent sequential workflow.
        """
        # 1. Identify Item
        object_info = self.object_agent.identify_item(description, image_url)
        
        # 2. Evaluate Condition
        condition_info = self.condition_agent.evaluate_condition(
            description, 
            object_info.get("detected_attributes")
        )
        
        # 3. Find Recipient Needs
        need_matches = self.need_agent.find_potential_matches(
            object_info.get("category"),
            condition_info.get("condition_grade")
        )
        
        # 4. Determine Logistics for the potential matches
        final_matches = []
        for match in need_matches:
            # Assume recipient location is mock-sourced or database-derived
            mock_recipient_loc = f"{match['organization_name']} Center, Downtown"
            
            logistics_info = self.logistics_agent.evaluate_logistics(
                location, 
                mock_recipient_loc
            )
            
            final_matches.append({
                "recipient": match,
                "logistics": logistics_info,
                "score": condition_info["usability_score"]
            })

        # Sort matches by quality score or logistics distance (here: score)
        final_matches.sort(key=lambda x: x["score"], reverse=True)

        return {
            "item_details": {
                "name": object_info["identified_name"],
                "category": object_info["category"],
                "condition": condition_info["condition_grade"]
            },
            "matches": final_matches,
            "status": "matched" if final_matches else "no_match_found"
        }
