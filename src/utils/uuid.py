"""Generate uuid"""

import uuid


def generate_n_digit_uuid(value: int) -> str:
    """Generate n digit uuid"""
    return str(uuid.uuid4().hex[:value])
