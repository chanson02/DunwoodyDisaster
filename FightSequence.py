from CharacterFactory import Character
from fightScreen import UpdateMeters

class FightSequence:
    def __init__(self, player, enemy):
        self.player = player
        self.enemy = enemy

    def Fight(self, playerAttack, enemyAttack):
        """
        Simulates a fight between player and enemy
        :param playerAttack: The attack the player is using
        :param enemyAttack: The attack the enemy is using
        :return: The stat changes for the player and enemy
        """
        canPlayerAttack = self.CanAttack(self.player, playerAttack)
        canEnemyAttack = self.CanAttack(self.enemy, enemyAttack)

        if(canPlayerAttack):
            playerDamage = self.CalculateDamage(playerAttack, self.player, self.enemy)
            self.player.curStamina -= playerAttack.staminaCost
            self.enemy.health -= playerDamage
            self.UpdateMeters(self.player, self.player.meters)
        if(canEnemyAttack):
            enemyDamage = self.CalculateDamage(enemyAttack, self.enemy, self.player)
            self.enemy.curStamina -= enemyAttack.staminaCost
            self.player.health -= enemyDamage
            self.UpdateMeters(self.enemy, self.enemy.meters)
        
        
        return self.player, self.enemy
    
        
    def CanAttack(self, player, attack) -> bool:
        if(player.curStamina - attack.staminaCost >= 0 and player.curMagic >= attack.magicCost):
            return True
        else:
            return False

    def CalculateDamage(attack, attacker, target):
        attackDamage = attack 
        

        return attackDamage