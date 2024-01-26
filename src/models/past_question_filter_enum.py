"""Past question filter type."""
from enum import Enum


class PastQuestionFilter(Enum):
    """Past question filter type."""

    PAST_QUESTION_ID = "past_question_id"
    COURSE_CODE = "course_code"
    COURSE_NAME = "course_name"
    LECTURER_NAME = "lecturer_name"
    SEMESTER = "semester"
    YEAR = "year"
