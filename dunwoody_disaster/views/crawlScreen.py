from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QColor, QFont, QPainter, QKeyEvent
from PySide6.QtWidgets import QWidget
from dunwoody_disaster import AUDIO
import dunwoody_disaster as DD
import pygame
from typing import Callable


class Crawl(QWidget):
    def __init__(self):
        super().__init__()
        self.setupMusicPlayer()
        
        self._finishCallback = DD.unimplemented
        self.text_lines = [
            "In a distant galaxy, in an era of peace and prosperity...",
            "",
            "Unexpected turmoil has emerged.",
            "Factions once united now stand divided,",
            "threatening the stability of the galaxy.",
            "",
            "A small group of brave individuals",
            "seeks to restore harmony and justice.",
            "Their journey will test their resolve,",
            "challenge their beliefs, and",
            "shape the fate of the cosmos.",
            "",
            "This is their story...",
            "",
        ]

        self.line_spacing = 30
        self.scroll_speed = 1  # Adjust the scrolling speed as needed
        self.scroll_position = 0
        self.initUI()

    def setupMusicPlayer(self):
        try:
            pygame.mixer.init()
            print("Mixer initialized.")
            pygame.mixer.music.load(AUDIO["CrawlMusic"])
            print("Music file loaded.")
            pygame.mixer.music.set_volume(1.0)
            pygame.mixer.music.play(-1)
            print("Music playback started.")
        except Exception as e:
            print("Failed to initialize music playback:", e)

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
        self.deleteLater()

    def onFinish(self, callback: Callable):
        pygame.mixer.music.stop()  # Stop the music when the crawl is finished
        self._finishCallback = callback
