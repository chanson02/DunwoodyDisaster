import pygame

from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QGridLayout,
    QSpacerItem,
    QSizePolicy,
)
from PySide6.QtGui import QPixmap, QKeyEvent, QMouseEvent
from PySide6.QtCore import Qt, Signal

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
        self.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )  # Sets the alignment of the QLabel to center both horizontally and vertically
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
        rooms = self.coordinates()

        unbeaten = rooms["all"] - rooms["beaten"]
        if len(rooms["all"] - rooms["boss"] - rooms["beaten"]) != 0:
            unbeaten = unbeaten - rooms["boss"]

        for room in self.available_rooms():
            pos = room["coordinate"]
            distance = sqrt((x - pos[0]) ** 2 + (y - pos[1]) ** 2)
            if distance < min_dist:
                min_dist = distance
                closest = room

        return closest

    def moveCharacter(self, x: int, y: int):
        self.char_pos = (x, y)
        if x < 0:
            self.setPixmap(self.pixmap())
            return

        char_img = QPixmap(self.character.image()).scaledToWidth(80)
        self.setPixmap(DD.overlay(self.pixmap(), char_img, (x, y)))
        self.repaint()
        return

    def addRoom(
        self,
        name: Optional[str],
        pos: tuple[int, int],
        NPC: Character,
        battlefield: str,
        boss: bool = False,
    ):
        original = 1024
        target = 750
        factor = target / original
        pos = (int(pos[0] * factor), int(pos[1] * factor))
        room = {
            "name": name,
            "coordinate": pos,
            "battlefield": DD.ASSETS[battlefield],
            "NPC": NPC,
            "boss": boss,
        }
        self.rooms.append(room)

    def coordinates(self) -> dict:
        """
        Returns a dictionary of sets
        """
        return {
            "all": {r["coordinate"] for r in self.rooms},
            "boss": {r["coordinate"] for r in self.rooms if r.get("boss")},
            "beaten": {r["coordinate"] for r in self.rooms if r["NPC"].curHealth <= 0},
        }

    def available_rooms(self) -> list:
        rooms = self.coordinates()
        result = rooms["all"] - rooms["beaten"]
        if len(rooms["all"] - rooms["boss"] - rooms["beaten"]) != 0:
            result -= rooms["boss"]
        return [r for r in self.rooms if r["coordinate"] in result]

    def pixmap(self) -> QPixmap:
        rooms = self.coordinates()
        # Scale the map image
        result = QPixmap(self.image).scaledToWidth(1270)  # original size 1024x1024
        # If not all non-bosses have been beaten
        if len(rooms["all"] - rooms["boss"] - rooms["beaten"]) != 0:
            for room in rooms["boss"]:
                icon = QPixmap(DD.ASSETS["lock"]).scaledToWidth(100)
                result = DD.overlay(result, icon, room)

        return result

    def setAsset(self, asset: str):
        self.image = DD.ASSETS[asset]
        self.moveCharacter(self.char_pos[0], self.char_pos[1])
        self.backgroundImageChanged.emit(self.image)

    @staticmethod
    def buildMap(char: Character) -> "Map":
        chars = CharacterFactory
        map = Map(char)
        map.setAsset("NewMapFinal")
        map.addRoom("Bus Stop", (419, 700), chars.JoeAxberg(), "MathClassResized")
        map.addRoom("Court Yard", (693, 559), chars.LeAnnSimonson(), "LibraryResized")
        map.addRoom("Commons", (451, 449), chars.RyanRengo(), "ScienceClassResized")
        map.addRoom("Math", (236, 359), chars.NoureenSajid(), "CourtyardResized")
        map.addRoom(
            "English", (770, 366), chars.AmalanPulendran(), "ComputerLabResized"
        )
        map.addRoom("Science", (490, 217), chars.MatthewBeckler(), "MathClassResized")
        map.addRoom(
            "Dean's Office", (90, 589), chars.BillHudson(), "DeansOfficeResized"
        )
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
            pygame.mixer.music.stop()
            if self.map.current_room:
                self._callback(self.map.current_room)

    def initUI(self):
        layout = QGridLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        map_container_layout = QGridLayout()
        # Create a spacer that will expand in both directions; placed at the top-left corner of the grid (row 0, column 0)
        map_container_layout.addItem(
            QSpacerItem(50, 50, QSizePolicy.Expanding, QSizePolicy.Expanding), 0, 0
        )
        map_container = DD.scroller(map_container_layout, True, True)
        # set the backjground color of the map container
        map_container.setStyleSheet("background-color: #231D1D; min-width: 1000px;")

        layout.addWidget(map_container, 0, 0)
        # Adds the map QLabel to the grid layout; placed centrally at row 1, column 1
        map_container_layout.addWidget(self.map, 1, 1)
        # Create a spacer that will expand in both directions; placed at the bottom-right corner of the grid (row 2, column 2)
        map_container_layout.addItem(
            QSpacerItem(50, 50, QSizePolicy.Expanding, QSizePolicy.Expanding), 2, 2
        )
        self.preview = FightPreview()
        self.preview.setStyleSheet("background-color: black;")
        self.map.onRoomChange(self.preview.setRoom)
        layout.addWidget(self.preview, 0, 1)

        if len(self.map.rooms) > 0 and not self.map.current_room:
            self.map.setRoom(self.map.rooms[0])
