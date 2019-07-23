from typeclasses.wornobject import Weapon


class Longsword(Weapon):
    key = "longsword"
    
    def at_object_creation(self):
        self.db.slot = "hands"
        self.db.damage = "1d6"
        self.db.mod = 0
    
    def on_equip(self, caller, hand):
        caller.msg("You hold %s in your %s hand." %(self.key, hand))
        
    def on_unequip(self, caller, hand):
        caller.msg("You remove %s from your %s hand." % (self.key, hand))