from dunwoody_disaster.views.meter import Meter

import dunwoody_disaster as DD
from PySide6.QtGui import QColor, QPixmap
from PySide6.QtWidgets import QLabel
from dunwoody_disaster import Item
import json
import os


class Character:
    def __init__(self):
        # Meta data
        self.level = 0
        self.name = ""
        self.classType = ""
        self.strength = 0
        self.intelligence = 0
        self.image_path = DD.ASSETS["no_texture"]

        # Meteres
        self.curHealth = 0
        self.maxHealth = 0
        self.curMagic = 0
        self.maxMagic = 0
        self.curStamina = 0
        self.maxStamina = 0

        self.inventory_capacity = 100

        self.health_lbl = QLabel(f"Health: {self.curHealth}")
        self.health_lbl.setStyleSheet("color: white; font-size: 14px;")
        self.magic_lbl = QLabel(f"Magic: {self.curMagic}")
        self.magic_lbl.setStyleSheet("color: white; font-size: 14px;")
        self.stamina_lbl = QLabel(f"Stamina: {self.curStamina}")
        self.stamina_lbl.setStyleSheet("color: white; font-size: 14px;")
        self.health_meter = Meter(QColor(255, 0, 0), 100)
        self.health_meter.setStyleSheet("height: 20px;")
        self.magic_meter = Meter(QColor(200, 0, 200), 100)
        self.magic_meter.setStyleSheet("height: 20px;")
        self.stamina_meter = Meter(QColor(50, 50, 50), 100)
        self.stamina_meter.setStyleSheet("height: 20px;")

        # What are these? --Cooper
        self.defense = 0
        self.magicDefense = 0

        # Inventory
        self.loot = []
        self.food = []
        self.weapons = []
        self.defenses = []

    def serialize(self) -> dict:
        return {
            "level": self.level,
            "name": self.name,
            "asset": DD.asset(self.image_path),
            "class": self.classType,
            "strength": self.strength,
            "intelligence": self.intelligence,
            "health": self.maxHealth,
            "curHealth": self.curHealth,
            "magic": self.maxMagic,
            "curMagic": self.curMagic,
            "stamina": self.maxStamina,
            "curStamina": self.curStamina,
            "defense": self.defense,
            "magicDefense": self.magicDefense,
            "inventory": {
                "weapons": [i.to_dict() for i in self.weapons],
                "armor": [i.to_dict() for i in self.defenses],
            },
        }

    def image(self) -> QPixmap:
        return QPixmap(self.image_path)

    def set_health(self, health: int):
        self.curHealth = min(self.maxHealth, max(0, health))
        if self.maxHealth == 0:
            percentage = 0
        else:
            percentage = (health / self.maxHealth) * 100
        self.health_lbl.setText(f"Health: {self.curHealth}")
        self.health_meter.setPercentage(percentage)

    def set_magic(self, magic: int):
        self.curMagic = min(self.maxMagic, max(0, magic))
        if self.maxMagic == 0:
            percentage = 0
        else:
            percentage = (magic / self.maxMagic) * 100
        self.magic_lbl.setText(f"Magic: {self.curMagic}")
        self.magic_meter.setPercentage(percentage)

    def set_stamina(self, stamina: int):
        self.curStamina = min(self.maxStamina, max(0, stamina))
        if self.maxStamina == 0:
            percentage = 0
        else:
            percentage = (stamina / self.maxStamina) * 100
        self.stamina_lbl.setText(f"Stamina: {self.curStamina}")
        self.stamina_meter.setPercentage(percentage)

    def add_item(self, item: Item.Item):
        kind = type(item)
        if kind is Item.Weapon:
            self.weapons.append(item)
        elif kind is Item.Armor:
            self.defenses.append(item)
        else:
            raise ValueError("Unknown item type")

    def get_items(self) -> list[Item.Item]:
        return self.weapons + self.defenses

    def clear_items(self):
        self.weapons = []
        self.defenses = []

    def reset(self):
        """Resets characters health, stamina, and magic back to the maximum amount."""
        self.set_health(self.maxHealth)
        self.set_magic(self.maxMagic)
        self.set_stamina(self.maxStamina)

    def reload(self):
        """Reloads the character's health, stamina, and magic from the last save point."""
        char = CharacterFactory.LoadCharacter(self.name)
        self.set_health(char.curHealth)
        self.set_magic(char.curMagic)
        self.set_stamina(char.curStamina)

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
        }
    }

    @staticmethod
    def createCharacter() -> Character:
        """
        Creates a character based on the given class type
        """

        character = Character()

        for weapon in Item.weapons:
            character.add_item(weapon)
        for armor in Item.armors:
            character.add_item(armor)

        return character

    @staticmethod
    def createTestChar() -> Character:
        """
        Creates a default character we can use for testing
        """
        character = CharacterFactory.createCharacter()

        for weapon in Item.weapons:
            character.add_item(weapon)
        for armor in Item.armors:
            character.add_item(armor)

        return character

    @staticmethod
    def SaveCharacter(character: Character) -> None:
        """
        Saves a character to a json file
        :param character: The character to save
        """
        save_path = "dunwoody_disaster/saves"
        os.makedirs(save_path, exist_ok=True)  # Ensure directory exists
        file_path = os.path.join(save_path, f"{character.name}.json")
        with open(file_path, "w") as f:
            json.dump(character.serialize(), f)

    @staticmethod
    def LoadCharacter(name: str) -> Character:
        """
        Loads a character from a json file
        :param name: The name of the character to load
        :return: The loaded character object
        """
        if not os.path.exists(f"dunwoody_disaster/saves/{name}.json"):
            raise FileNotFoundError(f"Character file {name}.json not found")
        with open(f"dunwoody_disaster/saves/{name}.json", "r") as f:
            data = json.loads(f.read())
            character = CharacterFactory.createFromJson(data)
            return character

    @staticmethod
    def createFromJson(json: dict) -> Character:
        char = Character()
        for key, value in json.items():
            setattr(char, key, value)
        return char

    @staticmethod
    def Cooper() -> Character:
        """"""

        char = CharacterFactory.createCharacter()
        char.name = "Cooper"
        char.maxHealth = 100
        char.maxMagic = 100
        char.maxStamina = 100
        char.reset()

        char.strength = 5
        char.intelligence = 50
        char.defense = 10
        char.magicDefense = 25

        char.weapons = [
            Item.Weapon(
                name="Syntax Error", damage=10, magic=5, stamina=5, magical=True
            ),
            Item.Weapon(
                name="Recursive Loop", damage=15, magic=5, stamina=10, magical=True
            ),
            Item.Weapon(name="Keyboard", damage=5, magic=0, stamina=3, magical=False),
        ]
        char.defenses = [
            Item.Armor(
                name="StackOverflow",
                armorVal=2,
                staminaCost=5,
                magicCost=1,
                magicDefense=10,
            ),
            Item.Armor(
                name="GDB", armorVal=5, staminaCost=5, magicCost=2, magicDefense=10
            ),
            Item.Armor(
                name="SSL Certificate",
                armorVal=10,
                staminaCost=5,
                magicCost=2,
                magicDefense=5,
            ),
        ]

        char.loot = []
        char.food = []

        char.image_path = DD.ASSETS["CooperRefined+"]
        return char

    @staticmethod
    def John() -> Character:
        """"""
        char = CharacterFactory.createCharacter()
        char.name = "John"
        char.maxHealth = 100
        char.maxMagic = 100
        char.maxStamina = 100
        char.reset()

        char.strength = 1
        char.intelligence = 1
        char.defense = 1
        char.magicDefense = 1

        char.image_path = DD.ASSETS["JohnRefined+"]
        # char.weapons = [
        #     Item.Weapon(name="", damage=5, magic=5, stamina=5, magical=True),
        #     Item.Weapon(name="", damage=5, magic=5, stamina=5, magical=False),
        #     Item.Weapon(name="", damage=5, magic=5, stamina=5, magical=False)
        # ]

        # char.defenses = [
        #     Item.Armor(name="", armorVal=5, staminaCost=5, magicCost=5, magicDefense=0),
        #     Item.Armor(name="", armorVal=5, staminaCost=5, magicCost=5, magicDefense=5)
        # ]
        return char

    @staticmethod
    def Noah() -> Character:
        """"""
        char = CharacterFactory.createCharacter()
        char.name = "Noah"
        char.maxHealth = 100
        char.maxMagic = 100
        char.maxStamina = 100
        char.reset()

        char.strength = 1
        char.intelligence = 1
        char.defense = 1
        char.magicDefense = 1

        char.image_path = DD.ASSETS["NoahRefined+"]
        # char.weapons = [
        #     Item.Weapon(name="", damage=5, magic=5, stamina=5, magical=True),
        #     Item.Weapon(name="", damage=5, magic=5, stamina=5, magical=False),
        #     Item.Weapon(name="", damage=5, magic=5, stamina=5, magical=False)
        # ]

        # char.defenses = [
        #     Item.Armor(name="", armorVal=5, staminaCost=5, magicCost=5, magicDefense=0),
        #     Item.Armor(name="", armorVal=5, staminaCost=5, magicCost=5, magicDefense=5)
        # ]
        return char

    @staticmethod
    def Mitch() -> Character:
        """Mitch is more strength and defense oriented. Weak to magic"""
        char = CharacterFactory.createCharacter()
        char.name = "Mitch"
        char.maxHealth = 120
        char.maxMagic = 40
        char.maxStamina = 80
        char.reset()

        char.strength = 30
        char.intelligence = 5
        char.defense = 30
        char.magicDefense = 5

        char.weapons = [
            Item.Weapon(name="Unreal End", damage=8, magic=15, stamina=8, magical=True),
            Item.Weapon(
                name="Thermos Throw", damage=12, magic=5, stamina=8, magical=False
            ),
            Item.Weapon(
                name="Laptop Lunge", damage=18, magic=5, stamina=10, magical=False
            ),
        ]

        char.defenses = [
            Item.Armor(
                name="Stress Ball",
                armorVal=15,
                staminaCost=5,
                magicCost=0,
                magicDefense=15,
            ),
            Item.Armor(
                name="Spaghetti Code",
                armorVal=5,
                staminaCost=5,
                magicCost=5,
                magicDefense=5,
            ),
        ]

        char.image_path = DD.ASSETS["MitchRefined+"]
        return char

    @staticmethod
    def LeAnnSimonson() -> Character:
        """LeAnn is built as a magic character, but weaker than Matthew."""
        char = CharacterFactory.createCharacter()
        char.name = "LeAnn Simonson"
        char.maxHealth = 70
        char.maxMagic = 110
        char.maxStamina = 65
        char.reset()

        char.strength = 1
        char.intelligence = 20
        char.defense = 0
        char.magicDefense = 15
        char.level = 1

        char.weapons = [
            Item.Weapon(name="Query", damage=5, magic=15, stamina=8, magical=True),
            Item.Weapon(
                name="Schema Smash", damage=8, magic=10, stamina=6, magical=True
            ),
            Item.Weapon(
                name="Index Impact", damage=12, magic=4, stamina=8, magical=False
            ),
        ]

        char.defenses = [
            Item.Armor(
                name="Firewall Fortress",
                armorVal=10,
                staminaCost=5,
                magicCost=5,
                magicDefense=0,
            ),
            Item.Armor(
                name="Query Validation",
                armorVal=0,
                staminaCost=5,
                magicCost=5,
                magicDefense=10,
            ),
        ]
        char.loot = []
        char.food = []
        char.image_path = DD.ASSETS["LeAnn"]
        return char

    @staticmethod
    def AmalanPulendran() -> Character:
        """Amalan is currently an all-around character."""
        char = CharacterFactory.createCharacter()
        char.name = "Amalan Pulendran"
        char.maxHealth = 100
        char.maxMagic = 70
        char.maxStamina = 60
        char.reset()

        char.strength = 15
        char.intelligence = 15
        char.defense = 15
        char.magicDefense = 15
        char.level = 2

        char.weapons = [
            Item.Weapon(name="API Ambush", damage=5, magic=15, stamina=8, magical=True),
            Item.Weapon(
                name="Confusion", damage=12, magic=20, stamina=12, magical=True
            ),
            Item.Weapon(
                name="DDoS Downpour", damage=15, magic=5, stamina=8, magical=False
            ),
            Item.Weapon(
                name="Patch Pummel", damage=2, magic=15, stamina=15, magical=False
            ),
        ]

        char.defenses = [
            Item.Armor(
                name="Malware Moat",
                armorVal=12,
                staminaCost=8,
                magicCost=0,
                magicDefense=5,
            ),
            Item.Armor(
                name="VPN Vigilance",
                armorVal=5,
                staminaCost=0,
                magicCost=8,
                magicDefense=12,
            ),
        ]
        char.loot = []
        char.food = []

        char.image_path = DD.ASSETS["Amalan"]
        return char

    @staticmethod
    def RyanRengo() -> Character:
        """Ryan is a bit of a glass cannon. Strong attacks, but weaker durability.
        I'm not sure if we want to keep it this way due to real-life situations..."""
        char = CharacterFactory.createCharacter()
        char.name = "Ryan Rengo"
        char.maxHealth = 80
        char.maxMagic = 70
        char.maxStamina = 45
        char.reset()

        char.strength = 25
        char.intelligence = 25
        char.defense = 5
        char.magicDefense = 5
        char.level = 3

        char.weapons = [
            Item.Weapon(
                name="API Avalanche", damage=15, magic=25, stamina=12, magical=True
            ),
            Item.Weapon(
                name="Cache Clash", damage=15, magic=15, stamina=15, magical=False
            ),
            Item.Weapon(
                name="Kubernetes Kick", damage=25, magic=12, stamina=12, magical=False
            ),
        ]

        char.defenses = [
            Item.Armor(
                name="Lambda Leap",
                armorVal=10,
                staminaCost=5,
                magicCost=5,
                magicDefense=10,
            ),
            Item.Armor(
                name="Docker Dash",
                armorVal=12,
                staminaCost=6,
                magicCost=6,
                magicDefense=12,
            ),
        ]
        char.loot = []
        char.food = []

        char.image_path = DD.ASSETS["Ryan"]
        return char

    @staticmethod
    def NoureenSajid() -> Character:
        """Noureen is currently built as a stronger character, similar to Joe."""
        char = CharacterFactory.createCharacter()
        char.name = "Noureen Sajid"
        char.maxHealth = 110
        char.maxMagic = 50
        char.maxStamina = 65
        char.reset()

        char.strength = 15
        char.intelligence = 20
        char.defense = 15
        char.magicDefense = 15
        char.level = 4

        char.weapons = [
            Item.Weapon(
                name="Short Circuit", damage=8, magic=15, stamina=8, magical=True
            ),
            Item.Weapon(
                name="Voltage Spike", damage=15, magic=8, stamina=8, magical=False
            ),
            Item.Weapon(
                name="Circuit Breaker", damage=25, magic=12, stamina=12, magical=False
            ),
        ]

        char.defenses = [
            Item.Armor(
                name="Resistor",
                armorVal=15,
                staminaCost=10,
                magicCost=8,
                magicDefense=12,
            ),
            Item.Armor(
                name="Diode Defense",
                armorVal=12,
                staminaCost=8,
                magicCost=10,
                magicDefense=15,
            ),
        ]
        char.loot = []
        char.food = []

        char.image_path = DD.ASSETS["Noureen"]
        return char

    @staticmethod
    def JoeAxberg() -> Character:
        """Joe is currently built as a strong, brute character."""
        char = CharacterFactory.createCharacter()
        char.name = "Joe Axberg"
        char.maxHealth = 120
        char.maxMagic = 40
        char.maxStamina = 50
        char.reset()

        char.strength = 20
        char.intelligence = 5
        char.defense = 15
        char.magicDefense = 0
        char.level = 5

        char.weapons = [
            Item.Weapon(name="SSH", damage=5, magic=15, stamina=5, magical=True),
            Item.Weapon(
                name="Breadboard", damage=10, magic=0, stamina=5, magical=False
            ),
            Item.Weapon(
                name="Server Rack", damage=18, magic=5, stamina=10, magical=False
            ),
        ]

        char.defenses = [
            Item.Armor(
                name="Virtualization Layer",
                armorVal=25,
                staminaCost=25,
                magicCost=0,
                magicDefense=0,
            ),
            Item.Armor(
                name="Command Line",
                armorVal=0,
                staminaCost=0,
                magicCost=15,
                magicDefense=10,
            ),
        ]

        char.loot = []
        char.food = []

        char.image_path = DD.ASSETS["Joe"]
        return char

    @staticmethod
    def MatthewBeckler() -> Character:
        """Matthew is currently the strongest magic caster."""
        char = CharacterFactory.createCharacter()
        char.name = "Matthew Beckler"
        char.maxHealth = 80
        char.maxMagic = 120
        char.maxStamina = 60
        char.reset()

        char.strength = 5
        char.intelligence = 30
        char.defense = 0
        char.magicDefense = 20
        char.level = 6

        char.weapons = [
            Item.Weapon(name="Compiler", damage=12, magic=20, stamina=12, magical=True),
            Item.Weapon(
                name="Syntax Error", damage=6, magic=15, stamina=6, magical=True
            ),
            Item.Weapon(
                name="Neural Nightmare", damage=5, magic=0, stamina=15, magical=False
            ),
        ]

        char.defenses = [
            Item.Armor(
                name="Overfitting Obstacle",
                armorVal=15,
                staminaCost=12,
                magicCost=12,
                magicDefense=20,
            ),
            Item.Armor(
                name="Bias Blockade",
                armorVal=20,
                staminaCost=12,
                magicCost=12,
                magicDefense=15,
            ),
        ]

        char.loot = []
        char.food = []
        return char

    @staticmethod
    def BillHudson() -> Character:
        """Bill is meant as a stronger version of Amalan. Strongest all-around stats."""
        char = CharacterFactory.createCharacter()
        char.name = "Bill Hudson"
        char.maxHealth = 120
        char.maxMagic = 100
        char.maxStamina = 75
        char.reset()

        char.strength = 20
        char.intelligence = 20
        char.defense = 20
        char.magicDefense = 20
        char.level = 7

        char.weapons = [
            Item.Weapon(
                name="Schedule Sabotage", damage=0, magic=12, stamina=8, magical=True
            ),
            Item.Weapon(
                name="Accredidation Ambush",
                damage=5,
                magic=20,
                stamina=13,
                magical=True,
            ),
            Item.Weapon(
                name="Policy Piracy", damage=12, magic=0, stamina=8, magical=False
            ),
            Item.Weapon(
                name="Admin Assault", damage=20, magic=0, stamina=13, magical=False
            ),
        ]

        char.defenses = [
            Item.Armor(
                name="Enrollment Error",
                armorVal=15,
                staminaCost=15,
                magicCost=0,
                magicDefense=0,
            ),
            Item.Armor(
                name="Stonewalling",
                armorVal=0,
                staminaCost=0,
                magicCost=15,
                magicDefense=15,
            ),
        ]
        char.loot = []
        char.food = []

        char.image_path = DD.ASSETS["Bill"]
        return char
