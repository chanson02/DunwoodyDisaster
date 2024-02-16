from typing import Optional


def highestAttack(attacker: dict, defender: dict) -> Optional[dict]:
    """
    Find the players strongest attack
    :return: Attack
    """
    attack_meter = attacker["meters"]
    if attack_meter["mechanical"] == 0 or attack_meter["health"] == 0:
        return None

    defenses = damageSoak(defender["defenses"])
    highest_damage = float("-inf")
    result = None
    for attack in attacker["attacks"]:
        if attack_meter["magic"] == 0 and attack["magic"] > 5:
            continue

        total_attack_value = 0
        for attack_value, defense_value in zip(meters_to_tuple(attack), defenses):
            total_attack_value += max(0, attack_value - defense_value)
        if total_attack_value > highest_damage:
            result = attack

    return result


def damageSoak(defense_profile: list) -> tuple:
    """
    :return: total (mechanical, magic, health) scores
    """
    mech = 0
    magic = 0
    health = 0
    for defense in defense_profile:
        mech += defense["mechanical"]
        magic += defense["magic"]
        health += defense["health"]
    return (mech, magic, health)


def plotDamage(attacker: dict, defender: dict) -> list:
    """
    Goes through potential attacks and their damage to the enemy depending on their defense profile
    :retuen: A list of attacks that show actual damage
    """
    defense_values = damageSoak(defender["defenses"])
    real_attacks = []  # How much damage each attack will really do
    attack_meter = attacker["meters"]

    for attack in attacker["attacks"]:
        if (
            (attack_meter["mechanical"] == 0 or attack_meter["health"] == 0)
            or attack_meter["magic"] == 0
            and attack["magic"] > 5
        ):
            real_damages = create_meters(0, 0, 0)
        else:
            attack_values = meters_to_tuple(attack)
            after_defense_values = [
                max(0, attack_values[i] - defense_values[i])
                for i in range(len(attack_values))
            ]
            real_damages = create_meters(*after_defense_values)

        real_attack = {"name": attack["name"]}
        real_attack.update(real_damages)
        real_attacks.append(real_attack)

    return real_attacks


def create_meters(mechanical: int, magic: int, health: int) -> dict:
    return {"mechanical": mechanical, "magic": magic, "health": health}


def meters_to_tuple(meters: dict) -> tuple:
    """
    :return: (mech, magic, health)
    """
    return (meters["mechanical"], meters["magic"], meters["health"])


def create_item(name: str, meters: dict) -> dict:
    result = {"name": name}
    result.update(meters)
    return result


def create_player(meters: dict, attacks: list, defenses: list) -> dict:
    return {"meters": meters, "attacks": attacks, "defenses": defenses}


attacks = [
    create_item("arrows", create_meters(22, 5, 45)),
    create_item("sparrow attack", create_meters(45, 15, 25)),
]
defenses = [
    create_item("shield", create_meters(5, 2, 3)),
    create_item("bubble spell", create_meters(3, 3, 3)),
]

player_meters = create_meters(50, 50, 50)
player1 = create_player(player_meters, attacks, defenses)
player2 = create_player(player_meters, attacks, defenses)

print(plotDamage(player1, player2))
print(highestAttack(player1, player2))

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
