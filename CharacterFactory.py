import copy

class CharacterFactory:
        def __init__(self):
                pass

        def createCharacter(self, name, classType): # creates a character with the given name and classType
                char = Character(name, classType)
                return char

# Dictionary of class types
# [name, classType, health, magic, mechanical, defense, magicDefense, level, loot, food ]
# basic class types, can be tweaked and added to as needed
class_type = {
        "blank": ["blank", 100, 0, 0, 0, 0, 0, 1, [], []],
        "warrior": ["warrior", 100, 0, 15, 0, 0, 1, [], []],
        "mage":["mage", 100, 15, 0, 0, 0, 1, [], []],
        "thief": ["thief", 100, 0, 10, 0, 0, 1, [], []]
}

risk_levels = {
        "high": "is a high risk attack",
        "medium": "is a medium risk attack",
        "low": "is a low risk attack",
        "none": "is a no risk attack"
}

class Character:
        # info
        name = ""
        classType = class_type["blank"]
        # stats
        health = 100
        magic = 0
        mechanical = 15
        defense = 0
        magicDefense = 0
        level = 1

        # inventory
        loot = []
        food = []


        def __init__(self, name, classType):
                self.classType = class_type[classType][1]
                self.health = class_type[classType][2]
                self.magic = class_type[classType][3]
                self.mechanical = class_type[classType][4]
                self.defense = class_type[classType][5]
                self.magicDefense = class_type[classType][6]
                self.level = class_type[classType][7]
                self.loot = class_type[classType][8]
                self.food = class_type[classType][9]
                self.name = name


        def PlotRisk(self, attacks): # goes through enemies potential attacks and damage according to our defense profile
                attacksCopy = copy.deepcopy(attacks)

                global health
                for attack in attacksCopy:
                        attackName = attack.pop(0)

                        mechDamage = attack.pop(0)
                        magicDamage = attack.pop(0)
                        healthDamage = attack.pop(0)
                        
                        if self.mechanical <= mechDamage:
                                att = f"{attackName} {risk_levels['high']}"
                                print(att) # will "stun" the character 
                                continue  
                        totalDamage = 0
                        totalDamage += magicDamage - self.magicDefense if self.magicDefense < magicDamage else 0
                        totalDamage += healthDamage - self.defense if self.defense < healthDamage else 0

                        if self.health - totalDamage <= 0:
                                print(f"{attackName} {risk_levels['high']}")
                                continue #will kill the character
                        elif totalDamage > self.health/2:
                                print(f"{attackName} {risk_levels['medium']}")    
                                continue #a lot of damage to the character
                        elif totalDamage > self.health/4:  
                                print(f"{attackName} {risk_levels['low']}")   
                                continue #a little damage the character
                        else:
                                print(f"{attackName} {risk_levels['none']}")
                                continue
                
        def PlotDamage(): # goes through potential attacks and their damage to the enemy depending on his defense profile cooper
                pass

        def SortLoot(): # sort the loot array into our different bags mitch
                pass

        def Heal(): # searches food items for needed nutritional value then consumes them for points, changes health meter accordingly John
                pass