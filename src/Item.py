# Assets for the items
images = {
    "sword": "assets/sword.png",
    "spear": "assets/spear.png",
    "shield": "assets/shield.png",
    "gloves": "assets/gloves.png",
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
        return self.name, self.stats


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
