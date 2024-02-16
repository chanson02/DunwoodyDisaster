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


# print(plotDamage(player1, player2))


def create_meters(mechanical: int, magic: int, health: int) -> dict:
    return {
            'mechanical': mechanical,
            'magic': magic,
            'health': health
            }


def meters_to_tuple(meters: dict) -> tuple:
    """
    :return: (mech, magic, health)
    """
    return (meters['mechanical'], meters['magic'], meters['health'])


def create_item(name: str, meters: dict) -> dict:
    result = {'name': name}
    result.update(meters)
    return result


def create_player(meters: dict, attacks: list, defenses: list) -> dict:
    return {
            'meters': meters,
            'attacks': attacks,
            'defenses': defenses
            }


attacks = [
        create_item('arrows', create_meters(22, 5, 45)),
        create_item('sparrow attack', create_meters(45, 15, 25))
        ]
defenses = [
        create_item('shield', create_meters(5, 2, 3)),
        create_item('bubble spell', create_meters(3, 3, 3))
        ]

player_meters = create_meters(50, 50, 50)
player1 = create_player(
        player_meters,
        attacks,
        defenses
        )
player2 = create_player(
        player_meters,
        attacks,
        defenses
        )


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
