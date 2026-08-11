from typing import Set

VALID_CONDITIONS: Set[str] = {"EXCELLENT", "GOOD", "FAIR", "POOR", "NON_FUNCTIONAL"}

VALID_CATEGORIES: Set[str] = {
    "Laptop",
    "Desktop",
    "Monitor",
    "Smartphone",
    "Tablet",
    "Keyboard",
    "Mouse",
    "Printer",
    "Router",
    "Component",
    "Other"
}

def validate_condition_string(condition: str) -> str:
    """
    Validates that the condition is one of the supported grading strings.
    """
    upper_cond = condition.strip().upper()
    if upper_cond not in VALID_CONDITIONS:
        raise ValueError(
            f"Invalid condition: '{condition}'. Must be one of: {', '.join(sorted(VALID_CONDITIONS))}"
        )
    return upper_cond

def validate_device_category(category: str) -> str:
    """
    Validates that the category is one of the recognized circular economy device categories.
    """
    capitalized_cat = category.strip().capitalize()
    
    # Special casing for Smartphone/Desktop/Laptop to match case
    for valid_cat in VALID_CATEGORIES:
        if valid_cat.lower() == capitalized_cat.lower():
            return valid_cat
            
    raise ValueError(
        f"Invalid category: '{category}'. Recognized categories: {', '.join(sorted(VALID_CATEGORIES))}"
    )

def validate_score_range(score: float, factor_name: str) -> float:
    """
    Ensures that scores are strictly within 0 and 100.
    """
    if not (0.0 <= score <= 100.0):
        raise ValueError(f"Score for {factor_name} must be between 0 and 100. Received: {score}")
    return score
