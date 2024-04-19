"""
The entry point for the game
"""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QGridLayout, QWidget, QLabel
from PySide6.QtGui import QPixmap, QKeyEvent
from typing import Callable
from dunwoody_disaster import ASSETS


class MapScreen(QWidget):
    """ """

    def __init__(self, callToMain: Callable):
        super().__init__()
        self.fighCallback = callToMain
        self.mainLayout = QGridLayout(spacing=0)
        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.mainLayout)

        self.mapPic = QLabel("")
        self.mapPic.setPixmap(QPixmap(ASSETS["CourtYard"]))
        self.mainLayout.addWidget(self.mapPic, 0, 0)

        self.imagePaths = [
            ASSETS[img]
            for img in ["CourtYard", "LectureHall", "Physics", "Science Lab"]
        ]

        self.currImgIndex = 0

    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key_Left:
            self.currImgIndex = (self.currImgIndex - 1) % len(self.imagePaths)
            self.mapPic.setPixmap(QPixmap(self.imagePaths[self.currImgIndex]))
            print("left")

        elif event.key() == Qt.Key.Key_Right:
            self.currImgIndex = (self.currImgIndex + 1) % len(self.imagePaths)
            self.mapPic.setPixmap(QPixmap(self.imagePaths[self.currImgIndex]))
            print("right")

        elif event.key() == Qt.Key_Return:
            self.fighCallback()
            pass
