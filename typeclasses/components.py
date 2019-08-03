from typeclasses.objects import Object

class Craftable(Object):
    def at_object_creation(self):
        pass
    def at_craft_use(self, caller, obj):
        pass


class LeatherStrip(Craftable):
    def at_object_creation(self):
        super(LeatherStrip, self).at_object_creation()
        self.tags.add("leather strip", category="craftable")


class SteelHilt(Craftable):
    def at_object_creation(self):
        super(SteelHilt, self).at_object_creation()
        self.tags.add("steel hilt", category="craftable")


class SmallSteelBlade(Craftable):
    def at_object_creation(self):
        super(SmallSteelBlade, self).at_object_creation()
        self.tags.add("small steel blade", category="craftable")


class LargeSteelBlade(Craftable):
    def at_object_creation(self):
        super(LargeSteelBlade, self).at_object_creation()
        self.tags.add("large steel blade", category="craftable")

