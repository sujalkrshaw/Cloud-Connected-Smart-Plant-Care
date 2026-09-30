"""Configurable demo plant profiles. Values are educational defaults, not horticultural prescriptions."""
PLANT_PROFILES = {
    'succulent': {'moisture_threshold': 20.0},
    'tomato': {'moisture_threshold': 40.0},
    'herb': {'moisture_threshold': 35.0},
    'indoor': {'moisture_threshold': 30.0},
}

def threshold_for(plant_type: str, fallback: float = 40.0) -> float:
    return float(PLANT_PROFILES.get(plant_type.lower(), {}).get('moisture_threshold', fallback))
