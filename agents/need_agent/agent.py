from agents.common.base_agent import BaseAgent
from .schemas import NeedInput, NeedResult, NeedMatch

class NeedAgent(BaseAgent):
    """
    NeedAgent is responsible for matching the identified item and condition grade
    against database lists of organization/individual requests and needs.
    """
    def __init__(self):
        super().__init__(name="NeedAgent")

    def _get_mock_organizations(self) -> list:
        return [
            {
                "id": "org_001",
                "name": "Community Housing Shelter",
                "needs": ["furniture"],
                "min_condition": "Good",
                "location": "123 Hope Lane"
            },
            {
                "id": "org_002",
                "name": "Second Chance Goods",
                "needs": ["furniture", "clothing"],
                "min_condition": "Fair",
                "location": "456 Charity Way"
            },
            {
                "id": "org_003",
                "name": "Kids Club Foundation",
                "needs": ["toys", "furniture"],
                "min_condition": "Good",
                "location": "789 Youth Ave"
            },
            {
                "id": "org_004",
                "name": "Tech for All",
                "needs": ["laptop", "monitor", "electronics"],
                "min_condition": "Fair",
                "location": "100 Tech Way"
            },
            {
                "id": "org_005",
                "name": "Digital Divide Aid",
                "needs": ["laptop"],
                "min_condition": "Good",
                "location": "456 Gateway Road"
            }
        ]

    def find_potential_matches(self, category: str, condition_grade: str) -> list:
        """
<<<<<<< HEAD
        Queries target lists of needs to find compatible organizations.
        Keeps legacy behavior intact but returns a list.
        """
        mock_organizations = self._get_mock_organizations()
=======
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

>>>>>>> origin/member1-frontend-ui
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

<<<<<<< HEAD
    def run(self, category: str, condition_grade: str) -> dict:
        """
        Execute need agent matches, validate inputs/outputs using Pydantic,
        and rank results by a transparent match score.
        """
        # Validate inputs
        inputs = NeedInput(category=category, condition_grade=condition_grade)
        cat = inputs.category
        grade = inputs.condition_grade

        mock_organizations = self._get_mock_organizations()
        condition_rank = {"Like New": 3, "Good": 2, "Fair": 1, "Poor": 0}
        item_rank = condition_rank.get(grade, 0)

        matches = []
        for org in mock_organizations:
            category_match = cat.lower() in [n.lower() for n in org["needs"]]
            min_cond = org["min_condition"]
            min_rank = condition_rank.get(min_cond, 0)

            if category_match and item_rank >= min_rank:
                # Calculate transparent score: base rank percentage plus a bonus for exceeding min requirement
                # Max score is 100.0
                raw_score = (item_rank / 3.0) * 100.0
                score = round(min(100.0, max(0.0, raw_score)), 2)

                priority = "High" if item_rank > min_rank else "Medium"
                reason = f"Category '{cat}' matches organization needs. Item condition '{grade}' meets or exceeds the minimum required condition '{min_cond}'."

                matches.append(NeedMatch(
                    organization_id=org["id"],
                    organization_name=org["name"],
                    priority=priority,
                    match_score=score,
                    reason=reason,
                    location=org.get("location"),
                    missing_information=["specific_quantity_required", "preferred_pickup_time"]
                ))

        # Rank matches by score descending
        matches.sort(key=lambda x: x.match_score, reverse=True)

        result_model = NeedResult(matches=matches)
        return result_model.model_dump()
=======
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
>>>>>>> origin/member1-frontend-ui
