"""Test fixture with attribute access."""

import os
from pathlib import Path

# Attribute access on imports
path = os.path.join("a", "b")
home = Path.home()
