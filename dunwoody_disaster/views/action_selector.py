from PySide6.QtWidgets import QWidget, QLayout, QGridLayout, QLabel
from PySide6.QtGui import QPixmap
from typing import Optional
from dunwoody_disaster import Item


class ActionSelector(QWidget):
    def __init__(self):
        super().__init__()
        self.attack: Optional[Item.Weapon] = None
        self.defense: Optional[Item.Armor] = None
        self.setLayout(self.create_layout())

    def set_attack(self, item: Optional[Item.Weapon]):
        self.attack = item
        self.update_ui()

    def set_defense(self, item: Optional[Item.Armor]):
        self.defense = item
        self.update_ui()

    def update_ui(self):
        if self.attack:
            print(self)
            self.attack_pic.setPixmap(QPixmap(self.attack.image).scaledToWidth(50))
        if self.defense:
            self.defend_pic.setPixmap(QPixmap(self.defense.image).scaledToWidth(50))

    def create_layout(self) -> QLayout:
        layout = QGridLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)

        self.attack_pic = QLabel("")
        self.defend_pic = QLabel("")

        layout.addWidget(self.attack_pic, 0, 0)
        layout.addWidget(self.defend_pic, 0, 1)
        return layout
