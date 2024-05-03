from PySide6.QtWidgets import QWidget, QLabel, QGridLayout, QSpacerItem, QSizePolicy
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QPixmap, QKeyEvent, QPainter, QMouseEvent

from dunwoody_disaster.views.FightPreview import FightPreview
import dunwoody_disaster as DD
from dunwoody_disaster.CharacterFactory import Character, CharacterFactory
from typing import Optional, Callable
from math import sqrt


class Map(QLabel):

    backgroundImageChanged = Signal(str)

    def __init__(
        self, character: Character, entryPoint: Optional[tuple[int, int]] = None
    ):
        super().__init__()
        self.character = character
        self.image = DD.ASSETS["no_texture"]
        self.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        self.rooms = []
        self.current_room: Optional[dict] = None
        self.roomChanged = DD.unimplemented

        if entryPoint:
            self.char_pos = entryPoint
        else:
            self.char_pos = (-1, 0)

    def onRoomChange(self, callback: Callable):
        self.roomChanged = callback

    def setRoom(self, room: Optional[dict]):
        if self.current_room == room:
            return

        self.current_room = room
        if self.current_room:
            pos = self.current_room["coordinate"]
            self.moveCharacter(pos[0], pos[1])

        self.roomChanged(self.current_room)

    def mousePressEvent(self, ev: QMouseEvent):
        point = ev.pos()
        new_room = self.findClosestRoom(point.x(), point.y())
        self.setRoom(new_room)

    def findClosestRoom(self, x: int, y: int) -> Optional[dict]:
        closest = None
        min_dist = float("inf")
        unbeaten = [r for r in self.rooms if r["NPC"].curHealth > 0]

        for room in unbeaten:
            room_pos = room["coordinate"]
            distance = sqrt((x - room_pos[0]) ** 2 + (y - room_pos[1]) ** 2)
            if distance < min_dist:
                min_dist = distance
                closest = room

        return closest

    def moveCharacter(self, x: int, y: int):
        self.char_pos = (x, y)
        if x < 0:
            self.setPixmap(self.pixmap())
            return

        map_pixmap = self.pixmap()
        painter = QPainter(map_pixmap)
        overlay = QPixmap(self.character.image()).scaledToWidth(80)
        painter.drawPixmap(x, y, overlay)
        painter.end()
        self.setPixmap(map_pixmap)
        self.repaint()

    def addRoom(
        self,
        name: Optional[str],
        pos: tuple[int, int],
        NPC: Character,
        battlefield: str,
    ):
        room = {
            "name": name,
            "coordinate": pos,
            "battlefield": DD.ASSETS[battlefield],
            "NPC": NPC,
        }
        self.rooms.append(room)

    def pixmap(self):
        return QPixmap(self.image).scaledToWidth(750)  # original size 1024x1024

    def setAsset(self, asset: str):
        self.image = DD.ASSETS[asset]
        self.moveCharacter(self.char_pos[0], self.char_pos[1])
        self.backgroundImageChanged.emit(self.image)

    @staticmethod
    def buildMap(char: Character) -> "Map":
        chars = CharacterFactory
        map = Map(char)
        map.setAsset("MainMap")
        map.addRoom("Bus Stop", (419, 700), chars.JoeAxberg(), "Science Lab")
        map.addRoom("Court Yard", (693, 559), chars.LeAnnSimonson(), "CourtYard")
        map.addRoom("Commons", (451, 449), chars.RyanRengo(), "Science Lab")
        map.addRoom("Math", (236, 359), chars.NoureenSajid(), "Physics")
        map.addRoom("English", (770, 366), chars.AmalanPulendran(), "LectureHall")
        map.addRoom("Science", (490, 217), chars.MatthewBeckler(), "Science Lab")
        map.addRoom("Dean's Office", (90, 589), chars.BillHudson(), "Science Lab")
        return map

    def serialize(self) -> dict:
        result = {"asset": DD.asset(self.image), "entry_point": None, "rooms": []}

        for room in self.rooms:
            NPC = room["NPC"].serialize()
            result["rooms"].append(
                {
                    "name": room["name"],
                    "coordinate": room["coordinate"],
                    "battlefield": room["battlefield"],
                    "NPC": NPC,
                }
            )

        return result

    @staticmethod
    def fromJson(json: dict, char: Character) -> "Map":
        ep = (json["entry_point"][0], json["entry_point"][1])
        map = Map(char, ep)
        map.setAsset(json["asset"])

        for room in json["rooms"]:
            NPC = CharacterFactory.createFromJson(room["NPC"])
            point = (room["coordinate"][0], room["coordinate"][1])
            map.addRoom(room["name"], point, NPC, room["battlefield"])

        return map


class MapScreen(QWidget):
    def __init__(self, map: Map):
        super().__init__()
        self.map = map
        self._callback = DD.unimplemented

        self.initUI()

    def onEnter(self, callback: Callable):
        """
        :param callback: A callback function that takes the room info as a parameter
        This callback will be triggered when the user selects which room to enter
        """
        self._callback = callback

    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key.Key_Enter or event.key() == Qt.Key.Key_Return:
            if self.map.current_room:
                self._callback(self.map.current_room)

    def initUI(self):
        layout = QGridLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        map_container_layout = QGridLayout()
        map_container_layout.addItem(
            QSpacerItem(
                50, 0, QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding
            ),
            0,
            0,
        )
        map_container = DD.scroller(map_container_layout, True, True)
        map_container.setStyleSheet("background-color: #57D7C1;")
        layout.addWidget(map_container, 0, 0)
        map_container_layout.addWidget(self.map, 1, 1)
        map_container_layout.addItem(
            QSpacerItem(
                50, 0, QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding
            ),
            2,
            2,
        )

        self.preview = FightPreview()
        self.map.onRoomChange(self.preview.setRoom)
        layout.addWidget(self.preview, 0, 1)
