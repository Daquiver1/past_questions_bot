import platform


def get_file_separator() -> str:
    """Return the appropriate file path separator based on the operating system."""
    if platform.system() == "Windows":
        return "\\"
    else:
        return "/"
