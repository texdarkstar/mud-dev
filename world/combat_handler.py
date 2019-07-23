import random
from typeclasses.scripts import Script


class CombatHandler(Script):
    """
    This implements the combat handler.
    """
    
    def at_script_creation(self):

        self.key = "combat handler_%s" % (
                "".join(str(random.randint(0, 9)) for i in range(8))
            )
        self.desc = "handles combat"
        self.interval = 5
        self.start_delay = True
        self.persistent = True
        
        
        self.db.characters = {}
        self.db.inititives = {}
        
        
    def roll_inititive(self):
        for character in self.db.characters.values():
            inititive = random.randint(1, 100) + character.db.primaries['dex']
            self.db.inititive[dbref] = inititive
            

    def _init_character(self, character):
        """
        This initializes handler back-reference
        and stuff.
        """
        dbref = character.id
        character.ndb.combat_handler = self

        
    def _cleanup_character(self, character):
        """
        Remove character from handler and clean
        it of the back-reference and stuff.
        """
        dbref = character.id

        del self.db.characters[dbref]
        del character.ndb.combat_handler
        del self.db.inititives[dbref]

    
    def at_start(self):
        """
        This is called on first start but also when the script is restarted
        after a server reboot. We need to re-assign this combat handler to 
        all characters as well as re-assign the cmdset.
        """
        for character in self.db.characters.values():
            self._init_character(character)
            

    def at_stop(self):
        "Called just before the script is stopped/destroyed."
        for character in list(self.db.characters.values()):
            # note: the list() call above disconnects list from database
            self._cleanup_character(character)

    def at_repeat(self):
        """
        This is called every self.interval seconds (turn timeout) or 
        when force_repeat is called (because everyone has entered their 
        commands). We know this by checking the existence of the
        `normal_turn_end` NAttribute, set just before calling 
        force_repeat.
        
        """
        if self.ndb.normal_turn_end:
            # we get here because the turn ended normally
            # (force_repeat was called) - no msg output
            del self.ndb.normal_turn_end
        else:        
            # turn timeout
            # self.msg_all("Turn timer timed out. Continuing.")
            pass
            
        self.roll_inititive()
        self.battle()
        self.end_turn()

    # Combat-handler methods

    def add_character(self, character):
        "Add combatant to handler"
        dbref = character.id
        self.db.characters[dbref] = character        
        self._init_character(character)
       
    def remove_character(self, character):
        "Remove combatant from handler"
        if character.id in self.db.characters:
            self._cleanup_character(character)
        if not self.db.characters:
            # if no more characters in battle, kill this handler
            self.stop()

    def msg_all(self, message):
        "Send message to all combatants"
        for character in self.db.characters.values():
            character.msg(message)

    def add_action(self, action, character, target):
        """
        Called by combat commands to register an action with the handler.

         action - string identifying the action, like "hit" or "parry"
         character - the character performing the action
         target - the target character or None

        actions are stored in a dictionary keyed to each character, each
        of which holds a list of max 2 actions. An action is stored as
        a tuple (character, action, target). 
        """
        dbref = character.id
        count = self.db.action_count[dbref]
        if 0 <= count <= 1: # only allow 2 actions            
            # self.db.turn_actions[dbref][count] = (action, character, target)
            pass
        else:        
            # report if we already used too many actions
            return False
        # self.db.action_count[dbref] += 1
        return True

    def check_end_turn(self):
        """
        Called by the command to eventually trigger 
        the resolution of the turn. We check if everyone
        has added all their actions; if so we call force the
        script to repeat immediately (which will call
        `self.at_repeat()` while resetting all timers). 
        """
        if all(count > 1 for count in self.db.action_count.values()):
            self.ndb.normal_turn_end = True
            self.force_repeat() 

    def end_turn(self):
        """
        This resolves all actions by calling the rules module. 
        It then resets everything and starts the next turn. It
        is called by at_repeat().
        """        
        # resolve_combat(self, self.db.turn_actions)

        if len(self.db.characters) < 2:
            # less than 2 characters in battle, kill this handler
            self.msg_all("Combat has ended")
            self.stop()
        else:
            # reset counters before next turn
            for character in self.db.characters.values():
                # self.db.characters[character.id] = character
                # self.db.action_count[character.id] = 0
                # self.db.turn_actions[character.id] = [("defend", character, None),
                                                  # ("defend", character, None)]
                pass
                
            self.msg_all("Next turn begins ...")
            
    def battle(self):
        for character in self.db.characters.values():
