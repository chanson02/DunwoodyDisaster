from dunwoody_disaster import CharacterFactory, Item
from dunwoody_disaster.views import fightScreen

class FightSequence:
    def __init__(self, player, enemy):
        self.player = player
        self.enemy = enemy

    def Fight(self, playerWeapon, enemyWeapon):
        """
        Simulates a fight between player and enemy
        :param playerAttack: The attack the player is using
        :param enemyAttack: The attack the enemy is using
        :return: The stat changes for the player and enemy
        """
        
        canPlayerAttack = self.CanAttack(self.player, playerWeapon)
        canEnemyAttack = self.CanAttack(self.enemy, enemyWeapon)

        if(canPlayerAttack):
            playerDamage = self.CalculateDamage(playerWeapon, self.player, self.enemy)
            self.player.curStamina -= playerWeapon.staminaCost
            self.enemy.health -= playerDamage
            fightScreen.UpdateMeters(self.player, self.player.meters)
        if(canEnemyAttack):
            enemyDamage = self.CalculateDamage(enemyWeapon, self.enemy, self.player)
            self.enemy.curStamina -= enemyWeapon.staminaCost
            self.player.health -= enemyDamage
            fightScreen.UpdateMeters(self.enemy, self.enemy.meters)
        
        
        return self.player, self.enemy
    
        
    def CanAttack(self, player, attack) -> bool:
        """
        
        """
        if(player.curStamina - attack.staminaCost >= 0 and player.curMagic >= attack.magicCost):
            return True
        else:
            return False

    def CalculateDamage(playerAttack : Item.Weapon, targetDefense : Item.Armor):
        """
        
        """
        attackDamage = playerAttack.damage - targetDefense.armorVal
        
        return attackDamage