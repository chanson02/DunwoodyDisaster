FoodDict = {"Bread": [10, 0],
            "Apple": [5, 0],
            "Chicken Head": [20, 20],
            "Thorny Fruit": [-20, -20]
            }

RepairItems = {"Wrench": [10],
               "Toolkit": [30],
               "Repair Box": [100]
            }

PlayerStats = {"Health": 100,
             "Magic": 100,
             "Supply": 100}



def Heal(foodDict, meter):
    print("Choose a healing item:")
    for item, values in foodDict.items():
        print(f"{item}: {values[0]} health points and {values[1]} Magic points")
    for item, values in RepairItems.items():
        print(f"{item}: {values[0]} supply points")
    selectedItem = input('Item: ')

    if selectedItem in foodDict:
        # Update the health and magic meters directly and store the updated values
        meter["Health"] = max(0, min(100, meter["Health"] + foodDict[selectedItem][0]))
        meter["Magic"] = max(0, min(100, meter["Magic"] + foodDict[selectedItem][1]))

        # Print the updated values
        print(f"Health restored by {foodDict[selectedItem][0]} points!")
        print(f"Current health: {meter['Health']}")
        print(f"Magic restored by {foodDict[selectedItem][1]} points!")
        print(f"Current magic: {meter['Magic']}")

    if selectedItem in RepairItems:
        meter["Supply"] = max(0, min(100, meter["Supply"] + RepairItems[selectedItem][0] ))
        print(f"Supply restored by {RepairItems[selectedItem][0]} points!")
        print(f"Current Supply: {meter['Supply']}")

    else:
        print("Invalid item")


action_moves = {"Attack": None,
        "Defend": None,
        "Heal": Heal}


while PlayerStats["Health"] >= 1: 
  
    # Print out the action moves
    print("Action Moves:")
    for move in action_moves:
        print(move)

    UserChoice = input(str("Choose Action: "))

    if UserChoice in action_moves:
        if UserChoice == "Heal":
            action_moves[UserChoice](FoodDict, PlayerStats)
        else:
            print("This action is not made yet.")
    else:
        print("Invalid Action")

    
    if PlayerStats["Health"] == 0:
        print("You are dead")
        break

    if PlayerStats["Magic"] == 0:
        print("You ran out of mana")

    choice = input("Do you want to perform another action? (yes/no) ")
    if choice.lower() != 'yes':
        break