import copy


risk_levels = {
        "high": "is a high risk attack",
        "medium": "is a medium risk attack",
        "low": "is a low risk attack",
        "none": "is a no risk attack"
}

class Character:
        #info
        name = ""
        classType = ""
        #stats
        health = 100
        magic = 0
        mechanical = 15
        defense = 0
        magicDefense = 0
        level = 1

        #inventory
        loot = []
        food = []


        def __init__(self, name):
                self.name = name

        def PlotRisk(self, attacks): # goes through enemies potential attacks and damage according to our defense profile Me
                #est time 1hr
                #total time 30mins
                attacksCopy = copy.deepcopy(attacks)

                global health
                for attack in attacksCopy:
                        attackName = attack.pop(0)

                        mechDamage = attack.pop(0)
                        magicDamage = attack.pop(0)
                        healthDamage = attack.pop(0)
                        
                        if self.mechanical <= mechDamage:
                                att = f"{attackName} {risk_levels['high']}"
                                print(att) #will "stun" the character 
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

att = [['arrows', 25, 5, 45], ['sparrow attack', 45, 15, 25]]
char = Character("Noah")

char.PlotRisk(att)
#level up
char.mechanical = 100
char.magicDefense = 100
char.defense = 100
char.health = 10
char.PlotRisk(att)
