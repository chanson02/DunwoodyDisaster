from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QColor, QFont, QPainter, QKeyEvent
from PySide6.QtWidgets import QWidget
import dunwoody_disaster as DD
from typing import Callable


class Crawl(QWidget):
    def __init__(self):
        super().__init__()
        self._finishCallback = DD.unimplemented
        self.text_lines = [
            "Filled with hope and the dream of becoming software engineers,",
            "four students will undertake a new journey each excited at the",
            "prospect of starting a new chapter in their lives.",
            "",
            "During their time at Dunwoody, they will experience a new form of education.",
            "An education devoid of thought, planning, or reason whose sole purpose is to",
            "burden unsuspecting students with financial strife while providing few avenues",
            "for employment. ",
            "",
            "Now, these four students must band together, united under one front, to dismantle",
            "the system that has crippled them financially, but provided so little in return. ",
            "",
            "This is their story...",
        ]
        self.line_spacing = 30
        self.scroll_speed = 0.51  # Adjust the scrolling speed as needed
        self.scroll_position = 0
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Story Crawl")
        self.setGeometry(100, 100, 1920, 1080)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateScroll)
        self.timer.start(10)  # Adjust the interval for smoother or faster scrolling
        self.show()

    def updateScroll(self):
        self.scroll_position += self.scroll_speed
        if (
            self.scroll_position
            >= len(self.text_lines) * self.line_spacing + self.height()
        ):
            self.endCrawlScreen()  # Once scrolling is done, callback and go to next screen.
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(Qt.black)
        painter.fillRect(self.rect(), Qt.black)

        font = QFont("Arial", 20)
        font.setBold(True)
        painter.setFont(font)
        painter.setPen(QColor(255, 255, 255))

        y = self.height() - self.scroll_position

        for line in self.text_lines:
            text_width = painter.fontMetrics().horizontalAdvance(line)
            x = (self.width() - text_width) / 2
            painter.drawText(x, y, line)
            y += self.line_spacing

    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key.Key_Enter or event.key() == Qt.Key.Key_Return:
            self.endCrawlScreen()

    def endCrawlScreen(self):
        self.timer.stop()
        self._finishCallback
        # Call the callback function to go to the next screen
        if self._finishCallback:
            self._finishCallback()
        self.deleteLater()

    def onFinish(self, callback: Callable):
        self._finishCallback = callback
