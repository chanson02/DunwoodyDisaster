# Assets for the items

from dunwoody_disaster import ASSETS

# Stats for the items
# Add items as needed under its respective category
WeaponStats = {"sword": [20, 30, 10], "spear": [30, 10, 20]}

FoodStats = {}

ArmorStats = {"shield": [30, 10, 20], "gloves": [10, 10, 10]}


class Item:
    def __init__(self, name):
        self.name = name
        self.stats = None

        if name in ASSETS:
            self.image = ASSETS[name]
        else:
            self.image = ASSETS["no_texture"]

    def __str__(self) -> str:
        return f"Item({self.name}, {self.stats})"

    def __repr__(self) -> str:
        return f"Item({self.name}, {self.stats})"


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


weapons = [Weapon("sword", 20, 0, 10), Weapon("spear", 30, 0, 20)]

armors = [Armor("shield", 30, 10, 20), Armor("gloves", 10, 10, 10)]
