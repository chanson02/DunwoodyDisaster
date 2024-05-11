from dunwoody_disaster import CharacterFactory, Item
from dunwoody_disaster.CharacterFactory import Character
from dunwoody_disaster.views.action_selector import ActionSelector
from dunwoody_disaster.views.fightScreen import FightScreen
from typing import Callable
import dunwoody_disaster as DD
from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget
from dunwoody_disaster.animations.LinearComponent import LinearComponent


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

        def setLockState(state: bool):
            self._locked = state
            playerActions.locked = state
            enemyActions.locked = state
            if state:
                enemyActions.show()
            else:
                enemyActions.hide()

        setLockState(True)
        playerAnimation = LinearComponent(
            playerActions.getAttack().image,
            self.signal,
            self.widget.animation.player_pos,
            self.widget.animation.enemy_pos,
            duration_ms=500,
        )

        enemyAnimation = LinearComponent(
            enemyActions.getAttack().image,
            self.signal,
            self.widget.animation.enemy_pos,
            self.widget.animation.player_pos,
            duration_ms=500,
        )

        def evaluatePlayerTurn():
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

            self.signal.connect(evaluateEnemyTurn)
            self.widget.animation.components.append(enemyAnimation)

        def evaluateEnemyTurn():
            attack = enemyActions.getAttack()
            defense = playerActions.getDefense()
            dmg = self.calculateDamage(self.player, attack, defense)
            self.player.set_health(self.player.curHealth - dmg)
            self.enemy.set_magic(self.enemy.curMagic - attack.magicCost)
            self.enemy.set_stamina(self.enemy.curStamina - attack.staminaCost)
            self.player.set_stamina(self.player.curStamina - defense.staminaCost)

            finishTurn()

        def finishTurn():
            setLockState(False)
            playerActions.clear()
            enemyActions.clear()
            enemyActions.selectRandom()
            if self.enemy.curHealth <= 0:
                if self.enemy.name == "Bill Hudson":
                    self._winGameCall()
                else:
                    self._winCallback()
            elif self.player.curHealth <= 0:
                self.player.reload()
                self.enemy.reset()
                self._loseCallback()

        self.signal.connect(evaluatePlayerTurn)
        self.widget.animation.components.append(playerAnimation)
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

    def onWinGame(self, callback: Callable):
        self._winGameCall = callback
