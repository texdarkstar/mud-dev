from commands.command import Command
from typeclasses.wornobject import *


class CmdWear(Command):
    key = "wear"
    aliases = ['wield']

    def func(self):
        arg = self.args.strip().lower()
        if not arg:
            self.caller.msg("%s what?" % self.cmdstring.capitalize())
            return

        item = self.caller.search(arg, location=self.caller)
        other_item = None
        
        if item:
            if item.is_typeclass(Armor):
                # wearing armor
                try:
                    other_item = self.caller.db.equip_worn[item.db.slot]
                except KeyError:
                    self.caller.msg("You can't wear %s, it doesn't fit!" % item.key)
                    return

                if other_item and item.id == other_item.id:
                    # but we're already wearing it
                    self.caller.msg("You're already wearing %s!" % item.key)
                    return
                    
                elif other_item and item.id != other_item.id:
                    # slot is already full with a different item
                    self.caller.msg("You can't wear that, you're already wearing %s!" % other_item.key)
                    return
                    
                else:
                    # slot is free, we are good to go
                    self.caller.db.equip_worn[item.db.slot] = item
                    item.on_wear(self.caller)
                    return

            elif item.is_typeclass(Weapon):
                # wielding weapon
                try:
                    right_hand = self.caller.db.equip_wield["right"]
                    left_hand = self.caller.db.equip_wield["left"]
                except KeyError:
                    self.caller.msg("You can't hold %s!" % item.key)
                    return

                if right_hand and left_hand:
                    self.caller.msg("Your hands are full.")
                    return
                    
                if item.id in [right_hand.id if right_hand else None, left_hand.id if left_hand else None]:
                    self.caller.msg("You're already wielding %s!" % item)
                    return

                if not right_hand:
                    self.caller.db.equip_wield["right"] = item
                    item.on_equip(self.caller, "right")
                    
                elif not left_hand:
                    self.caller.db.equip_wield["left hand"] = item
                    item.on_equip(self.caller, "left")


class CmdRemove(Command):
    key = "remove"
    aliases = ['unwield', 'rem']

    def func(self):
        arg = self.args.strip().lower()
        if not arg:
            self.caller.msg("Remove what?")
            return

        item = self.caller.search(arg, location=self.caller)
        other_item = None
        
        if item:
            if item.is_typeclass(Armor):
            # removing armor
                other_item = self.caller.db.equip_worn[item.db.slot]

                if other_item and item.id == other_item.id:
                    self.caller.db.equip_worn[item.db.slot] = None
                    item.on_remove(self.caller)
                    return
                    
                elif other_item and item.id != other_item.id:
                    self.caller.msg("You aren't wearing %s!" % item.key)
                    return
    
            elif item.is_typeclass(Weapon):
                # removing weapon
                right_hand = self.caller.db.equip_wield["right"]
                left_hand = self.caller.db.equip_wield["left"]
                
         
                if right_hand and right_hand.id == item.id:
                    self.caller.db.equip_wield["right"] = None
                    item.on_unequip(self.caller, "right")
                    
                elif left_hand and left_hand.id == item.id:
                    self.caller.db.equip_wield["left"] = None
                    item.on_unequip(self.caller, "left")

                else:
                    self.caller.msg("You aren't wielding %s!" % item.key)
                    return

            else:
                self.caller.msg("You can't remove that!")