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
        self.path = ASSETS['no_texture']

    def __str__(self) -> str:
        return f"Item{self.name}, {self.stats}"


class Weapon(Item):
    def __init__(self, name):
        super().__init__(name)
        self.stats = WeaponStats[name]


class Food(Item):
    def __init__(self, name):
        super().__init__(name)
        self.stats = FoodStats[name]


class Armor(Item):
    def __init__(self, name):
        super().__init__(name)
        self.stats = ArmorStats[name]
