from PySide6.QtWidgets import QWidget, QLayout, QLabel, QHBoxLayout
from PySide6.QtGui import QPixmap
from typing import Optional
from dunwoody_disaster import Item
from dunwoody_disaster.CharacterFactory import Character
import dunwoody_disaster as DD
import random


class ActionSelector(QWidget):
    def __init__(self, character: Character):
        super().__init__()
        self.character = character
        self.attack: Optional[Item.Weapon] = None
        self.defense: Optional[Item.Armor] = None
        self.setLayout(self.createLayout())

    def setAttack(self, item: Optional[Item.Weapon]):
        if item is not None:
            staminaCost = item.staminaCost
            magicCost = item.magicReq
            # TODO: Implement
            # if self.defense:
            #     staminaCost += self.defense.staminaCost
            #     magicCost += self.defense.magicReq

            if staminaCost > self.character.curStamina or magicCost > self.character.curMagic:
                # Do not let them select if they can't
                item = None

        self.attack = item
        self.updateUI()

    def setDefense(self, item: Optional[Item.Armor]):
        # TODO: Implement
        # if item is not None:
        #     staminaCost = item.staminaCost
        #     magicCost = item.magicReq
        #     if self.attack:
        #         staminaCost += self.self.attack.staminaCost
        #         magicCost += self.self.attack.magicReq
        #
        #     if staminaCost > self.character.curStamina or magicCost > self.character.curMagic:
        #         # Do not let them select if they can't
        #         item = None

        self.defense = item
        self.updateUI()

    def getAttack(self) -> Item.Weapon:
        if self.attack is None:
            raise Exception("Attack not set")
        return self.attack

    def getDefense(self) -> Item.Armor:
        if self.defense is None:
            raise Exception("Defense not set")
        return self.defense

    def updateUI(self):
        if self.attack:
            self.attack_pic.setPixmap(QPixmap(self.attack.image).scaledToWidth(50))
        else:
            self.attack_pic.setPixmap(QPixmap())
        if self.defense:
            self.defend_pic.setPixmap(QPixmap(self.defense.image).scaledToWidth(50))
        else:
            self.defend_pic.setPixmap(QPixmap())

    def ready(self) -> bool:
        return (self.attack and self.defense) is not None

    def selectRandom(self):
        weapons = [
                w for w in self.character.weapons
                if self.character.curMagic >= w.magicReq and self.character.curStamina >= w.staminaCost
                ]

        chosen_weapon = random.choice(weapons)
        self.setAttack(chosen_weapon)

        # TODO: Implement
        # adjustedMagic = self.character.curMagic - chosen_weapon.magicReq
        # adjustedStamina = self.character.curStamina - chosen_weapon.staminaCost
        # defenses = [
        #         w for w in self.character.defenses
        #         if adjustedMagic >= w.magicReq and adjustedStamina >= w.staminaCost
        #         ]
        self.setDefense(random.choice(self.character.defenses))

    def createLayout(self) -> QLayout:
        layout = QHBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)

        self.attack_pic = QLabel("")
        self.defend_pic = QLabel("")

        layout.addItem(DD.expander(True, False, 0))
        layout.addWidget(self.attack_pic)
        layout.addWidget(self.defend_pic)
        layout.addItem(DD.expander(True, False, 0))
        return layout
