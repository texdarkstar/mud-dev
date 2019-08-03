from evennia.commands.default.general import CmdGet, CmdInventory, CmdSay


class OverrideCmdGet(CmdGet):
    """
    pick up something

    Usage:
      get <obj>

    Picks up an object from your location and puts it in
    your inventory.
    """
    # key = "get"
    # aliases = "grab"
    # locks = "cmd:all()"
    # arg_regex = r"\s|$"

    def func(self):
        """implements the command."""

        caller = self.caller

        if not caller.db.has_thumbs:
            caller.msg(caller.db.no_thumbs_err or "You can't pick anything up, you don't have any opposable thumbs!")
            return

        if not self.args:
            caller.msg("Get what?")
            return
        obj = caller.search(self.args, location=caller.location)
        if not obj:
            return
        if caller == obj:
            caller.msg("You can't get yourself.")
            return
        if not obj.access(caller, 'get'):
            if obj.db.get_err_msg:
                caller.msg(obj.db.get_err_msg)
            else:
                caller.msg("You can't get that.")
            return

        # calling at_before_get hook method
        if not obj.at_before_get(caller):
            return

        obj.move_to(caller, quiet=True)
        caller.msg("You pick up %s." % obj.name)
        caller.location.msg_contents("%s picks up %s." %
                                     (caller.name,
                                      obj.name),
                                     exclude=caller)
        # calling at_get hook method
        obj.at_get(caller)

