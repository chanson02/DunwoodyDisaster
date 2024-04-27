from PySide6.QtWidgets import QWidget, QLayout, QLabel, QHBoxLayout
from PySide6.QtGui import QPixmap
from typing import Optional
from dunwoody_disaster import Item
import dunwoody_disaster as DD


class ActionSelector(QWidget):
    def __init__(self):
        super().__init__()
        self.attack: Optional[Item.Weapon] = None
        self.defense: Optional[Item.Armor] = None
        self.setLayout(self.createLayout())

    def setAttack(self, item: Optional[Item.Weapon]):
        self.attack = item
        self.updateUI()

    def setDefense(self, item: Optional[Item.Armor]):
        self.defense = item
        self.updateUI()

    def updateUI(self):
        if self.attack:
            print(self)
            self.attack_pic.setPixmap(QPixmap(self.attack.image).scaledToWidth(50))
        if self.defense:
            self.defend_pic.setPixmap(QPixmap(self.defense.image).scaledToWidth(50))

    def ready(self) -> bool:
        return (self.attack and self.defense) is not None

    def createLayout(self) -> QLayout:
        layout = QHBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)

        self.attack_pic = QLabel("")
        self.defend_pic = QLabel("")

        layout.addItem(DD.expander(True, False, 0))
        layout.addWidget(self.attack_pic)
        layout.addWidget(self.defend_pic)
        layout.addItem(DD.expander(True, False, 0))
        return layout
