import re
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from backend.models.device import Device
from backend.models.recipient import Recipient

def parse_capacity_to_gb(val: Optional[str]) -> Optional[float]:
    """
    Parses strings like '16GB', '8 GB', '512MB', '1TB', '256GB SSD' into float GB values.
    Returns None if value cannot be parsed or is empty.
    """
    if not val:
        return None
    val_clean = str(val).strip().upper()
    match = re.search(r'(\d+(?:\.\d+)?)\s*(TB|GB|MB|KB)?', val_clean)
    if not match:
        return None
    number = float(match.group(1))
    unit = match.group(2) if match.group(2) else 'GB'
    
    if unit == 'TB':
        return number * 1024.0
    elif unit == 'GB':
        return number
    elif unit == 'MB':
        return number / 1024.0
    elif unit == 'KB':
        return number / (1024.0 * 1024.0)
    return number

class MatchingService:
    """
    Database-driven matching service comparing devices against recipient requirements.
    Calculates transparent, explainable match scores (0-100).
    """

    @staticmethod
    def match_device_to_recipients(device_id: str, db: Session) -> Dict[str, Any]:
        """
        Retrieves device by device_id and matches it against all recipients in the database.
        Returns ranked list of matching recipients with detailed scoring explanations.
        """
        device = db.query(Device).filter(Device.id == device_id).first()
        if not device:
            raise ValueError(f"Device with ID '{device_id}' not found")

        recipients = db.query(Recipient).all()
        
        matches = []
        dev_type = (device.device_type or "").strip().lower()
        dev_ram_gb = parse_capacity_to_gb(device.ram)
        dev_storage_gb = parse_capacity_to_gb(device.storage)

        for recipient in recipients:
            score = 0.0
            reasons = []

            # A. Mandatory Device Type Comparison (50 pts)
            rec_req_type = (recipient.required_device_type or "").strip().lower()
            type_matched = (dev_type == rec_req_type) and bool(dev_type)

            if not type_matched:
                # Device type mismatch: Exclude recipient from matches
                continue

            score += 50.0
            reasons.append(f"Device type '{device.device_type}' matches recipient required type '{recipient.required_device_type}' (+50 pts)")

            # B. RAM Comparison (15 pts)
            rec_ram_gb = parse_capacity_to_gb(recipient.minimum_ram)
            if rec_ram_gb is not None:
                if dev_ram_gb is not None and dev_ram_gb >= rec_ram_gb:
                    score += 15.0
                    ram_result = f"Satisfied: Device ({device.ram}) >= Requirement ({recipient.minimum_ram}) (+15 pts)"
                elif dev_ram_gb is not None:
                    ram_result = f"Failed: Device ({device.ram}) < Requirement ({recipient.minimum_ram}) (+0 pts)"
                else:
                    ram_result = f"Unverified: Device RAM unspecified, Requirement is ({recipient.minimum_ram}) (+0 pts)"
            else:
                score += 15.0
                ram_result = "Satisfied: No minimum RAM required by recipient (+15 pts)"
            reasons.append(f"RAM: {ram_result}")

            # C. Storage Comparison (15 pts)
            rec_storage_gb = parse_capacity_to_gb(recipient.minimum_storage)
            if rec_storage_gb is not None:
                if dev_storage_gb is not None and dev_storage_gb >= rec_storage_gb:
                    score += 15.0
                    storage_result = f"Satisfied: Device ({device.storage}) >= Requirement ({recipient.minimum_storage}) (+15 pts)"
                elif dev_storage_gb is not None:
                    storage_result = f"Failed: Device ({device.storage}) < Requirement ({recipient.minimum_storage}) (+0 pts)"
                else:
                    storage_result = f"Unverified: Device storage unspecified, Requirement is ({recipient.minimum_storage}) (+0 pts)"
            else:
                score += 15.0
                storage_result = "Satisfied: No minimum storage required by recipient (+15 pts)"
            reasons.append(f"Storage: {storage_result}")

            # D. Priority Scoring (20 / 10 / 5 pts)
            prio = (recipient.priority or "Medium").strip().upper()
            if prio == "HIGH":
                score += 20.0
                prio_pts = 20
            elif prio == "MEDIUM":
                score += 10.0
                prio_pts = 10
            else:
                score += 5.0
                prio_pts = 5
            reasons.append(f"Priority '{recipient.priority}' applied (+{prio_pts} pts)")

            matches.append({
                "recipient_id": recipient.id,
                "recipient_name": recipient.name,
                "recipient_type": recipient.recipient_type,
                "location": recipient.location,
                "match_score": round(score, 2),
                "matched_device_type": device.device_type,
                "type_matched": type_matched,
                "ram_requirement": recipient.minimum_ram,
                "ram_result": ram_result,
                "storage_requirement": recipient.minimum_storage,
                "storage_result": storage_result,
                "priority": recipient.priority,
                "reasons": reasons
            })

        # Rank matches from highest score to lowest score
        matches.sort(key=lambda x: x["match_score"], reverse=True)

        return {
            "device_id": device.id,
            "device_type": device.device_type,
            "brand": device.brand,
            "model": device.model,
            "total_candidates_evaluated": len(recipients),
            "matches_found": len([m for m in matches if m["type_matched"]]),
            "matches": matches
        }
