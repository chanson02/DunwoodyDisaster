from dunwoody_disaster.CharacterFactory import Character
# from dunwoody_disaster.views.meter import Meter
from dunwoody_disaster import ASSETS
from PySide6.QtWidgets import QWidget, QGridLayout, QLayout, QSpacerItem, QSizePolicy, QLabel
from PySide6.QtGui import QColor, QPixmap
from PySide6.QtCore import Qt


class CharacterState(QWidget):
    def __init__(self, character: Character):
        super().__init__()
        self.character = character

        layout = self.create_layout()
        self.setLayout(layout)

    def spacer(self, height: int) -> QSpacerItem:
        return QSpacerItem(
            0, height, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed
        )

    def create_layout(self) -> QLayout:
        layout = QGridLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        row = 0

        name = QLabel(self.character.name)
        name.setStyleSheet("color: white; font-size: 30px;")
        layout.addWidget(name, row, 0, 1, 3)
        row += 1

        layout.addItem(self.spacer(30), row, 1)
        row += 1

        health = QLabel(f"Health: {self.character.curHealth}")
        magic = QLabel(f"Magic: {self.character.curMagic}")
        mech = QLabel(f"Mechanical: {self.character.curMechanical}")

        layout.addWidget(health, row, 0)
        layout.addWidget(self.character.health_meter, row, 1, 1, 2)
        row += 1
        layout.addWidget(magic, row, 0)
        layout.addWidget(self.character.magic_meter, row, 1, 1, 2)
        row += 1
        layout.addWidget(mech, row, 0)
        layout.addWidget(self.character.mech_meter, row, 1, 1, 2)
        row += 1

        layout.addItem(self.spacer(10), row, 0)
        row += 1

        pic = QLabel("")
        pic.setAlignment(Qt.AlignmentFlag.AlignCenter)
        pic.setStyleSheet("min-width: 380px;")
        pic.setPixmap(QPixmap(ASSETS["ready"]))
        layout.addWidget(pic, row, 0, 1, 3)
        row += 1

        layout.addItem(self.spacer(30), row, 0)
        row += 1

        return layout
