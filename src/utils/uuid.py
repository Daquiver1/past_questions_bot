"""Generate a 10 character uuid"""
import uuid


def generate_10_digit_uuid():
    """Generate 6 digit uuid"""
    return str(uuid.uuid4().hex[:10])
