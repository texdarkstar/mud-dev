from typeclasses.wornobject import Weapon

class SteelDagger(Weapon):
    def at_object_creation(self):
        super(SteelDagger, self).at_object_creation()
        self.db.damage = "1d4"
        self.db.mod = 0
        self.db.cooldown = 2