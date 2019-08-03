from commands.command import Command
from world.dice import *
from world.hitlocations import *
from evennia.utils import delay


class CmdAttack(Command):
    """
        attack <left/right>
        example:
            attack right
    """

    key = "attack"
    aliases = ['atk', 'at']
    
    def parse(self):
        args = self.args.strip().lower()
        self.hand = args


    def func(self):            
        if not self.caller.db.target:
            self.caller.msg("You have no target!")
            return

        if self.hand not in ["right", "left"]:
            self.caller.msg("Attack with which hand?")
            return


        target = self.caller.search("#%i" % self.caller.db.target, use_dbref=True, quiet=True).pop()

        weapon = None

        try:
            weapon = self.caller.db.equip_wield[self.hand]
        except KeyError:
            pass

        if weapon:
            weapon.attack(self.hand, self.caller, target)

        else:
            # self.caller.msg("You're unarmed!")

            self.caller.attack(self.hand, self.caller, target)
