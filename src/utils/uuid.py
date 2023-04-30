"""Generate a 6 character uuid"""
import uuid


def generate_6_digits_uuid():
    """Generate 6 digit uuid"""
    return str(uuid.uuid4().hex[:6])
