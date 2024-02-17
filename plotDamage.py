from typing import Optional


def HighestAttack(attacker: dict, defender: dict) -> Optional[dict]:
    """
    Find the players strongest attack
    :return: Attack
    """
    attackMeter = attacker["meters"]
    if attackMeter["mechanical"] == 0 or attackMeter["health"] == 0:
        return None

    defenses = DamageSoak(defender["defenses"])
    highestDamage = float("-inf")
    result = None
    for attack in attacker["attacks"]:
        if attackMeter["magic"] == 0 and attack["magic"] > 5:
            continue

        totalAttackValue = 0
        for attackValue, defenseValue in zip(MetersToTuple(attack), defenses):
            totalAttackValue += max(0, attackValue - defenseValue)
        if totalAttackValue > highestDamage:
            result = attack

    return result


def DamageSoak(defenses: list) -> tuple:
    """
    :return: total (mechanical, magic, health) scores
    """
    mech = 0
    magic = 0
    health = 0
    for defense in defenses:
        mech += defense["mechanical"]
        magic += defense["magic"]
        health += defense["health"]
    return (mech, magic, health)


def PlotDamage(attacker: dict, defender: dict) -> list:
    """
    Goes through potential attacks and their damage to the enemy depending on their defense profile
    :retuen: A list of attacks that show actual damage
    """
    defenseValues = DamageSoak(defender["defenses"])
    realAttacks = []  # How much damage each attack will really do
    attackMeter = attacker["meters"]

    for attack in attacker["attacks"]:
        if (
            (attackMeter["mechanical"] == 0 or attackMeter["health"] == 0)
            or attackMeter["magic"] == 0
            and attack["magic"] > 5
        ):
            realDamages = CreateMeters(0, 0, 0)
        else:
            attackValues = MetersToTuple(attack)
            afterDefenseValues = [
                max(0, attackValues[i] - defenseValues[i])
                for i in range(len(attackValues))
            ]
            realDamages = CreateMeters(*afterDefenseValues)

        realAttack = {"name": attack["name"]}
        realAttack.update(realDamages)
        realAttacks.append(realAttack)

    return realAttacks


def CreateMeters(mechanical: int, magic: int, health: int) -> dict:
    return {"mechanical": mechanical, "magic": magic, "health": health}


def MetersToTuple(meters: dict) -> tuple:
    """
    :return: (mech, magic, health)
    """
    return (meters["mechanical"], meters["magic"], meters["health"])


def CreateItem(name: str, meters: dict) -> dict:
    result = {"name": name}
    result.update(meters)
    return result


def CreatePlayer(meters: dict, attacks: list, defenses: list) -> dict:
    return {"meters": meters, "attacks": attacks, "defenses": defenses}


attacks = [
    CreateItem("arrows", CreateMeters(22, 5, 45)),
    CreateItem("sparrow attack", CreateMeters(45, 15, 25)),
]
defenses = [
    CreateItem("shield", CreateMeters(5, 2, 3)),
    CreateItem("bubble spell", CreateMeters(3, 3, 3)),
]

player_meters = CreateMeters(50, 50, 50)
player1 = CreatePlayer(player_meters, attacks, defenses)
player2 = CreatePlayer(player_meters, attacks, defenses)

print(PlotDamage(player1, player2))
print(HighestAttack(player1, player2))

"""
Each player has:
    mechanical meter
    magical (mana) meter
    health meter
    attack profile (consisting of attacks)
    defense profile (consisting of armor)

If a player attacks, the defending players defense is subtracted from the damage it does to that meter

# Enemy has health/magic/mechanical meters, attack & defense profile, Loot
# If mechanical or health are zero, you cannot attack
# Defense profile is additive and subtracts from attack
# Only one attack at a time, alternating turns
"""
