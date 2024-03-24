import copy

risk_levels = {
    "high": "is a high risk attack",
    "medium": "is a medium risk attack",
    "low": "is a low risk attack",
    "none": "is a no risk attack",
}


class CharacterFactory:
    class_types = {
                "blank": ["blank", 100, 0, 0, 0, 0, 0, 1, [], []],
                "warrior": ["warrior", 100, 0, 15, 0, 0, 1, [], []],
                "mage": ["mage", 100, 15, 0, 0, 0, 1, [], []],
                "thief": ["thief", 100, 0, 10, 0, 0, 1, [], []],
            }

    @staticmethod
    def createCharacter(name, classType):
        if classType not in CharacterFactory.class_types:
            raise ValueError('Invalid class type')

        data = CharacterFactory.class_types[classType]
        character = Character()

        character.name = name
        character.classType = classType
        character.health = data[1]
        character.magic = data[2]
        character.mechanical = data[4]
        character.defense = data[5]
        character.magicDefense = data[6]
        character.level = data[7]
        character.loot = data[8]
        character.food = data[9]

        return character


class Character:

    def __init__(self):
        # Meta data
        self.level = 0
        self.name = None
        self.classType = None

        # Meters
        self.health = 0
        self.magic = 0
        self.mechanical = 0
        self.defense = 0
        self.magicDefense = 0

        # Inventory
        self.loot = []
        self.food = []

    def PlotRisk(
        self, attacks
    ):  # goes through enemies potential attacks and damage according to our defense profile
        attacksCopy = copy.deepcopy(attacks)

        global health
        for attack in attacksCopy:
            attackName = attack.pop(0)

            mechDamage = attack.pop(0)
            magicDamage = attack.pop(0)
            healthDamage = attack.pop(0)

            if self.mechanical <= mechDamage:
                att = f"{attackName} {risk_levels['high']}"
                print(att)  # will "stun" the character
                continue
            totalDamage = 0
            totalDamage += (
                magicDamage - self.magicDefense
                if self.magicDefense < magicDamage
                else 0
            )
            totalDamage += (
                healthDamage - self.defense if self.defense < healthDamage else 0
            )

            if self.health - totalDamage <= 0:
                print(f"{attackName} {risk_levels['high']}")
                continue  # will kill the character
            elif totalDamage > self.health / 2:
                print(f"{attackName} {risk_levels['medium']}")
                continue  # a lot of damage to the character
            elif totalDamage > self.health / 4:
                print(f"{attackName} {risk_levels['low']}")
                continue  # a little damage the character
            else:
                print(f"{attackName} {risk_levels['none']}")
                continue
