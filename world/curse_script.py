from typeclasses.scripts import Script
from typeclasses.characters import Character
from world.creatures.wolf import Wolf
from evennia import create_object
from evennia.server.sessionhandler import SESSIONS


class AnimalCurse(Script):
    def at_script_creation(self):
        self.interval = 60
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
                "You begin to grow a short tail, as your nose grows into a fanged muzzle.",
                "{name} grows a short tail, as {name}'s face grows into a fanged muzzle."
                ],
            4: [
                "Your hands begin to fuse into paws, losing your ability to manipulate objects!",
                ""
                ],
            5: [
                "Your hair grows into a shaggy coat of slick black fur, as your tail reaches its full length.",
                "{name} grows a shaggy coat of slick black fur, as {name}'s tail reaches its full length."
                ],
            6: [
                "You suddenly can't stand straight! You slip to all fours as it is much more comfortable.",
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

        if self.stage == 3:
            self.obj.db.speech = "growl"

        if self.stage == 4:
            self.obj.db.has_thumbs = False
            self.obj.db.no_thumbs_err = "You can't pick up anything with your paws!"

        if self.stage >= self.repeats:
            character = self.obj
            animal = create_object(
                typeclass=Wolf,
                key="wolf",
                locks="puppet:id(%i)" % self.obj.account.id,    
                location=self.obj.location)


            self.obj.account.puppet_object(SESSIONS.sessions_from_account(self.obj.account).pop(), animal)

            self.obj.db.true_form = character

            # self.obj.tags.remove("humanoid")
            # self.obj.tags.add("quadruped")
            # self.obj.db.bodytype = "quadruped"
