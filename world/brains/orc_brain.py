from typeclasses.scripts import Script


class OrcBrain(Script):
    def at_script_creation(self):
        self.interval = 1

    def at_repeat(self):
        if self.obj.db.hostile:
            pass
