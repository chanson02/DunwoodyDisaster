from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt

import dunwoody_disaster as DD

# # Stats for the items
# # Add items as needed under its respective category
# WeaponStats = {"sword": [20, 30, 10], "spear": [30, 10, 20]}
#
# FoodStats = {}
#
# ArmorStats = {"shield": [30, 10, 20], "gloves": [10, 10, 10]}


class Item:
    def __init__(self, name: str, damage: int, stamina: int, magic: int):
        self.name = name
        self.damage = damage
        self.staminaCost = stamina
        self.magicCost = magic

        if name in DD.ASSETS:
            self.image = DD.ASSETS[name]
        else:
            self.image = DD.ASSETS["no_texture"]

    def __str__(self) -> str:
        return f"Item({self.name}, dmg={self.damage}, stamina={self.staminaCost}, magic={self.magicCost})"

    def __repr__(self) -> str:
        return f"Item({self.name}, dmg={self.damage}, stamina={self.staminaCost}, magic={self.magicCost})"

    def serialize(self) -> dict:
        return {
            "damage": self.damage,
            "magic": self.magicCost,
            "stamina": self.staminaCost,
        }

    def widget(self, min_width=100) -> QWidget:
        """
        Create a UI element to display the items properties
        :param min_width: the minimum amount of pixels to use when rendering
        """
        layout = QVBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)

        name = QLabel(self.name)
        name.setAlignment(Qt.AlignmentFlag.AlignCenter)
        name.setStyleSheet("color: white; font-size: 24px;")
        layout.addWidget(name)

        img = QLabel()
        img.setAlignment(Qt.AlignmentFlag.AlignCenter)
        img.setPixmap(QPixmap(self.image).scaledToWidth(80))
        layout.addWidget(img)

        for stat, value in self.serialize().items():
            lbl = QLabel(f"{stat}: {value}")
            lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(lbl)

        widget = QWidget()
        widget.setLayout(layout)
        widget.setContentsMargins(0, 0, 0, 0)
        widget.setMinimumWidth(min_width)
        return widget

    def to_dict(self) -> dict:
        DD.unimplemented()
        return {}


class Weapon(Item):
    def __init__(self, name: str, damage: int, stamina: int, magic: int):
        super().__init__(name, damage, stamina, magic)

    @staticmethod
    def from_json(json: dict) -> "Weapon":
        return Weapon(
            json["name"],
            # json["is_magical"],
            json["damage"],
            json["magicCost"],
            json["staminaCost"],
        )

    @staticmethod
    def default() -> "Weapon":
        weapon = Weapon("Fist", 1, 0, 0)
        return weapon

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            # "is_magical": self.magic,
            "damage": self.damage,
            "magicCost": self.magicCost,
            "staminaCost": self.staminaCost,
        }


# class Food(Item):
#     def __init__(self, name):
#         super().__init__(name)


class Armor(Item):
    def __init__(self, name: str, armorVal: int, staminaCost: int, magicCost: int):
        super().__init__(name, armorVal, staminaCost, magicCost)

    # @staticmethod
    # def from_json(json: dict) -> "Armor":
    #     return Armor(json["name"], json["armorVal"], json["magicDefense"])

    @staticmethod
    def default() -> "Armor":
        armor = Armor("Absorb", 1, 0, 0)
        return armor

    # def to_dict(self) -> dict:
    #     return {
    #         "name": self.name,
    #         "armorVal": self.armorVal,
    #         "magicDefense": self.magicDefense,
    #     }


weapons = [
        Weapon("sword", 30, 10, 0),
        Weapon("spear", 30, 10, 0)
        ]
armors = [
        Armor("shield", 30, 10, 0),
        Armor("gloves", 10, 5, 0)
        ]
