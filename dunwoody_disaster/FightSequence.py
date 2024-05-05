from dunwoody_disaster import CharacterFactory, Item
from dunwoody_disaster.CharacterFactory import Character
from dunwoody_disaster.views.action_selector import ActionSelector
from dunwoody_disaster.views.fightScreen import FightScreen
from typing import Callable
import dunwoody_disaster as DD
from PySide6.QtCore import QTimer, Signal
from functools import partial
from dunwoody_disaster.animations.basic_attack import AttackAnimation
from PySide6.QtWidgets import QWidget


class FightSequence(QWidget):
    signal = Signal()
    def __init__(
            self, player: CharacterFactory.Character, enemy: CharacterFactory.Character, battlefield: str
    ):
        super().__init__()
        self.player = player
        self.enemy = enemy
        self.widget = FightScreen(self, battlefield)
        self._locked = False

        self._winCallback = DD.unimplemented
        self._loseCallback = DD.unimplemented

    def takeTurn(self, playerActions: ActionSelector, enemyActions: ActionSelector):
        """
        Show enemy actions, then pause.
        """
        if self._locked:
            return

        self._locked = True
        enemyActions.show()

        callback = partial(self.finishTurn, playerActions, enemyActions)
        try:
            self.signal.disconnect()
        except RuntimeError:
            pass
        self.signal.connect(callback)
        animation = AttackAnimation(self.widget.background, self.player.image_path, self.enemy.image_path, playerActions.getAttack().image, self.signal)
        self.widget.animation_Object.setAnimation(animation)
        print('created attack animation')

    def finishTurn(self, playerActions: ActionSelector, enemyActions: ActionSelector):
        """
        Update the characters after using a move
        :param playerActions: The actions the player is using
        :param enemyActions: The actions the enemy is using
        """
        enemyActions.hide()
        self.widget.animation_Object.setAnimation(self.widget.idleAnimation)
        print('calling finish turn')

        playerDmg = self.calculateDamage(
            self.player, enemyActions.getAttack(), playerActions.getDefense()
        )
        enemyDmg = self.calculateDamage(
            self.enemy, playerActions.getAttack(), enemyActions.getDefense()
        )

        self.player.set_health(self.player.curHealth - playerDmg)
        self.player.set_magic(
            self.player.curMagic - playerActions.getAttack().magicCost
        )
        self.player.set_stamina(
            self.player.curStamina - playerActions.getAttack().staminaCost
        )

        self.enemy.set_health(self.enemy.curHealth - enemyDmg)
        self.enemy.set_magic(self.enemy.curMagic - enemyActions.getAttack().magicCost)
        self.enemy.set_stamina(
            self.enemy.curStamina - enemyActions.getAttack().staminaCost
        )

        playerActions.clear()
        enemyActions.selectRandom()

        if self.enemy.curHealth <= 0:
            self._winCallback()
        elif self.player.curHealth <= 0:
            self.player.reload()
            self.enemy.reset()
            self._loseCallback()

        self._locked = False
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

    def onWin(self, callback: Callable):
        self._winCallback = callback

    def onLose(self, callback: Callable):
        self._loseCallback = callback
