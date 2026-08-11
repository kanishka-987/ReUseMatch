# Schemas for LogisticsAgent

# Placeholder structure for logistics evaluation data
logistics_schema = {
    "type": "object",
    "properties": {
        "origin": {"type": "string"},
        "destination": {"type": "string"},
        "distance_km": {"type": "number"},
        "estimated_cost_usd": {"type": "number"},
        "recommended_mode": {"type": "string"},
        "route_status": {"type": "string"}
    }
}
