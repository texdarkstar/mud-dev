import random
from typeclasses.characters import Character
from evennia import TICKER_HANDLER as tickerhandler
from evennia import search_object


class Mob(Character):
    def at_object_creation(self):
        super(Mob, self).at_object_creation()
        self.db.patrol_state = False
        self.db.idle_state = False
        self.db.attack_state = False
        self.db.hostile = False

        self.db.patrol_pace = 6

        pace = self.db.cooldown

        for item in self.db.equip_wield.values():
            if item and item.db.cooldown < pace:
                pace = item.db.cooldown

        self.db.attack_pace = pace

        self.db.last_ticker_interval = None
        self.db.last_hook_key = None


    def start_idle(self):
        """
        Starts just standing around. This will kill
        the ticker and do nothing more.
        """
        self.set_state(None, None, stop=True)


    def start_patrol(self):
        if not self.db.patrol_state:
            self.start_idle()
            return

        self.set_state(self.db.patrol_pace, "patrol_state")
        self.db.patrol_state = True
        self.db.attack_state = False
        self.db.idle_state = False

    def start_attack(self):
        self.set_state(self.db.attack_pace, "attack_state")
        self.db.patrol_state = False
        self.db.attack_state = True
        self.db.idle_state = False

    def set_state(self, interval, hook_key, stop=False):
        idstring = self.key + "-" + str(self.id)
        last_interval = self.db.last_ticker_interval
        last_hook_key = self.db.last_hook_key

        if last_interval and last_hook_key:
             # we have a previous subscription, kill this first.
            tickerhandler.remove(interval=last_interval,
                                  callback=getattr(self, last_hook_key), idstring=idstring)

        self.db.last_ticker_interval = interval
        self.db.last_hook_key = hook_key

        if not stop:
            # set the new ticker
            tickerhandler.add(interval=interval,
                               callback=getattr(self, hook_key), idstring=idstring)

    def find_target(self, location):
        targets = [obj for obj in location.contents_get(exclude=self)
                    if obj.tags.get("creature") and not obj.is_superuser]

        return random.choice(targets)


    def attack_state(self, *args, **kwargs):
        # self.execute_cmd("say Die %s!" % self.db.target.get_display_name(self))
        if self.db.target.db.hp >= 0:
            self.execute_cmd("attack right")
            self.execute_cmd("attack left")
        else:
            self.start_patrol()

    def patrol_state(self, *args, **kwargs):
        if self.db.hostile:
            target = self.find_target(self.location)
            if target:
                self.db.target = target.id
                self.start_attack()
                return
            
        exits = [exi for exi in self.location.exits
                    if exi.access(self, "traverse")]
        if exits:
            exi = random.choice(exits)
            self.move_to(exi.destination)
        else:
            self.move_to(self.home)