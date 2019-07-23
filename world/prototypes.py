"""
Prototypes

A prototype is a simple way to create individualized instances of a
given `Typeclass`. For example, you might have a Sword typeclass that
implements everything a Sword would need to do. The only difference
between different individual Swords would be their key, description
and some Attributes. The Prototype system allows to create a range of
such Swords with only minor variations. Prototypes can also inherit
and combine together to form entire hierarchies (such as giving all
Sabres and all Broadswords some common properties). Note that bigger
variations, such as custom commands or functionality belong in a
hierarchy of typeclasses instead.

Example prototypes are read by the `@spawn` command but is also easily
available to use from code via `evennia.spawn` or `evennia.utils.spawner`.
Each prototype should be a dictionary. Use the same name as the
variable to refer to other prototypes.

Possible keywords are:
    prototype - string pointing to parent prototype of this structure.
    key - string, the main object identifier.
    typeclass - string, if not set, will use `settings.BASE_OBJECT_TYPECLASS`.
    location - this should be a valid object or #dbref.
    home - valid object or #dbref.
    destination - only valid for exits (object or dbref).

    permissions - string or list of permission strings.
    locks - a lock-string.
    aliases - string or list of strings.

    ndb_<name> - value of a nattribute (the "ndb_" part is ignored).
    any other keywords are interpreted as Attributes and their values.

See the `@spawn` command and `evennia.utils.spawner` for more info.

"""
ARMOR = {
    "key": "<armor>",
    "armor": 0,
    "typeclass": "typeclasses.wornobject.Armor",
    "desc": "You see nothing special.",
    }
    
STEEL_HELM = {
    "prototype_parent": "ARMOR",
    "key": "steel helm",
    "slot": "head",
    'armor': 300,
    'wear_message': "You pull your %s over your head and buckle it up.",
    'remove_message': "You unbuckle your %s and pull it off your head."
    }
    
STEEL_GAUNTLETS = {
    "prototype_parent": "ARMOR",
    "key": "steel gauntlets",
    "slot": "hands",
    "armor": 300,
}

STEEL_LEGGINGS = {
    "prototype_parent": "ARMOR",
    "key": "steel leggings",
    "slot": "legs",
    "armor": 300,
}

STEEL_PLATE = {
    "prototype_parent": "ARMOR",
    "key": "steel plate",
    "slot": "body",
    "armor": 300,
}

MELEE = {
    "key": "<melee>",
    "typeclass": "typeclasses.wornobject.Weapon",
    "damage": "1d1",
    "mod": 0,
    "cooldown": 3,
    "desc": "You see nothing special.",
}

LONGSWORD = {
    "prototype_parent": "MELEE",
    "key": "longsword",
    "damage": "1d6",
}

DAGGER = {
    "prototype_parent": "MELEE",
    "key": "dagger",
    "cooldown": 2,
    "damage": "1d4",
}

#from random import randint
#
# GOBLIN = {
# "key": "goblin grunt",
# "health": lambda: randint(20,30),
# "resists": ["cold", "poison"],
# "attacks": ["fists"],
# "weaknesses": ["fire", "light"]
# }
#
# GOBLIN_WIZARD = {
# "prototype": "GOBLIN",
# "key": "goblin wizard",
# "spells": ["fire ball", "lighting bolt"]
# }
#
# GOBLIN_ARCHER = {
# "prototype": "GOBLIN",
# "key": "goblin archer",
# "attacks": ["short bow"]
#}
#
# This is an example of a prototype without a prototype
# (nor key) of its own, so it should normally only be
# used as a mix-in, as in the example of the goblin
# archwizard below.
# ARCHWIZARD_MIXIN = {
# "attacks": ["archwizard staff"],
# "spells": ["greater fire ball", "greater lighting"]
#}
#
# GOBLIN_ARCHWIZARD = {
# "key": "goblin archwizard",
# "prototype" : ("GOBLIN_WIZARD", "ARCHWIZARD_MIXIN")
#}
