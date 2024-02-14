"""Generate past question unique code."""

import hashlib

from src.models.past_questions import PastQuestionCreate


def generate_pasco_unique_code(past_question: PastQuestionCreate) -> str:
    """Generate a hashed unique code for a past question."""
    base_string = f"{past_question.course_code.lower()}{past_question.course_name.lower()}{past_question.semester.lower()}{past_question.year}"

    normalized_string = base_string.replace(" ", "").lower()

    hash_object = hashlib.sha256()
    hash_object.update(normalized_string.encode("utf-8")) 
    hashed_code = hash_object.hexdigest()

    return hashed_code
