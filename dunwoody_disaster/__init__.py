from PySide6.QtWidgets import QSpacerItem, QSizePolicy
import os

ASSETS = {}
# I think this will make it so you can run main.py from anywhere --Cooper
asset_dir = os.path.join(os.path.dirname(__file__), "assets")
for fname in os.listdir(asset_dir):
    path = os.path.join(asset_dir, fname)
    if os.path.isfile(path) and "." in fname:
        key = os.path.splitext(fname)[0]
        ASSETS[key] = path


def spacer(height: int) -> QSpacerItem:
    """
    Create an invisible vertical spacer to separate UI elements.
    """
    return QSpacerItem(0, height, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
