"""Make Studio filesystem assertions available to each skill test suite."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "tests"))
