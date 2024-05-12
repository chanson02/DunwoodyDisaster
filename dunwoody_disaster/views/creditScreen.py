from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QColor, QFont, QPainter, QPixmap, QKeyEvent
from PySide6.QtWidgets import QWidget
import dunwoody_disaster as DD
from typing import Callable


class Credits(QWidget):
    def __init__(self):
        super().__init__()
        self._finishCallback = DD.unimplemented
        self.text_lines = [
            "Cooper",
            "Noah",
            "John",
            "Mitch",
        ]
        self.images = {
            "Cooper": DD.ASSETS["CooperRefined+"],
            "Noah": DD.ASSETS["NoahRefined+"],
            "John": DD.ASSETS["JohnRefined+"],
            "Mitch": DD.ASSETS["MitchRefined+"],
        }
        self.current_line = 0
        self.opacity = 0.0
        self.fade_in = True  # Control whether we are fading in or out
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Story Crawl")
        self.setGeometry(100, 100, 1920, 1080)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateOpacity)
        self.timer.start(100)  # 100 milliseconds for smooth transition
        self.show()

    def updateOpacity(self):
        if self.fade_in:
            if self.opacity < 1.0:
                self.opacity += 0.05
            else:
                self.fade_in = False
        else:
            if self.opacity > 0:
                self.opacity -= 0.05
            else:
                self.fade_in = True
                self.current_line += 1
                if self.current_line >= len(self.text_lines):
                    self.endCreditScreen()
                    return
        self.update()

    def paintEvent(self, event):
        if self.current_line >= len(self.text_lines):
            return
        line = self.text_lines[self.current_line]
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(Qt.black)
        painter.fillRect(self.rect(), Qt.black)
        painter.setOpacity(self.opacity)

        image = QPixmap(self.images[line])
        painter.drawPixmap(10, (self.height() - 200) / 2, 200, 200, image)

        font = QFont("Arial", 24)
        painter.setFont(font)
        painter.setPen(QColor(255, 255, 255))
        text_width = painter.fontMetrics().horizontalAdvance(line)
        x = self.width() / 2 + 100
        painter.drawText(x, (self.height() - painter.fontMetrics().height()) / 2, line)

    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key.Key_Enter or event.key() == Qt.Key.Key_Return:
            self.endCreditScreen()

    def endCreditScreen(self):
        self.timer.stop()
        if self._finishCallback:
            self._finishCallback()
        self.deleteLater()

    def onFinishCredits(self, callback: Callable):
        self._finishCallback = callback
