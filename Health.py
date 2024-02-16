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

foodList = [['bread', 10, 0], ['apple', 5, 0], ['chicken head', 20, 20]]
#potions = [['small red potion', 15], ['medium red potion', 30], ['big red potion', 50]]

meterArray = [['health', 100], ['magic', 100], ['supply', 100]]



def heal(foodChoice, meter): # searches food items for needed nutritional value then consumes them for points, changes health meter accordingly
       
    print("Choose a healing item:")
    for item in foodList:
        print(f"{item[0]}: {item[1]} health points")
        selectedItem = input ('Item: ')

        if item[0] == selectedItem:
            meter[0] += item[1]
            print(f"Health restored by {item[1]} points!")
            break
    
meterArray = [100]
heal('apple',meterArray)




heal(foodList, meterArray)