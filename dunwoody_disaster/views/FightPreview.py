from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QGroupBox,
    QHBoxLayout,
)
from PySide6.QtGui import QPixmap, QPainter
import dunwoody_disaster as DD
from PySide6.QtCore import Qt
from typing import Optional


class FightPreview(QWidget):
    def __init__(self):
        super().__init__()

        self.room_lbl = QLabel()
        self.weapons = QHBoxLayout()
        self.defenses = QHBoxLayout()
        self.health = QLabel()
        self.magic = QLabel()
        self.stamina = QLabel()

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        self.setLayout(layout)

        self.weapons.setContentsMargins(0, 0, 0, 0)
        self.defenses.setContentsMargins(0, 0, 0, 0)

        self.room_lbl = QLabel()
        self.room_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.room_lbl.setStyleSheet("font-size: 24px;")
        layout.addWidget(self.room_lbl)

        self.battlefield = QLabel()
        self.battlefield.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.battlefield)

        layout.addLayout(self.statLayout())

        gb = QGroupBox("Weapons")
        container = QHBoxLayout()
        gb.setLayout(container)
        scroller = DD.scroller(self.weapons, True, False)
        container.addWidget(scroller)
        layout.addWidget(gb)

        gb = QGroupBox("Defenses")
        container = QHBoxLayout()
        gb.setLayout(container)
        scroller = DD.scroller(self.defenses, True, False)
        container.addWidget(scroller)
        layout.addWidget(gb)

    def statLayout(self) -> QHBoxLayout:
        layout = QHBoxLayout()
        # Yes this is how much I hate grid layout --Cooper
        layout.addItem(DD.expander(True, False))
        layout.addItem(DD.expander(True, False))
        layout.addItem(DD.expander(True, False))
        layout.addWidget(self.health)
        layout.addItem(DD.expander(True, False))
        layout.addWidget(self.magic)
        layout.addItem(DD.expander(True, False))
        layout.addWidget(self.stamina)
        layout.addItem(DD.expander(True, False))
        layout.addItem(DD.expander(True, False))
        layout.addItem(DD.expander(True, False))
        return layout

    def clear(self):
        self.room_lbl.setText("")
        self.health.setText("")
        self.magic.setText("")
        self.stamina.setText("")
        self.battlefield.setPixmap(QPixmap())
        return

    def setRoom(self, room_info: Optional[dict]):
        DD.clear_layout(self.weapons)
        DD.clear_layout(self.defenses)
        if room_info is None:
            self.clear()
            return

        NPC = room_info["NPC"]
        lbl = f"{room_info['name']}: {NPC.name}"
        self.room_lbl.setText(lbl)

        bkg = QPixmap(room_info["battlefield"]).scaledToWidth(400)
        self.battlefield.setPixmap(
            self.centerOverlay(bkg, NPC.image().scaledToWidth(50))
        )

        self.health.setText(f"Health: {NPC.maxHealth}")
        self.magic.setText(f"Magic: {NPC.maxMagic}")
        self.stamina.setText(f"Stamina: {NPC.maxStamina}")

        DD.clear_layout(self.weapons)
        for weapon in NPC.weapons:
            self.weapons.addWidget(weapon.widget())

        DD.clear_layout(self.defenses)
        for defense in NPC.defenses:
            self.defenses.addWidget(defense.widget())

    def centerOverlay(self, background: QPixmap, foreground: QPixmap) -> QPixmap:
        x = (background.width() - foreground.width()) // 2
        y = (background.height() - foreground.height()) // 2
        painter = QPainter(background)
        painter.drawPixmap(x, y, foreground)
        painter.end()
        return background
