from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt

import dunwoody_disaster as DD


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

    def preview_widget(self) -> QWidget:
        """
        Create a UI element to display the items properties
        :param min_width: the minimum amount of pixels to use when rendering
        """
        layout = QVBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)

        name = QLabel(self.name.replace(" ", "\n"))
        name.setAlignment(Qt.AlignmentFlag.AlignCenter)
        name.setFixedHeight(40)
        name.setWordWrap(True)
        name.setStyleSheet(
            'color: white; font-size: 16px; font-family: "Futura Bk BT";'
        )
        layout.addWidget(name)

        img = QLabel()
        img.setAlignment(Qt.AlignmentFlag.AlignCenter)
        img.setPixmap(QPixmap(self.image).scaledToWidth(50))
        layout.addWidget(img)

        for stat, value in self.serialize().items():
            lbl = QLabel(f"{stat}: {value}")
            lbl.setStyleSheet('font-family: "Futura Bk BT";')
            lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(lbl)

        widget = QWidget()
        widget.setLayout(layout)
        widget.setContentsMargins(0, 0, 0, 0)
        return widget

    def widget(self, min_width=100) -> QWidget:
        """
        Create a UI element to display the items properties
        :param min_width: the minimum amount of pixels to use when rendering
        """
        layout = QVBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)

        name = QLabel(self.name.replace(" ", "\n"))
        name.setAlignment(Qt.AlignmentFlag.AlignCenter)
        name.setStyleSheet(
            'color: white; font-size: 20px; font-family: "Futura Bk BT";'
        )
        layout.addWidget(name)

        img = QLabel()
        img.setAlignment(Qt.AlignmentFlag.AlignCenter)
        img.setPixmap(QPixmap(self.image).scaledToWidth(80))
        layout.addWidget(img)

        for stat, value in self.serialize().items():
            lbl = QLabel(f"{stat}: {value}")
            lbl.setStyleSheet('font-family: "Futura Bk BT";')
            lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(lbl)

        widget = QWidget()
        widget.setLayout(layout)
        widget.setContentsMargins(0, 0, 0, 0)
        widget.setMinimumWidth(min_width)
        return widget

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "damage": self.damage,
            "magic": self.magicCost,
            "stamina": self.staminaCost,
        }


class Weapon(Item):
    def __init__(self, name: str, magical: bool, damage: int, stamina: int, magic: int):
        """
        :param magical: If true attack with intelligence, otherwise strength
        """
        super().__init__(name, damage, stamina, magic)
        self.magical = magical

    def to_dict(self) -> dict:
        result = super().to_dict()
        result["magical"] = self.magical
        return result

    @staticmethod
    def from_json(json: dict) -> "Weapon":
        return Weapon(
            json["name"],
            json["magical"],
            json["damage"],
            json["stamina"],
            json["magic"],
        )

    @staticmethod
    def default() -> "Weapon":
        weapon = Weapon("Fist", False, 1, 0, 0)
        return weapon


# class Food(Item):
#     def __init__(self, name):
#         super().__init__(name)


class Armor(Item):
    def __init__(
        self,
        name: str,
        armorVal: int,
        staminaCost: int,
        magicCost: int,
        magicDefense: int,
    ):
        """
        :param armorVal: Amount of damage to block if attack is not magical
        :param magicDefense: Amount of damage to block if attack is magical
        """
        super().__init__(name, armorVal, staminaCost, magicCost)
        self.magicDefense = magicDefense

    def to_dict(self) -> dict:
        result = super().to_dict()
        result["magicDefense"] = self.magicDefense
        return result

    @staticmethod
    def default() -> "Armor":
        armor = Armor("Absorb", 1, 0, 0, 0)
        return armor

    @staticmethod
    def from_json(json: dict) -> "Armor":
        return Armor(
            json["name"],
            json["damage"],
            json["stamina"],
            json["magic"],
            json["magicDefense"],
        )


weapons = [Weapon("sword", False, 30, 10, 0), Weapon("spear", False, 30, 10, 0)]
armors = [Armor("shield", 30, 10, 0, 0), Armor("gloves", 10, 5, 0, 0)]
