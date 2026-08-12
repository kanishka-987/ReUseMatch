class NeedAgent:
    """
    NeedAgent is responsible for matching the identified item and condition grade
    against database lists of organization/individual requests and needs.
    """
    def __init__(self):
        pass

    def find_potential_matches(self, category: str, condition_grade: str) -> list:
        """
        Legacy match finding logic.
        """
        mock_organizations = [
            {
                "id": "org_001",
                "name": "Community Housing Shelter",
                "needs": ["furniture", "electronics"],
                "min_condition": "Good",
                "location": "Community Housing Shelter Center, Downtown",
                "reason": "High demand for community room furniture & tech",
                "match_score": 88
            },
            {
                "id": "org_002",
                "name": "Second Chance Goods",
                "needs": ["furniture", "clothing", "electronics"],
                "min_condition": "Fair",
                "location": "Second Chance Hub, Westside",
                "reason": "Refurbishment & job training program",
                "match_score": 80
            },
            {
                "id": "org_003",
                "name": "Kids Club Foundation",
                "needs": ["toys", "furniture", "electronics"],
                "min_condition": "Good",
                "location": "Kids Club Learning Center, Northside",
                "reason": "Youth educational computer lab expansion",
                "match_score": 92
            }
        ]

        matches = []
        for org in mock_organizations:
            category_match = category.lower() in [n.lower() for n in org["needs"]]
            condition_rank = {"Like New": 3, "Good": 2, "Fair": 1, "Poor": 0}
            item_rank = condition_rank.get(condition_grade, 0)
            min_rank = condition_rank.get(org["min_condition"], 0)

            if category_match and item_rank >= min_rank:
                matches.append({
                    "organization_id": org["id"],
                    "organization_name": org["name"],
                    "priority": "High" if item_rank > min_rank else "Medium",
                    "match_score": org.get("match_score", 85),
                    "reason": org.get("reason", "Needs item matching category"),
                    "location": org.get("location", f"{org['name']} Center"),
                    "missing_information": "None"
                })

        return matches

    def run(self, category: str, condition_grade: str, lifecycle_action: str = "REUSE") -> dict:
        """
        Runs NeedAgent pipeline stage. If lifecycle_action is RECYCLE, matching is skipped.
        """
        if lifecycle_action == "RECYCLE":
            return {
                "status": "Skipped",
                "matching_organizations_count": 0,
                "matches": [],
                "skip_reason": "Recipient matching was bypassed because the lifecycle decision is RECYCLE."
            }

        matches = self.find_potential_matches(category, condition_grade)

        return {
            "status": "Success",
            "matching_organizations_count": len(matches),
            "matches": matches,
            "skip_reason": None
        }
