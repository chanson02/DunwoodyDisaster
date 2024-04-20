from PySide6.QtCore import Qt
from PySide6.QtWidgets import QGridLayout, QWidget, QLabel
from PySide6.QtGui import QPixmap, QKeyEvent, QPainter, QMouseEvent

import dunwoody_disaster as DD
from dunwoody_disaster.CharacterFactory import Character, CharacterFactory
from typing import Optional


class MapScreen(QWidget):
    def __init__(self, character: Character, entryPoint: Optional[tuple[int, int]]):
        super().__init__()
        self.character = character
        self.image = DD.ASSETS['no_texture']
        self.rooms = []

        if entryPoint:
            self.char_pos = entryPoint
        else:
            self.char_pos = (-1, 0)

        self.init_ui()

    def init_ui(self):
        layout = QGridLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        self.map = QLabel()
        self.map.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        self.move_character(-1, 0)
        layout.addWidget(self.map)

    def setAsset(self, asset: str):
        self.image = DD.ASSETS[asset]
        self.move_character(self.char_pos[0], self.char_pos[1])

    def addRoom(self, name: Optional[str], pos: tuple[int, int], NPC: Character):
        room = {
                'name': name,
                'coordinate': pos,
                'NPC': NPC
                }
        self.rooms.append(room)

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
        self.char_pos = (x, y)
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
        return QPixmap(self.image)

    def serialize(self) -> dict:
        result = {
                'asset': DD.asset(self.image),
                'entry_point': None,
                'rooms': []
                }

        for room in self.rooms:
            NPC = room['NPC'].serialize()
            result['rooms'].append({
                'name': room['name'],
                'coordinate': room['coordinate'],
                'NPC': NPC
                })

        return result

    @staticmethod
    def from_json(json: dict, char: Character) -> "MapScreen":
        ep = (json['entry_point'][0], json['entry_point'][1])
        map = MapScreen(char, ep)
        map.setAsset(json['asset'])

        for room in json['rooms']:
            NPC = CharacterFactory.createFromJson(room['NPC'])
            point = (room['coordinate'][0], room['coordinate'][1])
            map.addRoom(room['name'], point, NPC)

        return map
