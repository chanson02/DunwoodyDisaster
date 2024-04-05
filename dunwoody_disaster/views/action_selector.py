from PySide6.QtWidgets import QWidget, QLayout, QGridLayout, QLabel
from PySide6.QtGui import QPixmap
from typing import Optional
import dunwoody_disaster as DD


class ActionSelector(QWidget):
    def __init__(self):
        super().__init__()
        self.attack: Optional[dict] = None
        self.defense: Optional[dict] = None
        self.setLayout(self.create_layout())

    def set_attack(self, item: dict):
        self.attack = item
        self.update_ui()

    def set_defense(self, item: dict):
        self.defense = item
        self.update_ui()

    def update_ui(self):
        if self.attack:
            self.attack_pic.setPixmap(
                QPixmap(DD.ASSETS[self.attack["name"]]).scaledToWidth(50)
            )
        if self.defense:
            self.defend_pic.setPixmap(
                QPixmap(DD.ASSETS[self.defense["name"]]).scaledToWidth(50)
            )

    def create_layout(self) -> QLayout:
        layout = QGridLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)

        self.attack_pic = QLabel("")
        self.defend_pic = QLabel("")

        layout.addWidget(self.attack_pic, 0, 0)
        layout.addWidget(self.defend_pic, 0, 1)
        return layout
