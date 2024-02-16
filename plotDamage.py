from typing import Optional

def highestAttack(
    attack_profile: list, defense_profile: list, meters: list
) -> Optional[list]:
    """
    Find the strongest attack for this turn to use on a defense profile

    This took me around 20 minutes, I didn't get the timing exact
    because I accidently started doing the wrong problem.

    :param meters: [mechanical, magic, health]
        values of the attackers meters
    """
    # if mechanical or health are zero, you cannot attack
    if meters[0] <= 0 or meters[2] <= 0:
        return None

    defenses = damageSoak(defense_profile)

    highest_damage = float("-inf")
    result = None

    for attack in attack_profile:
        # cannot use magic attack if magic is zero
        if meters[1] == 0 and attack[2] > 5:
            continue

        damage = (
            attack[1]
            - defenses[0]
            + attack[2]
            - defenses[1]
            + attack[3]
            - defenses[2]
        )
        if damage > highest_damage:
            highest_damage = damage
            result = attack

    return result


def damageSoak(defense_profile: list) -> tuple:
    """
    :return: (mechanical, magic, health) scores
    """
    mech = 0
    magic = 0
    health = 0
    for defense in defense_profile:
        mech += defense[1]
        magic += defense[2]
        health += defense[3]
    return (mech, magic, health)


def plotDamage(attacker: list, defender: list) -> list:
    """
    Goes through potential attacks and their damage to the enemy depending on his defense profile
    :return: A list of attacks that show actual damage
    """
    defenses = damageSoak(defender[2])
    real_attacks = []  # How much damage each attack will really do

    for attack in attacker[1]:  # attack in attack profile
        if (
            (attacker[0][0] == 0 or attacker[0][2] == 0)
            or attack[2] > 5
            and attacker[0][1] == 0
        ):
            real_damages = [0, 0, 0]
        else:
            real_damages = [max(0, attack[i + 1] - defenses[i])
                            for i in range(3)]
        real_attacks.append([attack[0]] + real_damages)

    return real_attacks


attack1 = ["arrows", 22, 5, 45]
attack2 = ["sparrow attack", 45, 15, 25]
defense1 = ["shield", 5, 2, 3]
defense2 = ["bubble spell", 3, 3, 3]

attack_profile = [attack1, attack2]
defense_profile = [defense1, defense2]
meters = [50, 50, 50]

player1 = [meters, attack_profile, defense_profile]
player2 = [meters, attack_profile, defense_profile]
print(plotDamage(player1, player2))

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
