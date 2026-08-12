class LogisticsAgent:
    """
    LogisticsAgent is responsible for calculating distances, optimal transportation modes,
    routes, and estimating delivery costs between donor and recipient locations.
    """
    def __init__(self):
        pass

    def evaluate_logistics(self, donor_location: str, recipient_location: str) -> dict:
        """
        Legacy routing evaluation method.
        """
        distance_km = 12.5  # mock value
        cost_est = round(distance_km * 1.5, 2)  # $1.50 per km
        
        return {
            "origin": donor_location,
            "destination": recipient_location,
            "distance_km": distance_km,
            "estimated_cost_usd": cost_est,
            "recommended_mode": "Local Pickup Courier" if distance_km < 30 else "Standard Shipping",
            "route_status": "optimal"
        }

    def run(self, donor_location: str, matches: list, lifecycle_action: str = "REUSE") -> dict:
        """
        Runs LogisticsAgent for each matched recipient. Skipped if action is RECYCLE or no matches.
        """
        if lifecycle_action == "RECYCLE":
            return {
                "status": "Skipped",
                "routes": [],
                "skip_reason": "Logistics calculation was bypassed because the lifecycle decision is RECYCLE."
            }

        if not matches:
            return {
                "status": "Skipped",
                "routes": [],
                "skip_reason": "Logistics skipped because no matching recipient was found."
            }

        routes = []
        for match in matches:
            recipient_loc = match.get("location") or f"{match['organization_name']} Center, Downtown"
            route_info = self.evaluate_logistics(donor_location, recipient_loc)
            routes.append(route_info)

        return {
            "status": "Success",
            "routes": routes,
            "skip_reason": None
        }
