import copy


risk_levels = {
    "high": "is a high risk attack",
    "medium": "is a medium risk attack",
    "low": "is a low risk attack",
    "none": "is a no risk attack",
}


class Character:
    # info
    name = ""
    classType = ""
    # stats
    health = 100
    magic = 0
    mechanical = 15
    defence = 0
    magicDefence = 0
    level = 1

    # inventory
    loot = []
    food = []

    def __init__(self, name):
        self.name = name

    def plotRisk(
        self, attacks
    ):  # goes through enemies potential attacks and damage according to our defense profile Me
        # est time 1hr
        # total time 30mins
        attacksCopy = copy.deepcopy(attacks)
        risks = [
            "is a high risk attack",
            "is a medium risk attack",
            "is a low risk attack",
            "is a no risk attack",
        ]

        global health
        for attack in attacksCopy:
            attackName = attack.pop(0)

            mechDamage = attack.pop(0)
            magicDamage = attack.pop(0)
            healthDamage = attack.pop(0)

            if self.mechanical <= mechDamage:
                att = f"{attackName} {risks[0]}"
                print(att)  # will "stun" the character
                continue
            totalDamage = 0
            totalDamage += (
                magicDamage - self.magicDefence
                if self.magicDefence < magicDamage
                else 0
            )
            totalDamage += (
                healthDamage - self.defence if self.defence < healthDamage else 0
            )

            if self.health - totalDamage <= 0:
                print(f"{attackName} {risks[0]}")
                continue  # will kill the character
            elif totalDamage > self.health / 2:
                print(f"{attackName} {risks[1]}")
                continue  # a lot of damage to the character
            elif totalDamage > self.health / 4:
                print(f"{attackName} {risks[2]}")
                continue  # a little damage the character
            else:
                print(f"{attackName} {risks[3]}")
                continue

    def plotDamage():  # goes through potential attacks and their damage to the enemy depending on his defense profile cooper
        pass

    def sortLoot():  # sort the loot array into our different bags mitch
        pass

    def heal():  # searches food items for needed nutritional value then consumes them for points, changes health meter accordingly John
        pass


att = [["arrows", 25, 5, 45], ["sparrow attack", 45, 15, 25]]
char = Character("Noah")

char.plotRisk(att)
# level up
char.mechanical = 100
char.magicDefense = 100
char.defense = 100
char.health = 10
char.PlotRisk(att)
