from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QGroupBox,
    QHBoxLayout,
    QGridLayout,
    QSpacerItem,
    QSizePolicy,
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
        statsStyle = 'font-size: 14px; font-family: "Futura Bk BT";'
        self.health = QLabel()
        self.health.setStyleSheet(statsStyle)
        self.magic = QLabel()
        self.magic.setStyleSheet(statsStyle)
        self.stamina = QLabel()
        self.stamina.setStyleSheet(statsStyle)

        self.initUI()

    def initUI(self):
        layout = QGridLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        self.setLayout(layout)

        self.weapons.setContentsMargins(0, 0, 0, 0)
        self.defenses.setContentsMargins(0, 0, 0, 0)

        row = 0

        layout.addItem(
            QSpacerItem(20, 30, QSizePolicy.Fixed, QSizePolicy.Fixed), row, 0
        )
        row += 1

        self.room_lbl = QLabel()
        self.room_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.room_lbl.setStyleSheet("font-size: 30px;")
        layout.addWidget(self.room_lbl, row, 1)
        row += 1

        layout.addItem(
            QSpacerItem(0, 15, QSizePolicy.Fixed, QSizePolicy.MinimumExpanding), row, 1
        )
        row += 1

        self.battlefield = QLabel()
        self.battlefield.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.battlefield, row, 1)
        row += 1

        layout.addItem(
            QSpacerItem(0, 15, QSizePolicy.Fixed, QSizePolicy.MinimumExpanding), row, 1
        )
        row += 1

        layout.addLayout(self.statLayout(), row, 1)
        row += 1

        layout.addItem(
            QSpacerItem(0, 15, QSizePolicy.Fixed, QSizePolicy.MinimumExpanding), row, 1
        )
        row += 1

        gb = QGroupBox("Offense")
        gb.setStyleSheet(
            "max-width: 400px; max-height: 200px; height: 200px; font-size: 14px;"
        )
        container = QHBoxLayout()
        gb.setLayout(container)
        scroller = DD.scroller(self.weapons, True, False)
        scroller.setStyleSheet("border: none;")
        container.addWidget(scroller)
        layout.addWidget(gb, row, 1)
        row += 1

        layout.addItem(
            QSpacerItem(0, 15, QSizePolicy.Fixed, QSizePolicy.MinimumExpanding), row, 1
        )
        row += 1

        gb = QGroupBox("Defense")
        gb.setStyleSheet(
            "max-width: 400px; max-height: 200px; height: 200px; font-size: 14px;"
        )
        container = QHBoxLayout()
        gb.setLayout(container)
        scroller = DD.scroller(self.defenses, True, False)
        scroller.setStyleSheet("border: none;")
        container.addWidget(scroller)
        layout.addWidget(gb, row, 1)
        row += 1

        layout.addItem(
            QSpacerItem(20, 15, QSizePolicy.Fixed, QSizePolicy.MinimumExpanding), row, 2
        )

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
            self.centerOverlay(bkg, NPC.image().scaledToWidth(150))
        )
        if 'Engineering' in lbl:
            self.battlefield.setMaximumHeight(150)
        else:
            self.battlefield.setMaximumHeight(300)

        self.health.setText(f"Health: {NPC.maxHealth}")
        self.magic.setText(f"Magic: {NPC.maxMagic}")
        self.stamina.setText(f"Stamina: {NPC.maxStamina}")

        DD.clear_layout(self.weapons)
        for weapon in NPC.weapons:
            self.weapons.addWidget(weapon.preview_widget())

        DD.clear_layout(self.defenses)
        for defense in NPC.defenses:
            self.defenses.addWidget(defense.preview_widget())

    def centerOverlay(self, background: QPixmap, foreground: QPixmap) -> QPixmap:
        x = (background.width() - foreground.width()) // 2
        y = (background.height() - foreground.height()) // 2
        painter = QPainter(background)
        painter.drawPixmap(x, y, foreground)
        painter.end()
        return background
