from dunwoody_disaster import CharacterFactory, Item
from dunwoody_disaster.CharacterFactory import Character
from dunwoody_disaster.views.action_selector import ActionSelector
from dunwoody_disaster.views.fightScreen import FightScreen
import random


class FightSequence:
    def __init__(
        self, player: CharacterFactory.Character, enemy: CharacterFactory.Character
    ):
        self.player = player
        self.enemy = enemy
        self.widget = FightScreen(self)

    def takeTurn(self, playerActions: ActionSelector, enemyActions: ActionSelector):
        """
        Update the characters after using a move
        :param playerActions: The actions the player is using
        :param enemyActions: The actions the enemy is using
        """
        playerDmg = self.calculateDamage(self.player, enemyActions.getAttack(), playerActions.getDefense())
        enemyDmg = self.calculateDamage(self.enemy, playerActions.getAttack(), enemyActions.getDefense())

    def calculateDamage(self, player: Character, attack: Item.Weapon, defense: Item.Armor):
        """
        :param player: The player being attacked
        :param attack: The attack the opponent is using
        :param defense: The defense the player is using
        :return: A positive integer representing the damage done to the player
        """
        if attack.magic:
            dmg = attack.damage + player.intelligence - defense.magicDefense
        else:
            dmg = attack.damage + player.strength - defense.armorVal

        return max(0, dmg)


    #     # putting this here so the typechecker shuts up --Cooper
    #     if not (playerWeapon and enemyWeapon and playerDefense and enemyDefense):
    #         raise Exception("Players did not select items")
    #
    #     canPlayerAttack = self.CanAttack(self.player, playerWeapon)
    #     canEnemyAttack = self.CanAttack(self.enemy, enemyWeapon)
    #
    #     if canPlayerAttack:
    #         playerDamage = self.CalculateDamage(self.player, playerWeapon, enemyDefense)
    #         self.player.curStamina -= playerWeapon.staminaCost
    #         self.enemy.curHealth -= playerDamage
    #     if canEnemyAttack:
    #         enemyDamage = self.CalculateDamage(self.enemy, enemyWeapon, playerDefense)
    #         self.enemy.curStamina -= enemyWeapon.staminaCost
    #         self.player.curHealth -= enemyDamage
    #
    #     return self.player, self.enemy
    #
    # def CanAttack(self, player: Character, attack: Item.Weapon) -> bool:
    #     """
    #     Checks to see if character has enough stamina or magic to attack with.
    #     """
    #     return (
    #         player.curStamina - attack.staminaCost >= 0
    #         and player.curMagic >= attack.magicReq
    #     )
