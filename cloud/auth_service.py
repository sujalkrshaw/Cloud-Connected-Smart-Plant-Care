"""Development authentication boundary. Production should use a real identity provider and per-device credentials."""
import os

def validate_api_key(candidate: str | None) -> bool:
    expected = os.getenv('API_KEY', 'dev-plant-api-key')
    return bool(candidate) and candidate == expected
