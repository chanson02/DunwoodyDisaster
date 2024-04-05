from CharacterFactory import Character

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
        playerDamage = self.CalculateDamage(playerAttack, self.player)
        enemyDamage = self.CalculateDamage(enemyAttack, self.enemy)

        self.player.health -= enemyDamage
        self.enemy.health -= playerDamage

        return self.player, self.enemy
    
    #I need to confirm a move can be played based off a player's stats and return a boolean
    def CanPlayMove(self, player, move):
        if player.mechanical >= move.mechanicalCost and player.magic >= move.magicCost:
            return True
        else:
            return False