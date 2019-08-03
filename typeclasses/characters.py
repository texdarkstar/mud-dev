"""
Characters

Characters are (by default) Objects setup to be puppeted by Accounts.
They are what you "see" in game. The Character class in this module
is setup to be the "default" character type created by the default
creation commands.

"""
from evennia import DefaultCharacter, create_object
# from world.hitlocations import hitlocations
from typeclasses.corpse import Corpse
from typeclasses.rooms import Room
from evennia.utils import delay
from world.attack_roll import attack_roll


class Character(DefaultCharacter):
    """
    The Character defaults to reimplementing some of base Object's hook methods with the
    following functionality:

    at_basetype_setup - always assigns the DefaultCmdSet to this object type
                    (important!)sets locks so character cannot be picked up
                    and its commands only be called by itself, not anyone else.
                    (to change things, use at_object_creation() instead).
    at_after_move(source_location) - Launches the "look" command after every move.
    at_post_unpuppet(account) -  when Account disconnects from the Character, we
                    store the current location in the pre_logout_location Attribute and
                    move it to a None-location so the "unpuppeted" character
                    object does not need to stay on grid. Echoes "Account has disconnected"
                    to the room.
    at_pre_puppet - Just before Account re-connects, retrieves the character's
                    pre_logout_location Attribute and move it back on the grid.
    at_post_puppet - Echoes "AccountName has entered the game" to the room.

    """
    def at_say(self, message, msg_self=None, msg_location=None,
               receivers=None, msg_receivers=None, **kwargs):
        msg_type = 'say'
        if kwargs.get("whisper", False):
            # whisper mode
            msg_type = 'whisper'
            msg_self = '{self} whisper to {all_receivers}, "{speech}"' if msg_self is True else msg_self
            msg_receivers = '{object} whispers: "{speech}"'
            msg_receivers = msg_receivers or '{object} whispers: "{speech}"'
            msg_location = None
        else:
            msg_self = ('{self} %s, "{speech}"' % self.db.speech) if msg_self is True else msg_self
            msg_location = msg_location or '{object} %ss, "{speech}"' % self.db.speech 
            msg_receivers = msg_receivers or message

        custom_mapping = kwargs.get('mapping', {})
        receivers = make_iter(receivers) if receivers else None
        location = self.location

        if msg_self:
            self_mapping = {"self": "You",
                            "object": self.get_display_name(self),
                            "location": location.get_display_name(self) if location else None,
                            "receiver": None,
                            "all_receivers": ", ".join(
                                recv.get_display_name(self)
                                for recv in receivers) if receivers else None,
                            "speech": message}
            self_mapping.update(custom_mapping)
            self.msg(text=(msg_self.format(**self_mapping), {"type": msg_type}), from_obj=self)

        if receivers and msg_receivers:
            receiver_mapping = {"self": "You",
                                "object": None,
                                "location": None,
                                "receiver": None,
                                "all_receivers": None,
                                "speech": message}
            for receiver in make_iter(receivers):
                individual_mapping = {"object": self.get_display_name(receiver),
                                      "location": location.get_display_name(receiver),
                                      "receiver": receiver.get_display_name(receiver),
                                      "all_receivers": ", ".join(
                                            recv.get_display_name(recv)
                                            for recv in receivers) if receivers else None}
                receiver_mapping.update(individual_mapping)
                receiver_mapping.update(custom_mapping)
                receiver.msg(text=(msg_receivers.format(**receiver_mapping),
                             {"type": msg_type}), from_obj=self)

        if self.location and msg_location:
            location_mapping = {"self": "You",
                                "object": self,
                                "location": location,
                                "all_receivers": ", ".join(str(recv) for recv in receivers) if receivers else None,
                                "receiver": None,
                                "speech": message}
            location_mapping.update(custom_mapping)
            exclude = []
            if msg_self:
                exclude.append(self)
            if receivers:
                exclude.extend(receivers)
            self.location.msg_contents(text=(msg_location, {"type": msg_type}),
                                       from_obj=self,
                                       exclude=exclude,
                                       mapping=location_mapping)

    def at_post_unpuppet(self, account, session=None, **kwargs):
        if not self.sessions.count():
            # only remove this char from grid if no sessions control it anymore.
            if self.location:
                # def message(obj, from_obj):
                    # obj.msg("%s has left the game." % self.get_display_name(obj), from_obj=from_obj)
                # self.location.for_contents(message, exclude=[self], from_obj=self)
                self.db.prelogout_location = self.location
                self.location = None


    def at_post_puppet(self, **kwargs):
        self.msg((self.at_look(self.location), {'type':'look'}), options = None)

    def get_pronoun(self, typ):
        pass

    def at_object_creation(self):
        self.tags.add("creature")
        # self.tags.add("humanoid")
        if self.db.desc is None:
            self.db.desc = str()

        self.db.death_location = None

        self.db.race = "human"
        self.db.natural_armor = "skin"
        self.db.speech = "say"

        self.db.primaries = {
            'str': 10,
            'dex': 10,
            'con': 10,
            'int': 10,
            'wis': 10,
            'cha': 10,
            }

        self.db.attacking = {
            "right": False,
            "left": False,
            }

        self.db.attack = 300
        self.db.dodge = 300
        
        self.db.wounds = []

        self.db.craft_stack = []
        self.db.armor = {
            "head": 0,
            "body": 0,
            "legs": 0,
            "hands": 0,
            }

        self.db.hp_max = 20
        self.db.hp = self.db.hp_max


        self.db.mv_max = 10
        self.db.mv = self.db.mv_max

        self.db.carry_weight = self.db.primaries['str']

        self.db.level = 1
        self.db.xp = 0
        self.db.xp_tnl = 1000

        self.db.gender = "ambiguous"
        self.db.has_thumbs = True

        self.db.unarmed_damage = "1d3"
        self.db.unarmed_name = "fists"
        self.db.cooldown = 3


        self.db.equip_worn = {
            "head": None,
            "body": None,
            "legs": None,
            # "feet": "",
            "hands": None,
            "ring": None,
            }

        self.db.equip_wield = {
            "left": None,
            "right": None,
            }


    def return_appearance(self, looker, **kwargs):
        if not looker:
            return ""
            
        # get description, build string
        string = "|c%s|n\n" % self.get_display_name(looker)

        equip_desc = ""
        wield_desc = ""


        for slot in self.db.equip_worn.keys():
            item = self.db.equip_worn[slot]
            if item:
                if not equip_desc.startswith("\nThey are wearing:\n"):
                    equip_desc += "\nThey are wearing:\n"

                equip_desc += "    |C%s|n on their %s\n" % (item, slot)

        for slot in self.db.equip_wield.keys():
            item = self.db.equip_wield[slot]
            if item:
                if not wield_desc.startswith("\nThey are holding:\n"):
                    wield_desc += "\nThey are holding:\n"

                wield_desc += "    |C%s on their %s\n" % (item, slot)

            # body = self.db.equip_worn['body']
            # legs = self.db.equip_worn['legs']
            # hands = self.db.equip_worn['hands']
            # ring = self.db.equip_worn['ring']
            
            # right_hand = self.db.equip_wield["right"]
            # left_hand = self.db.equip_wield["left"]
        
        # equip_desc = self.db.equip_desc.format(
                # head=head or "nothing",
                # body=body or "nothing",
                # legs=legs or "nothing",
                # hands=hands or "nothing",
                # ring=ring or "nothing",
                # left=left_hand or "nothing",
                # right=right_hand or "nothing",
            # )

        string += self.db.desc
        if equip_desc:
            string += equip_desc
        if wield_desc:
            string += wield_desc

        return string


    def at_defeat(self, killer):
        self.location.msg_contents("{victim} falls to the ground, slain.".format(victim=self.key))
        create_object(key="%s's corpse" % self.key, typeclass=Corpse, location=self.location)
        obj = create_object(key="Hell", typeclass=Room)
        self.db.death_location = self.location
        self.location = obj
        self.execute_cmd("look")


    def at_kill(self, victim):
        pass

    def revive(self):
        if self.location.key == "Hell":
            hell = self.location
            self.location = self.db.death_location
            self.execute_cmd("look")
            hell.delete()

    def level_up(self):
        self.db.level += 1
        self.db.xp_tnl += (1000 * self.db.level)


    def at_before_move(self, destination, **kwargs):
        if self.db.mv <= 0:
            return False
        elif self.db.mv > 0:
            self.db.mv -= 1
            return True

    def at_after_move(self, source_location, **kwargs):
        super(Character, self).at_after_move(source_location, **kwargs)
        self.db.target = None


    def attack(self, hand, caller, target):
        if self.db.attacking[hand]:
            self.msg("You're already attacking with your %s!" % self.db.unarmed_name)
            return

        self.msg("Ok - Attacking %s with %s." % (target.key, self.db.unarmed_name))
        self.db.attacking[hand] = True
        delay(self.db.cooldown, attack_roll, weapon=None, hand=hand, caller=self, target=target)
