import random
from typeclasses.characters import Character


class Wolf(Character):
    def at_object_creation(self):
        super(Wolf, self).at_object_creation()
        self.db.race = "wolf"
        self.db.equip_worn = {}
        self.db.equip_wield = {}

        self.db.unarmed_damage = "1d6"
        self.db.unarmed_name = "claws"
        self.db.cooldown = 2
        self.db.natural_armor = "fur"
        self.db.has_thumbs = False
        self.db.speech = "growl"

        self.db.no_thumbs_err = "You can't pick up anything with your paws!"

        self.db.armor = {
            'head': 600,
            'body': 600,
            'paws': 600,
            'legs': 600,
            }

    def at_before_say(self, speech):
        text = ['Rrr.', 'Grr.', 'Woof!', 'Yip!', 'Aaaarooooo!']
        return random.choice(text)

