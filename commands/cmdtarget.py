from commands.command import Command


class CmdTarget(Command):
    key = "target"
    aliases = ['t']
    def parse(self):
        self.target = self.args.strip()


    def func(self):
        target = self.caller.search(self.target)
        if not target:
            return

        self.caller.msg("You target {target}.".format(target=target.key))
        self.caller.db.target = target.id

            
