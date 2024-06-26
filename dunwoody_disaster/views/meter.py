"""
https://doc.qt.io/qtforpython-6/PySide6/QtGui/QPainter.html#PySide6.QtGui.PySide6.QtGui.QPainter.fillRect
https://doc.qt.io/qtforpython-6/examples/example_widgets_painting_painter.html
"""

from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPainter, QColor, QPaintEvent
from PySide6.QtCore import QTimer
from typing import Optional


class Meter(QWidget):
    def __init__(self, color: QColor, percentage=0):
        super().__init__()
        self._endColor: Optional[QColor] = None
        self.setColor(color)
        self.animated = True
        self.animationTimer = QTimer()
        self.animationTimer.timeout.connect(self.nextFrame)

        self._prevPercentage = 0
        self._percentage = 0
        self.setPercentage(percentage)

    def setColor(self, color: QColor):
        self._color = color

    def setEndColor(self, color: QColor):
        self._endColor = color

    def setPercentage(self, percentage: int | float):
        self._prevPercentage = self._percentage
        self._percentage = max(0, min(percentage, 100))

        diff = max(1, self._prevPercentage - self._percentage)
        if self.animated:
            self.animationTimer.start(int(750 // diff))
        else:
            self.update()
        return

    def nextFrame(self):
        if self._prevPercentage < self._percentage or self._prevPercentage == 1:
            self.animationTimer.stop()

        self._prevPercentage -= 1
        self.update()
        return

    def interpolateColor(self, thresh: int = 80) -> QColor:
        """
        :param thresh: Do not interpolate color if the percentage is lower than this value
        """
        if self._endColor is None or self._percentage < thresh:
            return self._color
        r = (
            int((self._endColor.red() - self._color.red()) * self._percentage / 100)
            + self._color.red()
        )
        g = (
            int((self._endColor.green() - self._color.green()) * self._percentage / 100)
            + self._color.green()
        )
        b = (
            int((self._endColor.blue() - self._color.blue()) * self._percentage / 100)
            + self._color.blue()
        )
        return QColor(r, g, b)

    def paintEvent(self, event: QPaintEvent):
        super().paintEvent(event)
        painter = QPainter(self)
        prev_color = QColor(255, 165, 0)

        for_color = self.interpolateColor()
        bkg_color = QColor(20, 0, 20)

        w = self.width()
        h = self.height()
        border = min(int(h * 0.05), 15)

        max_fill_width = w - 2 * border
        fill_h = int(h - 2 * border)
        fill_w = int(max_fill_width * self._percentage / 100)

        diff = 1 - abs(self._percentage - self._prevPercentage) / 100
        prev_w = int(max_fill_width * self._prevPercentage / 100)
        prev_h = max(5, int(fill_h * diff))
        prev_y = border + (fill_h - prev_h) // 2

        painter.fillRect(0, 0, w, h, bkg_color)
        if self.animated:
            painter.fillRect(border, prev_y, prev_w, prev_h, prev_color)
        painter.fillRect(border, border, fill_w, fill_h, for_color)
