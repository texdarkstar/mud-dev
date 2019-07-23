from commands.command import Command
from evennia import create_script


class CmdCurse(Command):
    key = "curse"
    locks = "cmd:perm(Developers)"

    def func(self):
        args = self.args.strip().lower()

        if not args:
            self.caller.msg("Curse who?")
            return

        
        target = self.caller.search(args)
        if target and not target.db.cursed:
            script = create_script("world.curse_script.AnimalCurse", obj=target, persistent=True, report_to=target)
            script.start()
