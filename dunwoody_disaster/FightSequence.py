from dunwoody_disaster import CharacterFactory, Item
from dunwoody_disaster.CharacterFactory import Character
from dunwoody_disaster.views import action_selector
import random


class FightSequence:
    def __init__(
        self, player: CharacterFactory.Character, enemy: CharacterFactory.Character
    ):
        self.player = player
        self.enemy = enemy

    def Fight(
        self,
        playerActions: action_selector.ActionSelector,
        enemyActions: action_selector.ActionSelector,
    ) -> tuple[CharacterFactory.Character, CharacterFactory.Character]:
        """
        Simulates a fight between player and enemy
        :param playerActions: The actions the player is using
        :param enemyActions: The actions the enemy is using
        :return: The updated player and enemy characters
        """
        playerWeapon = playerActions.attack
        enemyWeapon = enemyActions.attack
        playerDefense = playerActions.defense
        enemyDefense = enemyActions.defense

        # putting this here so the typechecker shuts up --Cooper
        if not (playerWeapon and enemyWeapon and playerDefense and enemyDefense):
            raise Exception("Players did not select items")

        canPlayerAttack = self.CanAttack(self.player, playerWeapon)
        canEnemyAttack = self.CanAttack(self.enemy, enemyWeapon)

        if canPlayerAttack:
            playerDamage = self.CalculateDamage(self.player, playerWeapon, enemyDefense)
            self.player.curStamina -= playerWeapon.staminaCost
            self.enemy.curHealth -= playerDamage
        if canEnemyAttack:
            enemyDamage = self.CalculateDamage(self.enemy, enemyWeapon, playerDefense)
            self.enemy.curStamina -= enemyWeapon.staminaCost
            self.player.curHealth -= enemyDamage

        return self.player, self.enemy

    def CanAttack(self, player: Character, attack: Item.Weapon) -> bool:
        """
        Checks to see if character has enough stamina or magic to attack with.
        """
        return (
            player.curStamina - attack.staminaCost >= 0
            and player.curMagic >= attack.magicReq
        )

    def CalculateDamage(
        self, player: Character, playerAttack: Item.Weapon, targetDefense: Item.Armor
    ):
        """
        Calculates damage based on playerAttack vs the targets defensive item.
        """
        if playerAttack.magic:
            attackDamage = (
                playerAttack.damage + player.intelligence
            ) - targetDefense.magicDefense
        else:
            attackDamage = (
                playerAttack.damage + player.strength
            ) - targetDefense.armorVal
        print("attack damage: ", attackDamage)
        if attackDamage > 0:
            return attackDamage
        return 0

    def EnemySelectArsenal(
        self, enemy: Character, selection: action_selector.ActionSelector
    ):
        """
        Use this to make enemy select one weapon to use and one defensive item to use.
        """
        # Random number based on number/length of enemy weapons. Same for defense
        attackChoice = random.choice(enemy.weapons)
        defenseChoice = random.choice(enemy.defenses)

        selection.set_attack(attackChoice)
        selection.set_defense(defenseChoice)
