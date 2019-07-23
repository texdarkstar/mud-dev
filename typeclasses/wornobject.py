from typeclasses.objects import Object
from world.dice import *
from world.hitlocations import *
from world.attack_roll import attack_roll
from evennia.utils import delay


class Armor(Object):
    def at_object_creation(self):
        self.db.slot = "body"
        self.db.armor = 0
        self.db.wear_message = "You don %s."
        self.db.remove_message = "You remove %s."

    def at_before_drop(self, dropper, **kwargs):
        if dropper.db.equip_worn[self.db.slot] == self.id:
            dropper.msg("You can't drop %s. You're wearing it!" % self.key)
            return False
        else:
            return True
        
    def on_wear(self, caller):
        caller.msg(self.db.wear_message % self.key)
        caller.db.armor[self.db.slot] += self.db.armor
        
    def on_remove(self, caller):
        caller.msg(self.db.remove_message % self.key)       
        caller.db.armor[self.db.slot] -= self.db.armor


class Weapon(Object):
    def at_object_creation(self):
        self.db.slot = "hands"
        self.db.damage = "1d1"
        self.db.mod = 0
        self.db.cooldown = 3
        self.db.equip_message = "You hold %s in your %s hand."
        self.db.remove_message = "You remove %s from your %s hand."
        self.db.hand = None

    def on_equip(self, caller, hand):
        caller.msg(self.db.equip_message % (self.key, hand))
        self.db.hand = hand.lower()
        
    def on_unequip(self, caller, hand):
        caller.msg(self.db.remove_message % (self.key, hand))
        self.db.hand = None

    def is_cooldown(self, caller):
        return caller.db.attacking[self.db.hand]

    def at_before_drop(self, dropper, **kwargs):
        if self.db.hand and dropper.db.equip_wield[self.db.hand].id == self.id:
            dropper.msg("You can't drop %s. You're wielding it!" % self.key)
            return False
        else:
            return True

    def attack(self, hand, caller, target):
        if caller.db.attacking[hand]:
            caller.msg("You're already attacking with your %s!" % self.key)
            return

        caller.msg("Ok - Attacking %s with %s." % (target.key, self.key))
        caller.db.attacking[hand] = True
        delay(self.db.cooldown, attack_roll, weapon=self, hand=hand, caller=caller, target=target)


    def _attack(self, hand, caller, target, *args, **kwargs):
        caller.db.attacking[hand] = False

        attack_rating = caller.db.attack
        dodge_rating = target.db.dodge

        attack_roll = roll_pool({"num": 1, "sides": 100, "mod": 0})
        dodge_roll = roll_pool({"num": 1, "sides": 100, "mod": 0})

        attack_chance = 100.0 * (attack_rating / (attack_rating + 300.0))
        dodge_chance = 100.0 * (dodge_rating / (dodge_rating + 300.0))

        location = roll_location(target.db.bodytype)


        damage_roll = roll_pool(parse_pool(self.db.damage))
        damage_dealt = int((1.0 - (
                    target.db.armor[location] / (target.db.armor[location] + 300.0)
                )
            ) * damage_roll)

        caller.msg("<COMBAT> (|g{attack_rating}|n vs |r{dodge_rating}|n) rolled |g{attack_roll}|n vs |r{dodge_roll}|n".format(**locals()))

        # self.caller.msg("attack chance {attack_chance}% dodge chance {dodge_chance}%".format(**locals()))

        if (attack_roll <= attack_chance) and ((attack_roll > dodge_roll) or (dodge_roll > dodge_chance)):
            if dodge_roll < dodge_chance: # dodged well but we rolled higher
                caller.msg("{target} failed to dodge out of the way!".format(**locals()))
                target.msg("You failed to dodge out of the way of {caller}'s attack!".format(**locals()))

            caller.msg("You hit {target} with {self}, dealing |c{damage_dealt}|n damage to their {location}!".format(
                **locals(),
                )
            )

            target.msg("{caller} hit you with {self}, dealing |r{damage_dealt}|n damage!".format(
                **locals(),
                )
            )

            if damage_dealt == 0 and damage_roll > 0:
                armor = target.db.equip_worn[location]

                caller.msg("Your blow fails to penetrate {target}'s {armor}!".format(**locals()))

            target.db.hp -= damage_dealt
            if target.db.hp <= 0:
                target.at_defeat(caller)
        else:
            if attack_roll > attack_chance: # flat miss
                caller.msg("You missed!")
                target.msg("{caller} missed you!".format(**locals()))

            elif attack_roll < dodge_roll: # he dodged
                caller.msg("{target} dodged out of the way!".format(**locals()))
                target.msg("You dodged out of the way of {caller}'s attack!".format(**locals()))


