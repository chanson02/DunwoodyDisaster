# Dictionary of food items and their attributes: [weight, health]
FoodDict = {
    "Bread": [10, 0],
    "Apple": [5, 0],
    "Chicken Head": [20, 20],
    "Thorny Fruit": [-20, -20],
}

# Dictionary of repair items and their attributes: [Mechanical]
RepairItems = {"Wrench": 10, "Toolkit": 30, "Repair Box": 100}

# Dictionary of player's statistics: Health, Magic, Mechanical
PlayerStats = {"Health": 100, "Magic": 100, "Mechanical": 100}


# Function to heal the player
def Heal(foodDict, meter):
    """
    Function to heal the player.

    :param food_dict: Dictionary of food items and their attributes.
    :param meter: Dictionary of player's statistics.
    """

    # Display available healing items
    print("Choose a healing item:")
    for item, values in foodDict.items():
        print(f"{item}: {values[0]} health points and {values[1]} Magic points")
    for item, values in RepairItems.items():
        print(f"{item}: {values[0]} Mechanical points")
    selectedItem = input("Item: ")

    # Check if the selected item is a healing item
    if selectedItem in foodDict:
        # Update the health and magic meters and store the updated values
        meter["Health"] = max(0, min(100, meter["Health"] + foodDict[selectedItem][0]))
        meter["Magic"] = max(0, min(100, meter["Magic"] + foodDict[selectedItem][1]))

        # Print the updated values
        print(f"Health restored by {foodDict[selectedItem][0]} points!")
        print(f"Current health: {meter['Health']}")
        print(f"Magic restored by {foodDict[selectedItem][1]} points!")
        print(f"Current magic: {meter['Magic']}")

    # Check if the selected item is a repair item
    if selectedItem in RepairItems:
        # Update the Mechanical meter and store the updated value
        meter["Mechanical"] = max(
            0, min(100, meter["Mechanical"] + RepairItems[selectedItem][0])
        )
        print(f"Mechanical restored by {RepairItems[selectedItem][0]} points!")
        print(f"Current Mechanical: {meter['Mechanical']}")
    else:
        print("Invalid item")


# Dictionary of action moves, including the "Heal" action which calls the Heal function
action_moves = {"Attack": None, "Defend": None, "Heal": Heal}


# Main game loop
def main():
    while PlayerStats["Health"] > 0:
        # Print out the available action moves
        print("Action Moves:")
        for move in action_moves:
            print(move)

        UserChoice = input(str("Choose Action: "))

        # Check if the user's choice is a valid action move
        if UserChoice not in action_moves:
            print("\nInvalid Action\nChoose one of listed actions\n")
            continue

        # Call the Heal function if the user chooses to heal
        if UserChoice == "Heal":
            action_moves[UserChoice](FoodDict, PlayerStats)

        """if UserChoice in action_moves:
            if UserChoice == "Heal":
                action_moves[UserChoice](FoodDict, PlayerStats)
            else:
                print("This action is not made yet.")
        else:
            print("Invalid Action") """

        # Check if the player's health is zero or negative
        if PlayerStats["Health"] == 0:
            print("You are dead")
            break

        # Check if the player's magic is zero or negative
        if PlayerStats["Magic"] == 0:
            print("You ran out of mana")

        # Ask the player if they want to perform another action
        choice = input("Do you want to perform another action? (yes/no) ")
        if choice.lower() != "yes":
            break


main()
