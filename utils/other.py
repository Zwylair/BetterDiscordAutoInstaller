import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="(%(asctime)s) %(message)s")


def backslash_path(path: str) -> str:
    """Replaces two slashes (\\) with a backslash (/)"""
    return path.replace("\\", "/")
