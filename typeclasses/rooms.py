"""
Room

Rooms are simple containers that has no location of their own.

"""

from evennia import DefaultRoom


class Room(DefaultRoom):
    """
    Rooms are like any Object, except their location is None
    (which is default). They also use basetype_setup() to
    add locks so they cannot be puppeted or picked up.
    (to change that, use at_object_creation instead)

    See examples/object.py for a list of
    properties and methods available on all Objects.
    """
    def at_object_leave(self, moved_obj, target_location, **kwargs):
        for obj in self.contents:
            if obj.db.target == moved_obj.id and obj.id != moved_obj.id:
                obj.msg("You can't see {target} anymore.".format(target=moved_obj.key))
                obj.db.target = None
