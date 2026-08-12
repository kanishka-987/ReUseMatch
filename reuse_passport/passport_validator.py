import re
from datetime import datetime
from typing import Dict, Set, Optional
from .passport import DigitalReusePassport, StatusHistoryEntry
from .passport_status import PassportStatus, DEFAULT_TRANSITION_RULES

class PassportValidator:
    """
    Enforces structural, range, and lifecycle transition validations on DigitalReusePassports.
    """
    def __init__(self, transition_rules: Dict[PassportStatus, Set[PassportStatus]] = None):
        self.transition_rules = transition_rules or DEFAULT_TRANSITION_RULES.copy()

    def validate_structure(self, passport: DigitalReusePassport) -> bool:
        """
        Validates ranges, format rules, and structure elements.
        Throws ValueError on discrepancy, otherwise returns True.
        """
        # Validate Passport ID format: RM-PASS-YYYY-XXXXXX
        id_pattern = r"^RM-PASS-\d{4}-\d{6}$"
        if not re.match(id_pattern, passport.passport_id):
            raise ValueError(
                f"Invalid Passport ID format: '{passport.passport_id}'. Must match pattern: RM-PASS-YYYY-XXXXXX"
            )

        # Validate score ranges
        if not (0.0 <= passport.reuse_score <= 100.0):
            raise ValueError(f"Reuse score out of bounds (0-100): {passport.reuse_score}")
            
        if not (0.0 <= passport.repairability_score <= 100.0):
            raise ValueError(f"Repairability score out of bounds (0-100): {passport.repairability_score}")
            
        if not (0.0 <= passport.analysis_confidence <= 1.0):
            raise ValueError(f"Confidence score out of bounds (0-1): {passport.analysis_confidence}")

        # Validate reusable component structure
        for comp in passport.reusable_components:
            required_keys = {"component_name", "condition", "reusable", "repairable", "estimated_value"}
            missing_keys = required_keys - set(comp.keys())
            if missing_keys:
                raise ValueError(
                    f"Component entry for '{comp.get('component_name', 'Unknown')}' is missing keys: {missing_keys}"
                )

        # Validate component recovery structure
        for rec in passport.component_recovery:
            required_keys = {
                "component", "potential_score", "potential_level", 
                "confidence_score", "confidence_level", "assessment_status"
            }
            missing_keys = required_keys - set(rec.keys())
            if missing_keys:
                raise ValueError(
                    f"Component recovery entry for '{rec.get('component', 'Unknown')}' is missing keys: {missing_keys}"
                )

        return True

    def is_transition_allowed(self, from_status: PassportStatus, to_status: PassportStatus) -> bool:
        """
        Checks if a status transition is permitted based on the active state transition graph.
        """
        allowed_states = self.transition_rules.get(from_status, set())
        return to_status in allowed_states

    def update_status(
        self, 
        passport: DigitalReusePassport, 
        new_status: PassportStatus, 
        description: str
    ) -> DigitalReusePassport:
        """
        Verifies and transitions a passport to a new lifecycle status.
        Appends the event to the history log and updates timestamps.
        Throws ValueError if the transition is prohibited.
        """
        current_state = passport.current_status
        
        # Enforce lifecycle transition path validation
        if not self.is_transition_allowed(current_state, new_status):
            allowed_list = [s.value for s in self.transition_rules.get(current_state, set())]
            raise ValueError(
                f"Forbidden state transition: Cannot change status from '{current_state.value}' to '{new_status.value}'. "
                f"Allowed target transitions from '{current_state.value}': {allowed_list or 'None'}"
            )

        # Apply state transition
        current_time = datetime.utcnow().isoformat() + "Z"
        passport.current_status = new_status
        passport.last_updated_date = current_time
        
        passport.status_history.append(
            StatusHistoryEntry(
                status=new_status,
                timestamp=current_time,
                description=description
            )
        )
        
        return passport
