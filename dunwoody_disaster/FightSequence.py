from dunwoody_disaster import CharacterFactory, Item
from dunwoody_disaster.CharacterFactory import Character
from dunwoody_disaster.views.action_selector import ActionSelector
from dunwoody_disaster.views.fightScreen import FightScreen


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
