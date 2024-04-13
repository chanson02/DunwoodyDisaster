"""
https://doc.qt.io/qtforpython-6/PySide6/QtGui/QPainter.html#PySide6.QtGui.PySide6.QtGui.QPainter.fillRect
https://doc.qt.io/qtforpython-6/examples/example_widgets_painting_painter.html
"""

from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPainter, QColor, QPaintEvent


class Meter(QWidget):
    def __init__(self, color: QColor, percentage=0):
        super().__init__()
        self.setColor(color)
        self.setPercentage(percentage)

    def setColor(self, color: QColor):
        self._color = color

    def setPercentage(self, percentage: int | float):
        self._percentage = max(0, min(percentage, 100))
        self.update()

    def paintEvent(self, event: QPaintEvent):
        super().paintEvent(event)
        painter = QPainter(self)
        bkg_color = QColor(20, 0, 20)

        w = self.width()
        h = self.height()
        border = min(int(h * 0.05), 15)

        max_fill_width = w - 2 * border
        fill_h = int(h - 2 * border)
        fill_w = int(max_fill_width * self._percentage / 100)

        painter.fillRect(0, 0, w, h, bkg_color)
        painter.fillRect(border, border, fill_w, fill_h, self._color)
