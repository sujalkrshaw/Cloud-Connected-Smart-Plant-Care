"""Pure decision helper used for explaining/testing watering policy."""

def should_water(*, moisture: float, threshold: float, tank_level: float, cooldown_complete: bool, hourly_events: int, max_events_per_hour: int = 4) -> bool:
    return (
        moisture < threshold
        and tank_level >= 10
        and cooldown_complete
        and hourly_events < max_events_per_hour
    )
