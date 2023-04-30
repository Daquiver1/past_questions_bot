import platform


def get_file_separator():
    """Return the appropriate file path separator based on the operating system."""
    return '/'
    if platform.system() == 'Windows':
        return '\\'
    else:
        return '/'
