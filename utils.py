"""Small shared helpers for the football position classifier."""

POSITION_MAPPING = {
    "GK": "Goalkeeper",
    "CB": "Defender",
    "LB": "Defender",
    "RB": "Defender",
    "LWB": "Defender",
    "RWB": "Defender",
    "CDM": "Midfielder",
    "CM": "Midfielder",
    "CAM": "Midfielder",
    "LM": "Midfielder",
    "RM": "Midfielder",
    "ST": "Forward",
    "CF": "Forward",
    "LW": "Forward",
    "RW": "Forward",
}


def get_position_group(position: str | None) -> str | None:
    """Map a FIFA primary position to one of the four target classes."""
    if not isinstance(position, str):
        return None
    return POSITION_MAPPING.get(position.strip())
