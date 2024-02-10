"""Get bot name."""

import os

from fastapi import UploadFile

from src.utils.uuid import generate_n_digit_uuid


def create_object_name(past_question_file: UploadFile) -> str:
    """Create name of past question."""
    key = generate_n_digit_uuid(6)

    original_filename = past_question_file.filename

    base_name, _ = os.path.splitext(original_filename)

    new_filename = f"{base_name}{key}.pdf"

    return new_filename
