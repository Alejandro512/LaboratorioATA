from datetime import datetime
from typing import Optional

def sensor_document(data: dict) -> dict:
    return {
        "serial": data["serial"],
        "type": data["type"],
        "location": data["location"],
        "ownerUserId": data["ownerUserId"],
        "installedAt": data.get("installedAt", datetime.utcnow()),
        "status": data.get("status", "online"),
        "thresholds": data["thresholds"]
    }
