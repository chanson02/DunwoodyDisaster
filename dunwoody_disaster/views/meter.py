"""
https://doc.qt.io/qtforpython-6/PySide6/QtGui/QPainter.html#PySide6.QtGui.PySide6.QtGui.QPainter.fillRect
https://doc.qt.io/qtforpython-6/examples/example_widgets_painting_painter.html
"""

from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPainter, QColor, QPaintEvent
from typing import Optional


class Meter(QWidget):
    def __init__(self, color: QColor, percentage=0):
        super().__init__()
        self._endColor: Optional[QColor] = None
        self.setColor(color)
        self.setPercentage(percentage)

    def setColor(self, color: QColor):
        self._color = color

    def setEndColor(self, color: QColor):
        self._endColor = color

    def setPercentage(self, percentage: int | float):
        self._percentage = max(0, min(percentage, 100))
        self.update()

    def interpolateColor(self, thresh: int = 80) -> QColor:
        """
        :param thresh: Do not interpolate color if the percentage is lower than this value
        """
        if self._endColor is None or self._percentage < thresh:
            return self._color
        r = int((self._endColor.red() - self._color.red()) * self._percentage / 100) + self._color.red()
        g = int((self._endColor.green() - self._color.green()) * self._percentage / 100) + self._color.green()
        b = int((self._endColor.blue() - self._color.blue()) * self._percentage / 100) + self._color.blue()
        return QColor(r, g, b)

    def paintEvent(self, event: QPaintEvent):
        super().paintEvent(event)
        painter = QPainter(self)
        for_color = self.interpolateColor()
        bkg_color = QColor(20, 0, 20)

        w = self.width()
        h = self.height()
        border = min(int(h * 0.05), 15)

        max_fill_width = w - 2 * border
        fill_h = int(h - 2 * border)
        fill_w = int(max_fill_width * self._percentage / 100)

        painter.fillRect(0, 0, w, h, bkg_color)
        painter.fillRect(border, border, fill_w, fill_h, for_color)
