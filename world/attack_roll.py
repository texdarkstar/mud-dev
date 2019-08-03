from world.dice import *
from world.hitlocations import *
from evennia.utils import delay


def attack_roll(weapon, hand, caller, target):
    weapon_name = ""
    weapon_damage = ""

    if not weapon:
        weapon_name = caller.db.unarmed_name
        weapon_damage = caller.db.unarmed_damage
    else:
        weapon_name = weapon.key
        weapon_damage = weapon.db.damage

    caller.db.attacking[hand] = False

    attack_rating = caller.db.attack
    dodge_rating = target.db.dodge

    attack_roll = roll_pool({"num": 1, "sides": 100, "mod": 0})
    dodge_roll = roll_pool({"num": 1, "sides": 100, "mod": 0})

    attack_chance = 100.0 * (attack_rating / (attack_rating + 300.0))
    dodge_chance = 100.0 * (dodge_rating / (dodge_rating + 300.0))

    location = None

    damage_roll = roll_pool(parse_pool(weapon_damage))
    damage_dealt = 0

    if not target.db.is_inanimate:
        location = roll_location(target.db.race)

        damage_dealt = int((1.0 - (
                    target.db.armor[location] / (target.db.armor[location] + 300.0)
                )
            ) * damage_roll)

    else:
        damage_dealt = int((1.0 - (
                    target.db.toughness / (target.db.toughness + 300.0)
                )
            ) * damage_roll)

    caller.msg("<COMBAT> (|g{attack_rating}|n vs |r{dodge_rating}|n) rolled |g{attack_roll}|n vs |r{dodge_roll}|n".format(**locals()))

    # self.caller.msg("attack chance {attack_chance}% dodge chance {dodge_chance}%".format(**locals()))

    if (attack_roll <= attack_chance) and ((attack_roll > dodge_roll) or (dodge_roll > dodge_chance)):
        if dodge_roll < dodge_chance: # dodged well but we rolled higher
            caller.msg("{target} failed to dodge out of the way!".format(**locals()))
            target.msg("You failed to dodge out of the way of {caller}'s attack!".format(**locals()))

        if not target.db.is_inanimate:
            caller.msg("You hit {target} with {weapon_name}, dealing |c{damage_dealt}|n damage to their {location}!".format(
                **locals(),
                )
            )

            target.msg("{caller} hit you with {weapon_name}, dealing |r{damage_dealt}|n damage!".format(
                **locals(),
                )
            )
        elif target.db.is_inanimate:
            caller.msg("You hit {target} with {weapon_name}, dealing |c{damage_dealt}|n damage!".format(**locals()))

        if damage_dealt == 0 and damage_roll > 0:
            armor = ""
            if not target.db.is_inanimate:
                try:
                    armor = target.db.equip_worn[location]
                except KeyError:
                    armor = target.db.natural_armor

                caller.msg("Your blow fails to penetrate {target}'s {armor}!".format(**locals()))
                target.msg("{caller}'s blow failed to penetrate your {armor}!".format(**locals()))
            else:
                caller.msg("Your blow glances off {target}!".format(**locals()))

            return

        target.db.hp -= damage_dealt
        if target.db.hp <= 0:
            target.at_defeat(caller)
            caller.db.target = None
    else:
        if attack_roll > attack_chance: # flat miss
            caller.msg("You missed!")
            target.msg("{caller} missed you!".format(**locals()))

        elif attack_roll < dodge_roll: # he dodged
            caller.msg("{target} dodged out of the way!".format(**locals()))
            target.msg("You dodged out of the way of {caller}'s attack!".format(**locals()))