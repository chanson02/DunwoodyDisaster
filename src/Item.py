# Assets for the items
images = {
    "sword": "assets/sword.png",
    "spear": "assets/spear.png",
}
# Stats for the items
# Add items as needed under its respective category
WeaponStats = {"sword": [20, 30, 10]}

FoodStats = {}

ArmorStats = {}


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
