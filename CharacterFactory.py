class Character:
    def __init__(self):
        # Meta data
        self.level = 0
        self.name = ""
        self.classType = ""

        # Meters
        self.curHealth = 0
        self.maxHealth = 0
        self.curMagic = 0
        self.maxMagic = 0
        self.curMechanical = 0
        self.maxMechanical = 0

        # Inventory
        self.loot = []
        self.food = []
        self.weapons = {}
        self.defenses = {}

    def PlotRisk(self, attacks: list) -> None:
        """
        Goes through enemeis potential attacks and damage according to our defense profile
        Prints how risk each attack could be
        :param attacks: List containing attack data [name, mechanical damage, magic damage, health damage]
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
            if self.maxMechanical <= mech:
                # attack stuns opponent ?
                print(risk_levels["high"])
                continue

            total_damage = max(0, magic - self.magicDefense) + max(
                0, health - self.defense
            )
            if total_damage >= self.maxHealth:
                print(risk_levels["high"])
            elif total_damage > self.maxHealth / 2:
                print(risk_levels["medium"])
            elif total_damage > self.maxHealth / 4:
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
            "magic": 1,
            "mechanical": 1,
            "defense": 0,
            "magicDefense": 0,
            "level": 1,
            "loot": [],
            "food": [],
        },
        "warrior": {
            "health": 100,
            "magic": 0,
            "mechanical": 15,
            "defense": 0,
            "magicDefense": 0,
            "level": 1,
            "loot": [],
            "food": [],
        },
        "mage": {
            "health": 100,
            "magic": 15,
            "mechanical": 0,
            "defense": 0,
            "magicDefense": 0,
            "level": 1,
            "loot": [],
            "food": [],
        },
        "thief": {
            "health": 100,
            "magic": 0,
            "mechanical": 10,
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
        character.maxMechanical = data["mechanical"]
        character.defense = data["defense"]
        character.magicDefense = data["magicDefense"]
        character.level = data["level"]
        character.loot = data["loot"]
        character.food = data["food"]

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
