from typeclasses.objects import Object
from evennia import create_script


class Corpse(Object):
    def at_object_creation(self):
        # create_script("world.corpse_script.CorpseScript", key="%s's decay script" % self.key, persistent=True, autostart=True, obj=self)
        pass


