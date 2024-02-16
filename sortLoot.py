
# We are going to start building a game together. The ultimate goal here is for everyone to gain a strong understanding of
# the code. We are going to simulate a super accelerated agile development practice. Where we will regroup every 30 minutes to 
# determine the best way forward.

def PlotRisk(): # goes through enemies potential attacks and damage according to our defense profile
    pass
def PlotDamage(): # goes through potential attacks and their damage to the enemy depending on his defense profile
    pass
   
def SortLoot(loot): # sort the loot array into our different bags
    weapons = []
    defense = []
    food = []
    supplies = []
    
    for item in loot:
        if('weapon' in item):
            item.remove('weapon')
            weapons.append([item[0]] + item[1])
            
        elif('defense' in item):
            item.remove('defense')
            defense.append([item[0]] + item[1])
        elif('food' in item):
            item.remove('food')
            food.append([item[0]] + item[1])
        elif('supplies' in item):
            item.remove('supplies')
            supplies.append(item)
        
    
  
                
            
def Heal(): # searches food items for needed nutritional value then consumes them for points, changes health meter accordingly
    pass


#lootPile1 = [['MagicWand', 'weapon', [3, 2, 1]],
#              ['gloves', 'defense', [1, 1, 2]],
#              ['banana', 'food', [10, 5]],
#              ['tape', 'supplies', 5]]
# print(lootPile1[0][2])
SortLoot(lootPile1)
# Example attack profile:
# [[weapon, mechanical damage int, magic damage int, health damage int], 

# [[‘arrows’, 25, 5, 45], ['sparrow attack', 45, 15, 25], ...]

# Example defense profile:
# [[defenseType, mechanical defense int, magic defense int, health defense int], 

# [[‘shield’, 5, 2, 3], ['bubble spell', 3, 3, 3], ...]

# Example Loot Pile:
# [[nameOfItem, objectType, [attack/defense profile or nutrient value], ...]
# object Types are either 'food', 'weapon', 'defense'
# food item would be ['foodName', 'food', [vitC_Value, vitB_Value]]
# supplies would be ['supplyName', 'supplies', repairValue]
# lootPile1 = [['MagicWand', 'weapon', [3, 2, 1]],
#              ['gloves', 'defense', [1, 1, 2]],
#              ['banana', 'food', [10, 5]],
#              ['tape', 'supplies', 5]]

# For Healing:
# vitC heals health
# vitB heald magic
# supplies repair mechanical

# Enemy has health/magic/mechanical meters, attack & defense profile, Loot 
# If mechanical or health are zero, you cannot attack
# If magic is zero, you may not use attacks with more than 5 magic damage
# Defense profile is additive and subtracts from attack
# Only one attack at a time, alternating turns
