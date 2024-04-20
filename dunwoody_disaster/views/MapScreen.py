"""
The entry point for the game
"""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QGridLayout, QWidget, QLabel
from PySide6.QtGui import QPixmap, QKeyEvent, QPainter, QMouseEvent

import dunwoody_disaster as DD
from dunwoody_disaster.CharacterFactory import Character


class MapScreen(QWidget):
    def __init__(self, character: Character):
        super().__init__()
        self.character = character

        self.mainLayout = QGridLayout()
        self.mainLayout.setSpacing(0)
        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.mainLayout)

        self.map = QLabel()
        self.map.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        self.move_character(-1, 0)
        self.mainLayout.addWidget(self.map)

    def keyPressEvent(self, event: QKeyEvent):
        print("entering")
        if event.key() == Qt.Key.Key_Left:
            # self.currImgIndex = (self.currImgIndex - 1) % len(self.imagePaths)
            # self.mapPic.setPixmap(QPixmap(self.imagePaths[self.currImgIndex]))
            print("left")

        elif event.key() == Qt.Key.Key_Right:
            # self.currImgIndex = (self.currImgIndex + 1) % len(self.imagePaths)
            # self.mapPic.setPixmap(QPixmap(self.imagePaths[self.currImgIndex]))
            print("right")

    def move_character(self, x: int, y: int):
        if x < 0:
            self.map.setPixmap(self.pixmap())
            return

        map_pixmap = self.pixmap()
        painter = QPainter(map_pixmap)
        overlay = QPixmap(self.character.image()).scaledToWidth(80)
        painter.drawPixmap(x, y, overlay)
        painter.end()
        self.map.setPixmap(map_pixmap)
        self.repaint()

    def mousePressEvent(self, event: QMouseEvent):
        point = event.pos()
        print(point)
        self.move_character(point.x(), point.y())

    def pixmap(self):
        return QPixmap(DD.ASSETS["MainMap_Coop_bus"])
