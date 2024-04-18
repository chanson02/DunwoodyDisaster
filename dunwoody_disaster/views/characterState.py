from dunwoody_disaster.CharacterFactory import Character
import dunwoody_disaster as DD
from PySide6.QtWidgets import (
    QWidget,
    QGridLayout,
    QLayout,
    QLabel,
)
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt


class CharacterState(QWidget):
    def __init__(self, character: Character):
        super().__init__()
        self.character = character

        self.setLayout(self.create_layout())
        return

    def create_layout(self) -> QLayout:
        layout = QGridLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        row = 0

        name = QLabel(self.character.name)
        name.setStyleSheet("color: white; font-size: 30px;")
        layout.addWidget(name, row, 0, 1, 3)
        row += 1

        layout.addItem(DD.spacer(30), row, 1)
        row += 1

        layout.addWidget(self.character.health_lbl, row, 0)
        layout.addWidget(self.character.health_meter, row, 1, 1, 2)
        row += 1
        layout.addWidget(self.character.magic_lbl, row, 0)
        layout.addWidget(self.character.magic_meter, row, 1, 1, 2)
        row += 1
        layout.addWidget(self.character.stamina_lbl, row, 0)
        layout.addWidget(self.character.stamina_meter, row, 1, 1, 2)
        row += 1

        layout.addItem(DD.spacer(10), row, 0)
        row += 1

        pic = QLabel("")
        pic.setAlignment(Qt.AlignmentFlag.AlignCenter)
        pic.setStyleSheet("min-width: 380px;")
        pic.setPixmap(self.character.image())
        layout.addWidget(pic, row, 0, 1, 3)
        row += 1

        layout.addItem(DD.spacer(30), row, 0)
        row += 1

        return layout
