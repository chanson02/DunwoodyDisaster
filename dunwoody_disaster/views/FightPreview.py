from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QGroupBox,
    QScrollArea,
    QHBoxLayout,
)
from PySide6.QtGui import QPixmap, QPainter
from dunwoody_disaster.CharacterFactory import Character
from PySide6.QtCore import Qt


class FightPreview(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.setLayout(layout)

        self.room_lbl = QLabel()
        self.room_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.room_lbl.setStyleSheet("font-size: 24px;")
        layout.addWidget(self.room_lbl)

        self.battlefield = QLabel()
        self.battlefield.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.battlefield)

        self.stats = QLabel()
        layout.addWidget(self.stats)

        layout.addWidget(QLabel("Inventory"))

        self.weapons = QHBoxLayout()
        scroll_area = QScrollArea()
        scroll_area.setLayout(self.weapons)
        container = QHBoxLayout()
        container.addWidget(scroll_area)
        gb = QGroupBox("Weapons")
        gb.setLayout(container)
        layout.addWidget(gb)
        gb.setMinimumHeight(250)
        container.setContentsMargins(0, 0, 0, 0)

        self.defenses = QHBoxLayout()
        gb = QGroupBox("Defenses")
        gb.setMinimumHeight(250)
        container = QHBoxLayout()
        container.setContentsMargins(0, 0, 0, 0)
        scroll_area = QScrollArea()
        layout.addWidget(gb)
        gb.setLayout(container)
        container.addWidget(scroll_area)
        scroll_area.setLayout(self.defenses)

    def set_room(self, room_info: dict):
        NPC = room_info["NPC"]
        lbl = f"{room_info['name']}: {NPC.name}"
        self.room_lbl.setText(lbl)

        bkg = QPixmap(room_info["battlefield"]).scaledToWidth(400)
        self.battlefield.setPixmap(
            self.center_overlay(bkg, NPC.image().scaledToWidth(50))
        )

        self.stats.setText(self.stat_text(NPC))

        for i in reversed(range(self.weapons.count())):
            widget = self.weapons.itemAt(i).widget()
            self.weapons.removeWidget(widget)
            widget.setParent(None)

        for weapon in NPC.weapons:
            self.weapons.addWidget(weapon.widget())

        for i in reversed(range(self.defenses.count())):
            widget = self.defenses.itemAt(i).widget()
            self.defenses.removeWidget(widget)
            widget.setParent(None)

        for defense in NPC.defenses:
            self.defenses.addWidget(defense.widget())

    def center_overlay(self, background: QPixmap, foreground: QPixmap) -> QPixmap:
        x = (background.width() - foreground.width()) // 2
        y = (background.height() - foreground.height()) // 2
        painter = QPainter(background)
        painter.drawPixmap(x, y, foreground)
        painter.end()
        return background

    def stat_text(self, char: Character) -> str:
        result = ""
        result += f"Health: {char.maxHealth}\n"
        result += f"Magic: {char.maxMagic}\n"
        result += f"Stamina: {char.maxStamina}\n"
        return result
