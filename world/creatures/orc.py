from typeclasses.mobs import Mob
from evennia import create_script


class Orc(Mob):
    def at_init(self):
        script = create_script("world.brains.orc_brain.OrcBrain", key="orc_brain", obj=self, autostart=True)
