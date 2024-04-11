from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt

from dunwoody_disaster import ASSETS

# Stats for the items
# Add items as needed under its respective category
WeaponStats = {"sword": [20, 30, 10], "spear": [30, 10, 20]}

FoodStats = {}

ArmorStats = {"shield": [30, 10, 20], "gloves": [10, 10, 10]}


class Item:
    def __init__(self, name: str):
        self.name = name
        self.stats = {}

        if name in ASSETS:
            self.image = ASSETS[name]
        else:
            self.image = ASSETS["no_texture"]

    def __str__(self) -> str:
        return f"Item({self.name}, {self.stats})"

    def __repr__(self) -> str:
        return f"Item({self.name}, {self.stats})"

    def widget(self) -> QWidget:
        """
        Create a UI element to display the items properties
        """
        layout = QVBoxLayout()

        name = QLabel(self.name)
        name.setAlignment(Qt.AlignmentFlag.AlignCenter)
        name.setStyleSheet("color: white; font-size: 24px;")
        layout.addWidget(name)

        img = QLabel()
        img.setAlignment(Qt.AlignmentFlag.AlignCenter)
        img.setPixmap(QPixmap(self.image).scaledToWidth(80))
        layout.addWidget(img)

        stats = {'stat1': self.stats[0], 'stat2': self.stats[1], 'stat3': self.stats[2]}
        for stat, value in stats.items():
            lbl = QLabel(f"{stat}: {value}")
            lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(lbl)

        widget = QWidget()
        widget.setLayout(layout)
        return widget


class Weapon(Item):
    def __init__(self, name, damage, magicCost, staminaCost):
        super().__init__(name)
        self.stats = WeaponStats[name]
        self.damage = damage
        self.magicReq = magicCost
        self.staminaCost = staminaCost


class Food(Item):
    def __init__(self, name):
        super().__init__(name)
        self.stats = FoodStats[name]


class Armor(Item):
    def __init__(self, name: str, armorVal: int, *args):
        super().__init__(name)
        self.stats = ArmorStats[name]
        self.armorVal = armorVal


weapons = [Weapon("sword", 20, 30, 10), Weapon("spear", 30, 10, 20)]

armors = [Armor("shield", 30, 10, 20), Armor("gloves", 10, 10, 10)]