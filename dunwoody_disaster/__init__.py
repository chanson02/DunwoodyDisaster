from PySide6.QtWidgets import QSpacerItem, QSizePolicy, QWidget
from PySide6.QtCore import QObject, Signal, QEvent, SignalInstance
import os

ASSETS = {}
# I think this will make it so you can run main.py from anywhere --Cooper
asset_dir = os.path.join(os.path.dirname(__file__), "assets")
for fname in os.listdir(asset_dir):
    path = os.path.join(asset_dir, fname)
    if os.path.isfile(path) and "." in fname:
        key = os.path.splitext(fname)[0]
        ASSETS[key] = path


def asset(path: str) -> str:
    """
    Get an asset name from a path
    """
    return os.path.splitext(os.path.basename(path))[0]


def spacer(height: int) -> QSpacerItem:
    """
    Create an invisible vertical spacer to separate UI elements.
    """
    return QSpacerItem(0, height, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)


def expander(horizontal: bool, vertical: bool) -> QSpacerItem:
    """
    Create a spacer that will grow as large as possible horizontally or vertically
    """
    if horizontal:
        h_policy = QSizePolicy.Policy.MinimumExpanding
    else:
        h_policy = QSizePolicy.Policy.Fixed
    if vertical:
        v_policy = QSizePolicy.Policy.MinimumExpanding
    else:
        v_policy = QSizePolicy.Policy.Fixed
    return QSpacerItem(0, 0, h_policy, v_policy)

def unimplemented(*_, **k):
    _ = k
    """
    Use this as a default callback
    """
    raise Exception("This function is unimplemented")


# https://wiki.python.org/moin/PyQt/Making%20non-clickable%20widgets%20clickable
def clickable(widget: QWidget) -> SignalInstance:
    """
    Turn any QWidget into a clickable object.
    :example: clickable(QLabel('Hello')).connect(lambda: print('clicked'))
    """

    class Filter(QObject):
        clicked = Signal()

        def eventFilter(self, watched: QObject, event: QEvent) -> bool:
            if watched == widget:
                if event.type() == QEvent.Type.MouseButtonRelease:
                    if widget.rect().contains(event.pos()):
                        self.clicked.emit()
                        return True
            return False

    filter = Filter(widget)
    widget.installEventFilter(filter)
    return filter.clicked
