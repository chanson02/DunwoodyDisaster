from dunwoody_disaster.CharacterFactory import Character
import dunwoody_disaster as DD
from PySide6.QtWidgets import (
    QWidget,
    QGridLayout,
    QLayout,
    QLabel,
    QSpacerItem,
    QSizePolicy
)
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
        name.setAlignment(Qt.AlignmentFlag.AlignCenter)
        name.setStyleSheet("color: white; font-size: 30px;")
        layout.addWidget(name, row, 0, 1, 3)
        row += 1

        layout.addItem(QSpacerItem(0, 50, 
                        QSizePolicy.Fixed, 
                        QSizePolicy.Fixed), row, 0)
        row += 1  

        layout.addWidget(self.character.health_lbl, row, 0)
        layout.addWidget(self.character.health_meter, row, 1, 1, 2)
        row += 1

        layout.addItem(QSpacerItem(0, 5, 
                        QSizePolicy.Fixed, 
                        QSizePolicy.Fixed), row, 0)
        row += 1  

        layout.addWidget(self.character.magic_lbl, row, 0)
        layout.addWidget(self.character.magic_meter, row, 1, 1, 2)
        row += 1

        layout.addItem(QSpacerItem(0, 5, 
                        QSizePolicy.Fixed, 
                        QSizePolicy.Fixed), row, 0)
        row += 1  

        layout.addWidget(self.character.stamina_lbl, row, 0)
        layout.addWidget(self.character.stamina_meter, row, 1, 1, 2)
        row += 1

        layout.addItem(QSpacerItem(0, 50, 
                        QSizePolicy.Fixed, 
                        QSizePolicy.Fixed), row, 0)

        return layout
