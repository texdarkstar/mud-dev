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
    def at_post_puppet(self, **kwargs):
        self.msg((self.at_look(self.location), {'type':'look'}), options = None)


    def at_object_creation(self):
        self.tags.add("creature")
        self.tags.add("humanoid")
        if self.db.desc is None:
            self.db.desc = str()

        self.db.death_location = None

        self.db.bodytype = "humanoid"
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

        self.db.hp_max = 20
        self.db.hp = self.db.hp_max

        self.db.carry_weight = self.db.primaries['str']

        self.db.mv_max = 10
        self.db.mv = self.db.mv_max

        self.db.level = 1
        self.db.xp = 0
        self.db.xp_tnl = 1000
        self.db.gender = "ambiguous"

        self.db.unarmed_damage = "1d3"
        self.db.unarmed_name = "fists"

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
            
        self.db.armor = {
            "head": 0,
            "body": 0,
            "legs": 0,
            "hands": 0,
            }

        string = "\nThey are wearing:\n"
        string += "    |C{head}|n on their head\n"
        string += "    |C{body}|n on their body\n"
        string += "    |C{legs}|n on their legs\n"
        string += "    |C{hands}|n on their hands\n"
        string += "    |C{ring}|n on their finger\n"
        string += "They are holding:\n"
        string += "    |C{left}|n in their left hand\n"
        string += "    |C{right}|n in their right hand\n"
        self.db.equip_desc = string


    def return_appearance(self, looker, **kwargs):
        if not looker:
            return ""
            
        # get description, build string
        string = "|c%s|n\n" % self.get_display_name(looker)
        head = self.db.equip_worn['head']
        body = self.db.equip_worn['body']
        legs = self.db.equip_worn['legs']
        hands = self.db.equip_worn['hands']
        ring = self.db.equip_worn['ring']
        
        right_hand = self.db.equip_wield["right"]
        left_hand = self.db.equip_wield["left"]
        
        # head = body = legs = hands = ring = left_hand = right_hand = "nothing"
        
        # if head_id:
            # head = self.search("#%d" % head_id, location=self, use_dbref=True)
        # if body_id:
            # body = self.search("#%d" % body_id, location=self, use_dbref=True)
        # if legs_id:
            # legs = self.search("#%d" % legs_id, location=self, use_dbref=True)
        # if hands_id:
            # hands = self.search("#%d" % hands_id, location=self, use_dbref=True)
        # if ring_id:
            # ring = self.search("#%d" % ring_id, location=self, use_dbref=True)
            
        # if right_hand_id:
            # right_hand = self.search("#%d" % right_hand_id, location=self, use_dbref=True)
        # if left_hand_id:
            # left_hand = self.search("#%d" % left_hand_id, location=self, use_dbref=True)

        equip_desc = self.db.equip_desc.format(
                head=head or "nothing",
                body=body or "nothing",
                legs=legs or "nothing",
                hands=hands or "nothing",
                ring=ring or "nothing",
                left=left_hand or "nothing",
                right=right_hand or "nothing",
            )

        string += self.db.desc
        string += equip_desc

        return string


    def at_defeat(self, killer):
        self.location.msg_contents("{victim} falls to the ground, slain.".format(victim=self.key))
        create_object(key="%s's corpse" % self.key, typeclass=Corpse, location=self.location)
        obj = create_object(key="Hell", typeclass=Room)
        self.db.death_location = self.location
        self.location = obj
        self.execute_cmd("look")

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
            self.msg("You're already attacking with your %s!" % self.unarmed_name)
            return

        self.msg("Ok - Attacking %s with %s." % (target.key, self.unarmed_name))
        self.db.attacking[hand] = True
        delay(self.db.cooldown, attack_roll, weapon=None, hand=hand, caller=self, target=target)