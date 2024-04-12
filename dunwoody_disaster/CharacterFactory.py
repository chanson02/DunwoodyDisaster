from dunwoody_disaster.views.meter import Meter
from PySide6.QtGui import QColor
from PySide6.QtWidgets import QLabel


class Character:
    def __init__(self):
        # Meta data
        self.level = 0
        self.name = ""
        self.classType = ""
        self.strength = 0
        self.intelligence = 0

        #Meteres
        self.curHealth = 0
        self.maxHealth = 0
        self.curMagic = 0
        self.maxMagic = 0
        self.curStamina = 0
        self.maxStamina = 0

        self.health_lbl = QLabel(f"Health: {self.curHealth}")
        self.health_lbl.setStyleSheet("color: white; font-size: 24px;")
        self.magic_lbl = QLabel(f"Magic: {self.curMagic}")
        self.magic_lbl.setStyleSheet("color: white; font-size: 24px;")
        self.stamina_lbl = QLabel(f"Stamina: {self.curStamina}")
        self.stamina_lbl.setStyleSheet("color: white; font-size: 24px;")
        self.health_meter = Meter(QColor(255, 0, 0), 100)
        self.magic_meter = Meter(QColor(200, 0, 200), 100)
        self.stamina_meter = Meter(QColor(50, 50, 50), 100)

        # What are these? --Cooper
        self.defense = 0
        self.magicDefense = 0

        # Inventory
        self.loot = []
        self.food = []
        self.weapons = {}
        self.defenses = {}

    def set_health(self, health: int):
        self.curHealth = health
        if self.maxHealth == 0:
            percentage = 0
        else:
            percentage = (health // self.maxHealth) * 100
        print(f"Health: {self.curHealth}")
        self.health_lbl.setText(f"Health: {self.curMagic}")
        self.health_meter.setPercentage(percentage)

    def set_magic(self, magic: int):
        self.curMagic = magic
        if self.maxMagic == 0:
            percentage = 0
        else:
            percentage = (magic // self.maxMagic) * 100
        self.magic_lbl.setText(f"Magic: {self.curMagic}")
        self.magic_meter.setPercentage(percentage)

    def set_stamina(self, stamina: int):
        self.curStamina = stamina
        if self.maxStamina == 0:
            percentage = 0
        else:
            percentage = (stamina // self.maxStamina) * 100
        self.stamina_lbl.setText(f"Stamina: {self.curStamina}")
        self.stamina_meter.setPercentage(percentage)

    def PlotRisk(self, attacks: list) -> None:
        """
        Goes through enemeis potential attacks and damage according to our defense profile
        Prints how risk each attack could be
        :param attacks: List containing attack data [name, stamina cost, magic damage, health damage]
        """
        risk_levels = {
            "high": "is a high risk attack",
            "medium": "is a medium risk attack",
            "low": "is a low risk attack",
            "none": "is a no risk attack",
        }

        for attack in attacks:
            name, mech, magic, health = attack
            print(f"{name} ", end="")
            if self.curStamina <= mech:
                # attack stuns opponent ?
                print(risk_levels["high"])
                continue

            total_damage = max(0, magic - self.magicDefense) + max(
                0, health - self.defense
            )
            if total_damage >= self.curHealth:
                print(risk_levels["high"])
            elif total_damage > self.curHealth / 2:
                print(risk_levels["medium"])
            elif total_damage > self.curHealth / 4:
                print(risk_levels["low"])
            else:
                print(risk_levels["none"])


class CharacterFactory:
    """
    A class for creating characters
    """

    class_types = {
        "blank": {
            "health": 100,
            "magic": 100,
            "stamina": 100,
            "strength": 10,
            "intelligence": 10,
            "defense": 0,
            "magicDefense": 0,
            "level": 1,
            "loot": [],
            "food": [],
        },
        "warrior": {
            "health": 100,
            "magic": 0,
            "stamina": 15,
            "strength": 15,
            "intelligence": 5,
            "defense": 0,
            "magicDefense": 0,
            "level": 1,
            "loot": [],
            "food": [],
        },
        "mage": {
            "health": 100,
            "magic": 15,
            "stamina": 0,
            "strength": 5,
            "intelligence": 15,
            "defense": 0,
            "magicDefense": 0,
            "level": 1,
            "loot": [],
            "food": [],
        },
        "thief": {
            "health": 100,
            "magic": 0,
            "stamina": 10,
            "strength": 8,
            "intelligence": 8,
            "defense": 0,
            "magicDefense": 0,
            "level": 1,
            "loot": [],
            "food": [],
        },
    }

    @staticmethod
    def createCharacter(name: str, classType: str) -> Character:
        """
        Creates a character based on the given class type
        :param name: The name of the character
        :param classType: The type of the character
        :return: The created character object
        :raises:
            ValueError: If the provided classType is not a member of CharacterFactory.class_types
        """
        if classType not in CharacterFactory.class_types:
            raise ValueError("Invalid class type")

        data = CharacterFactory.class_types[classType]
        character = Character()

        character.name = name
        character.classType = classType
        character.maxHealth = data["health"]
        character.maxMagic = data["magic"]
        character.maxStamina = data["stamina"]

        character.strength = data["strength"]
        character.intelligence = data["intelligence"]

        character.defense = data["defense"]
        character.magicDefense = data["magicDefense"]

        character.level = data["level"]
        character.loot = data["loot"]
        character.food = data["food"]

        character.set_health(data["health"])
        character.set_magic(data["magic"])
        character.set_stamina(data["stamina"])

        return character

    @staticmethod
    def createTestChar() -> Character:
        """
        Creates a default character we can use for testing
        """
        character = CharacterFactory.createCharacter("Test-Char", "blank")
        character.weapons = {"sword": [20, 30, 10], "spear": [30, 10, 20]}
        character.defenses = {"shield": [30, 10, 20], "gloves": [10, 10, 10]}
        return character
