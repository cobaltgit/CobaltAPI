from os import cpu_count
from pathlib import Path

APP = "cobaltapi:COBALTAPI"
"""Import string for the FastAPI app."""


HOST = "127.0.0.1"
"""The host to listen at."""
PORT = 8000
"""The port to listen at."""
WORKERS = cpu_count() * 2 + 1
"""The number of workers to use."""

DEBUG = True
"""Whether to run in debug mode."""
ACCESS_LOG = True
"""Whether to log access."""

ROOT_PATH = Path(__file__).parent
"""The root path of the project."""
FILES_ROOT = ROOT_PATH / "cobaltapi" / "files"
"""Root path for all files."""
FACTS_PATH = FILES_ROOT / "facts.txt"
"""The path to the facts file."""


try:
    from private_settings import *  # type: ignore

except ImportError:
    from warnings import warn

    warn("No `private_settings.py` found!")
