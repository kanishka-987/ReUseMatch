from enum import Enum
from typing import Dict, Set

class PassportStatus(str, Enum):
    """
    Standard lifecycle statuses for a Digital Reuse Passport.
    """
    ANALYZED = "ANALYZED"
    AVAILABLE = "AVAILABLE"
    MATCHED = "MATCHED"
    RESERVED = "RESERVED"
    TRANSFERRED = "TRANSFERRED"
    REUSED = "REUSED"
    REFURBISHMENT_REQUIRED = "REFURBISHMENT_REQUIRED"
    RECYCLING = "RECYCLING"

# Configurable permitted state transition rules
DEFAULT_TRANSITION_RULES: Dict[PassportStatus, Set[PassportStatus]] = {
    PassportStatus.ANALYZED: {
        PassportStatus.AVAILABLE,
        PassportStatus.REFURBISHMENT_REQUIRED,
        PassportStatus.RECYCLING
    },
    PassportStatus.REFURBISHMENT_REQUIRED: {
        PassportStatus.AVAILABLE,
        PassportStatus.RECYCLING
    },
    PassportStatus.AVAILABLE: {
        PassportStatus.MATCHED,
        PassportStatus.RECYCLING
    },
    PassportStatus.MATCHED: {
        PassportStatus.RESERVED,
        PassportStatus.AVAILABLE,  # Match declined, back to active pool
        PassportStatus.RECYCLING
    },
    PassportStatus.RESERVED: {
        PassportStatus.TRANSFERRED,
        PassportStatus.AVAILABLE,  # Reservation canceled/timed out
        PassportStatus.RECYCLING
    },
    PassportStatus.TRANSFERRED: {
        PassportStatus.REUSED,
        PassportStatus.RECYCLING
    },
    PassportStatus.REUSED: {
        PassportStatus.ANALYZED,    # Device re-donated / secondary lifecycle
        PassportStatus.RECYCLING
    },
    PassportStatus.RECYCLING: set() # Terminal state
}
