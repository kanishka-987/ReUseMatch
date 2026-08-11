class NeedAgent:
    """
    NeedAgent is responsible for matching the identified item and condition grade
    against database lists of organization/individual requests and needs.
    """
    def __init__(self):
        pass

    def find_potential_matches(self, category: str, condition_grade: str) -> list:
        """
        Queries target lists of needs to find compatible organizations.
        """
        # Placeholder recipient list
        mock_organizations = [
            {"id": "org_001", "name": "Community Housing Shelter", "needs": ["furniture"], "min_condition": "Good"},
            {"id": "org_002", "name": "Second Chance Goods", "needs": ["furniture", "clothing"], "min_condition": "Fair"},
            {"id": "org_003", "name": "Kids Club Foundation", "needs": ["toys", "furniture"], "min_condition": "Good"}
        ]
        
        matches = []
        for org in mock_organizations:
            category_match = category.lower() in [n.lower() for n in org["needs"]]
            # Simple condition matching hierarchy: Like New > Good > Fair
            condition_rank = {"Like New": 3, "Good": 2, "Fair": 1}
            item_rank = condition_rank.get(condition_grade, 0)
            min_rank = condition_rank.get(org["min_condition"], 0)
            
            if category_match and item_rank >= min_rank:
                matches.append({
                    "organization_id": org["id"],
                    "organization_name": org["name"],
                    "priority": "High" if item_rank > min_rank else "Medium"
                })
                
        return matches
