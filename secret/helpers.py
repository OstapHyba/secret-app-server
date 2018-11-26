from datetime import datetime

def is_expired(instance_datetime, minutes):
    now_minutes = datetime.utcnow().timestamp() / 60
    instance_minutes = instance_datetime.timestamp() / 60

    if now_minutes - instance_minutes < minutes:
        return False
    return True