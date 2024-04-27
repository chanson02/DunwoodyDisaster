from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QLabel, QHBoxLayout
from PySide6.QtGui import QPixmap, QKeyEvent, QPainter, QMouseEvent

from dunwoody_disaster.views.FightPreview import FightPreview
import dunwoody_disaster as DD
from dunwoody_disaster.CharacterFactory import Character, CharacterFactory
from typing import Optional, Callable
from math import sqrt


class MapScreen(QWidget):
    def __init__(self, character: Character, entryPoint: Optional[tuple[int, int]]):
        super().__init__()
        self.character = character
        self._callback = DD.unimplemented
        self.image = DD.ASSETS["no_texture"]
        self.rooms = []
        self.current_room: Optional[dict] = None

        if entryPoint:
            self.char_pos = entryPoint
        else:
            self.char_pos = (-1, 0)

        self.init_ui()

    def onEnter(self, callback: Callable):
        """
        :param callback: A callback function that takes the room info as a parameter
        This callback will be triggered when the user selects which room to enter
        """
        self._callback = callback

    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            if self.current_room:
                self._callback(self.current_room)

    def init_ui(self):
        # layout = QGridLayout()
        layout = QHBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        self.map = QLabel()
        self.map.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        self.move_character(-1, 0)
        layout.addWidget(self.map)

        self.preview = FightPreview()
        layout.addWidget(self.preview)

    def setAsset(self, asset: str):
        self.image = DD.ASSETS[asset]
        self.move_character(self.char_pos[0], self.char_pos[1])

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

    def findClosestRoom(self, x: int, y: int) -> Optional[dict]:
        closest = None
        min_dist = float("inf")

        for room in self.rooms:
            room_pos = room["coordinate"]
            distance = sqrt((x - room_pos[0]) ** 2 + (y - room_pos[1]) ** 2)
            if distance < min_dist:
                min_dist = distance
                closest = room

        return closest

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
        self.current_room = self.findClosestRoom(point.x(), point.y())
        if self.current_room:
            pos = self.current_room["coordinate"]
            self.move_character(pos[0], pos[1])
            self.preview.set_room(self.current_room)

    def pixmap(self):
        return QPixmap(self.image)

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
    def from_json(json: dict, char: Character) -> "MapScreen":
        ep = (json["entry_point"][0], json["entry_point"][1])
        map = MapScreen(char, ep)
        map.setAsset(json["asset"])

        for room in json["rooms"]:
            NPC = CharacterFactory.createFromJson(room["NPC"])
            point = (room["coordinate"][0], room["coordinate"][1])
            map.addRoom(room["name"], point, NPC, room["battlefield"])

        return map

    @staticmethod
    def build_map(char: Character) -> "MapScreen":
        test_enemy = CharacterFactory.createTestChar()
        test_enemy.name = "test enemy"
        test_enemy.image_path = DD.ASSETS["cooper"]
        ms = MapScreen(char, None)
        ms.setAsset("MainMap")
        ms.addRoom("Bus Stop", (419, 700), test_enemy, "no_texture")
        ms.addRoom("Court Yard", (693, 559), test_enemy, "no_texture")
        ms.addRoom("Commons", (451, 449), test_enemy, "no_texture")
        ms.addRoom("Math", (236, 359), test_enemy, "no_texture")
        ms.addRoom("English", (770, 366), test_enemy, "no_texture")
        ms.addRoom("Science", (490, 217), test_enemy, "no_texture")
        ms.addRoom("Dean's Office", (90, 589), test_enemy, "no_texture")
        return ms
