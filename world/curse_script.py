from typeclasses.scripts import Script
from typeclasses.characters import Character
from evennia import create_object
from evennia.server.sessionhandler import SESSIONS


class AnimalCurse(Script):
    def at_script_creation(self):
        self.interval = 2
        self.messages = {
            1: [
                "You start feeling some fuzz on your limbs.",
                ""
                ],
            2: [
                "Your nose begins to elongate, and the hair on your body thickens.",
                "{name}'s face begins to elongate."
                ],
            3: [
                "Your thumbs begin to fuse together, losing your ability to manipulate objects.",
                ""
                ],
            4: [
                "You begin to grow a short tail, as your nose grows into a fanged muzzle.",
                "{name} grows a short tail, as {name}'s face grows into a fanged muzzle."
                ],
            5: [
                "Your hair grows into a shaggy coat of slick black fur, as your tail reaches its full length.",
                "{name} grows a shaggy coat of slick black fur, as {name}'s tail reaches its full length."
                ],
            6: [
                "You suddenly can't stand straight! You slip to your fours as it is much more comfortable.",
                "{name}'s yelps in pain! {name} slips to all fours."
                ],
            }

        self.repeats = len(self.messages)
        
        self.stage = 0


    def at_repeat(self):
        self.stage += 1
        
        self.obj.msg(self.messages[self.stage][0])
        if self.messages[self.stage][1]:
            self.obj.location.msg_contents(self.messages[self.stage][1].format(name=self.obj.key), exclude=self.obj)

        if self.stage >= self.repeats:
            # self.caller.msg("Grabbing character reference...")

            character = self.obj
            # self.caller.msg("Reference aquired. Spawning object...")

            animal = create_object(
                typeclass=Character,
                key="wolf",
                locks="puppet:id(%i)" % self.obj.id,    
                location=self.obj.location)

            # self.caller.msg("Object spawned. Initiating puppet...")

            self.obj.account.puppet_object(SESSIONS.sessions_from_account(self.obj.account).pop(), animal)
            # obj.account.db._last_puppet = animal
            self.obj.db.true_form = character

            self.obj.tags.remove("humanoid")
            self.obj.tags.add("quadruped")
            self.obj.db.bodytype = "quadruped"

            # self.stop()
        # else:
            # delay(self.interval, self.advance_stage, obj=obj)
