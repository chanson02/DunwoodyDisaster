# For Healing:
# vitC heals health
# vitB heal magic
# supplies repair mechanical

# food item would be ['foodName', 'food', [vitC_Value, vitB_Value]]

# Enemy has health/magic/mechanical meters, attack & defense profile, Loot 
# If mechanical or health are zero, you cannot attack
# If magic is zero, you may not use attacks with more than 5 magic damage
# Defense profile is additive and subtracts from attack
# Only one attack at a time, alternating turns

""" foodList = [['bread', 10, 0], ['apple', 5, 0], ['chicken head', 20, 20]] """

""" potions = [['small red potion', 15], ['medium red potion', 30], ['big red potion', 50]] """

foodDict = {"Bread": [10, 0],
            "Apple": [5, 0],
            "Chicken Head": [20,20]}

""" meterArray = [['health', 100], ['magic', 100], ['supply', 100]] """

meterDict = {"Health": 100,
             "Magic": 100,
             "Supply": 100}

def heal(foodDict, meter): # searches food items for needed nutritional value then consumes them for points, changes health meter accordingly
       
    print("Choose a healing item:")
    for item, values in foodDict.items():
        print(f"{item}: {values[0]} health points and {values[1]} Magic points")
    selectedItem = input ('Item: ')

    if selectedItem in foodDict:
        meter[0] += foodDict[selectedItem][0]
        print(f"Health restored by {foodDict[selectedItem][0]} points!")
        print(f"Magic restored by {foodDict[selectedItem][1]} points!")
    else:
        print("Invalid item")
    




heal(foodDict, meterArray)