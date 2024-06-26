from PySide6.QtWidgets import (
    QSpacerItem,
    QSizePolicy,
    QWidget,
    QScrollArea,
    QLayout,
    QVBoxLayout,
)
from PySide6.QtGui import QPixmap, QPainter
from PySide6.QtCore import QObject, Signal, QEvent, SignalInstance, Qt
import os
from typing import Callable

BASE_PATH = os.path.dirname(__file__)

ASSETS = {}
# I think this will make it so you can run main.py from anywhere --Cooper
asset_dir = os.path.join(BASE_PATH, "assets")
for fname in os.listdir(asset_dir):
    path = os.path.join(asset_dir, fname)
    if os.path.isfile(path) and "." in fname:
        key = os.path.splitext(fname)[0]
        ASSETS[key] = path

AUDIO = {}
# I think this will make it so you can run main.py from anywhere --Cooper
audio_dir = os.path.join(BASE_PATH, "audio")
for fname in os.listdir(audio_dir):
    path = os.path.join(audio_dir, fname)
    if os.path.isfile(path) and "." in fname:
        key = os.path.splitext(fname)[0]
        AUDIO[key] = path


def audio(path: str) -> str:
    """
    Get an audio name from a path
    """
    return os.path.splitext(os.path.basename(path))[0]


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


def expander(horizontal: bool, vertical: bool, min=10) -> QSpacerItem:
    """
    Create a spacer that will grow as large as possible horizontally or vertically
    :param min: Minimum distance to space
    """
    h_policy = QSizePolicy.Policy.Fixed
    width = 0
    v_policy = QSizePolicy.Policy.Fixed
    height = 0
    if horizontal:
        h_policy = QSizePolicy.Policy.MinimumExpanding
        width = min
    if vertical:
        v_policy = QSizePolicy.Policy.MinimumExpanding
        height = min

    return QSpacerItem(width, height, h_policy, v_policy)


def scroller(child: QLayout, horizontal: bool, vertical: bool) -> QScrollArea:
    """
    :return: a QScrollArea(QWidget)
    """
    child.setSpacing(0)
    child.setContentsMargins(0, 0, 0, 0)

    h_policy = Qt.ScrollBarPolicy.ScrollBarAlwaysOff
    v_policy = Qt.ScrollBarPolicy.ScrollBarAlwaysOff
    if horizontal:
        h_policy = Qt.ScrollBarPolicy.ScrollBarAsNeeded
    if vertical:
        v_policy = Qt.ScrollBarPolicy.ScrollBarAsNeeded

    result = QScrollArea()
    result.setContentsMargins(0, 0, 0, 0)
    result.setWidgetResizable(True)
    result.setHorizontalScrollBarPolicy(h_policy)
    result.setVerticalScrollBarPolicy(v_policy)

    widget = QWidget()
    widget.setLayout(child)
    result.setWidget(widget)
    return result


def layout(widget: QWidget) -> QLayout:
    """
    Convert a widget to a layout
    """
    layout = QVBoxLayout()
    layout.setSpacing(0)
    layout.setContentsMargins(0, 0, 0, 0)
    layout.addWidget(widget)
    return layout


def clear_layout(layout: QLayout):
    """
    Clear all widgets inside layout from screen
    """
    for i in reversed(range(layout.count())):
        widget = layout.itemAt(i).widget()
        layout.removeWidget(widget)
        widget.setParent(None)


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


def overlay(base: QPixmap, overlay: QPixmap, position: tuple[int, int]) -> QPixmap:
    painter = QPainter(base)
    painter.drawPixmap(position[0], position[1], overlay)
    painter.end()
    return base


# Copy and pasted from python3.12/typing.py
def override(method: Callable, /) -> Callable:
    """Indicate that a method is intended to override a method in a base class.

    Usage::

        class Base:
            def method(self) -> None:
                pass

        class Child(Base):
            @override
            def method(self) -> None:
                super().method()

    When this decorator is applied to a method, the type checker will
    validate that it overrides a method or attribute with the same name on a
    base class.  This helps prevent bugs that may occur when a base class is
    changed without an equivalent change to a child class.

    There is no runtime checking of this property. The decorator attempts to
    set the ``__override__`` attribute to ``True`` on the decorated object to
    allow runtime introspection.

    See PEP 698 for details.
    """
    try:
        method.__override__ = True
    except (AttributeError, TypeError):
        # Skip the attribute silently if it is not writable.
        # AttributeError happens if the object has __slots__ or a
        # read-only property, TypeError if it's a builtin class.
        pass
    return method
