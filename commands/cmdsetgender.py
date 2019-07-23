from commands.command import Command


class CmdSetGender(Command):
    """
    Sets gender on yourself

    Usage:
      @gender male||female||neutral||ambiguous

    """
    key = "@gender"
    aliases = "@sex"
    locks = "call:all()"

    def func(self):
        """
        Implements the command.
        """
        caller = self.caller
        arg = self.args.strip().lower()
        if arg not in ("male", "female", "neutral", "ambiguous"):
            caller.msg("Usage: @gender male||female||neutral||ambiguous")
            return
        caller.db.gender = arg
        caller.msg("Your gender was set to %s." % arg)