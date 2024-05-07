from dunwoody_disaster import CharacterFactory, Item
from dunwoody_disaster.CharacterFactory import Character
from dunwoody_disaster.views.action_selector import ActionSelector
from dunwoody_disaster.views.fightScreen import FightScreen
from typing import Callable
import dunwoody_disaster as DD
from PySide6.QtCore import Signal
from functools import partial
from dunwoody_disaster.animations.basic_attack import AttackAnimation
from PySide6.QtWidgets import QWidget


class FightSequence(QWidget):
    signal = Signal()


    def __init__(
        self,
        player: CharacterFactory.Character,
        enemy: CharacterFactory.Character,
        battlefield: str,
    ):
        super().__init__()
        self.player = player
        self.enemy = enemy
        self.widget = FightScreen(self, battlefield)
        self._locked = False

        self._winCallback = DD.unimplemented
        self._loseCallback = DD.unimplemented

    def clearSignal(self):
        try:
            self.signal.disconnect()
        except RuntimeError:
            # signal is already disconnected
            return

    def takeTurn(self, playerActions: ActionSelector, enemyActions: ActionSelector):
        if self._locked:
            # Don't let the user spam the attack button
            return

        self.clearSignal()
        self._locked = True
        enemyActions.show()

        def playerTurn():
            attack = playerActions.getAttack()
            defense = enemyActions.getDefense()
            dmg = self.calculateDamage(self.enemy, attack, defense)
            self.enemy.set_health(self.enemy.curHealth - dmg)
            self.player.set_magic(self.player.curMagic - attack.magicCost)
            self.player.set_stamina(self.player.curStamina - attack.staminaCost)
            self.enemy.set_stamina(self.enemy.curStamina - defense.staminaCost)

            self.clearSignal()
            if self.isOver():
                finishTurn()
                return

            self.signal.connect(enemyTurn)
            animation = AttackAnimation(
                self.widget.background,
                self.enemy.image_path,
                self.player.image_path,
                enemyActions.getAttack().image,
                self.signal,
            )
            self.widget.animation_Object.setAnimation(animation)

        def enemyTurn():
            attack = enemyActions.getAttack()
            defense = playerActions.getDefense()
            dmg = self.calculateDamage(self.player, attack, defense)
            self.player.set_health(self.player.curHealth - dmg)
            self.enemy.set_magic(self.enemy.curMagic - attack.magicCost)
            self.enemy.set_stamina(self.enemy.curStamina - attack.staminaCost)
            self.player.set_stamina(self.player.curStamina - defense.staminaCost)

            finishTurn()

        def finishTurn():
            playerActions.clear()
            enemyActions.selectRandom()
            if self.enemy.curHealth <= 0:
                self._winCallback()
            elif self.player.curHealth <= 0:
                self.player.reload()
                self.enemy.reset()
                self._loseCallback()

            self.widget.animation_Object.setAnimation(self.widget.idleAnimation)
            self._locked = False

        self.signal.connect(playerTurn)
        animation = AttackAnimation(
            self.widget.background,
            self.player.image_path,
            self.enemy.image_path,
            playerActions.getAttack().image,
            self.signal,
        )
        self.widget.animation_Object.setAnimation(animation)
        return

    def calculateDamage(
        self, player: Character, attack: Item.Weapon, defense: Item.Armor
    ):
        """
        :param player: The player being attacked
        :param attack: The attack the opponent is using
        :param defense: The defense the player is using
        :return: A positive integer representing the damage done to the player
        """
        if attack.magical:
            dmg = attack.damage + player.intelligence - defense.magicDefense
        else:
            dmg = attack.damage + player.strength - defense.damage

        return max(0, dmg)

    def isOver(self) -> bool:
        return self.enemy.curHealth <= 0 or self.player.curHealth <= 0

    def onWin(self, callback: Callable):
        self._winCallback = callback

    def onLose(self, callback: Callable):
        self._loseCallback = callback
