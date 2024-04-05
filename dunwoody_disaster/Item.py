# Assets for the items

from dunwoody_disaster import ASSETS

images = {
    "sword": ASSETS["sword"],
    "spear": ASSETS["spear"],
    "shield": ASSETS["shield"],
    "gloves": ASSETS["gloves"],
}
# Stats for the items
# Add items as needed under its respective category
WeaponStats = {"sword": [20, 30, 10], "spear": [30, 10, 20]}

FoodStats = {}

ArmorStats = {"shield": [30, 10, 20], "gloves": [10, 10, 10]}


class Item:
    def __init__(self, name):
        self.name = name
        self.image = images[self.name]
        self.stats = None

    def __str__(self) -> str:
        return str(self.name, self.stats)


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
    def __init__(self, name, armorVal):
        super().__init__(name)
        self.stats = ArmorStats[name]
        self.armorVal = armorVal
