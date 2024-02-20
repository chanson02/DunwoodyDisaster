
# We are going to start building a game together. The ultimate goal here is for everyone to gain a strong understanding of
# the code. We are going to simulate a super accelerated agile development practice. Where we will regroup every 30 minutes to 
# determine the best way forward.

def PlotRisk(): # goes through enemies potential attacks and damage according to our defense profile
    pass
def PlotDamage(): # goes through potential attacks and their damage to the enemy depending on his defense profile
    pass
   
        
    
# lootDict = {'item1' : {'itemName' : 'MagicWand','itemType' : 'weapon', 'itemStats': [3, 2, 1] },
            
#             'item2' : {'itemName' : 'gloves', 'itemType' : 'defense','itemStats': [1, 1, 2] }
#             }

playerInventory = {}

lootDict = {'MagicWand': ['weapon', 3, 2, 1],
             'gloves' : ['defense', 1, 1, 2],
             'banana' : ['food', 10, 5],
             'tape' : ['supplies', 5]}
    
         
def SortLoot(loot: dict, playerInv: dict):
    weapons = {}
    defense = {}
    food = {}
    supplies = {}
    
    for itemName in loot:
        # print('item:', itemName)
        for item in loot[itemName]:
            # print('itemName:', item)
            if item == 'weapon':
                loot[itemName].remove('weapon')
                weapons.update({itemName : loot[itemName]})
            elif item == 'defense':
                loot[itemName].remove('defense')
                defense.update({itemName : loot[itemName]})
            elif item == 'food':
                loot[itemName].remove('food')
                food.update({itemName : loot[itemName]})
            elif item == 'supplies':
                loot[itemName].remove('supplies')
                supplies.update({itemName : loot[itemName]})
                
    playerInv = {**weapons, **defense, **food, **supplies}
    return(playerInv)
    
  
 
           
def Heal(): # searches food items for needed nutritional value then consumes them for points, changes health meter accordingly
    pass


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
