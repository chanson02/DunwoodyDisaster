from dunwoody_disaster import CharacterFactory, Item
from dunwoody_disaster.CharacterFactory import Character
from dunwoody_disaster.views import fightScreen


class FightSequence:
    def __init__(
        self, player: CharacterFactory.Character, enemy: CharacterFactory.Character
    ):
        self.player = player
        self.enemy = enemy

    def Fight(
        self, playerWeapon: Item.Weapon, enemyWeapon: Item.Weapon,
        playerDefense: Item.Armor, enemyDefense: Item.Armor
    ) -> tuple[CharacterFactory.Character, CharacterFactory.Character]:
        """
        Simulates a fight between player and enemy
        :param playerAttack: The attack the player is using
        :param enemyAttack: The attack the enemy is using
        :return: The stat changes for the player and enemy
        """
        print("Fighting")
        canPlayerAttack = self.CanAttack(self.player, playerWeapon)
        canEnemyAttack = self.CanAttack(self.enemy, enemyWeapon)
        print("thye can attack")
        if canPlayerAttack:
            playerDamage = self.CalculateDamage(self.player, playerWeapon, enemyDefense)
            self.player.curStamina -= playerWeapon.staminaCost
            self.enemy.curHealth -= playerDamage
            fightScreen.UpdateMeters(self.player, self.player.meters)
        if canEnemyAttack:
            enemyDamage = self.CalculateDamage(self.enemy, enemyWeapon, playerDefense)
            self.enemy.curStamina -= enemyWeapon.staminaCost
            self.player.curHealth -= enemyDamage
            fightScreen.UpdateMeters(self.enemy, self.enemy.meters)

        return self.player, self.enemy

    def CanAttack(
        self, player: Character, attack: Item.Weapon
    ) -> bool:
        """
        Checks to see if character has enough stamina or magic to attack with.
        """
        return (
            player.curStamina - attack.staminaCost >= 0
            and player.curMagic >= attack.magicReq
        )

    def CalculateDamage(self, player:Character, playerAttack: Item.Weapon, targetDefense: Item.Armor):
        """
        Calculates damage based on playerAttack vs the targets defensive item.
        """
        attackDamage = playerAttack.damage - targetDefense.armorVal

        return attackDamage
