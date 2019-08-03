from typeclasses.components import Craftable


class Steel(Craftable):
    def at_object_creation(self):
        super(Steel, self).at_object_creation()
        self.tags.add("steel", category="craftable")

class Iron(Craftable):
    def at_object_creation(self):
        super(Iron, self).at_object_creation()
        self.tags.add("iron", category="craftable")

class Leather(Craftable):
    def at_object_creation(self):
        super(Leather, self).at_object_creation()
        self.tags.add("leather", category="craftable")
