from commands.command import Command


class CmdStats(Command):
    """View basic statistics about your character."""
    key = "stats"
    
    def func(self):
        strength = self.caller.db.primaries['str']
        dexterity = self.caller.db.primaries['dex']
        constitution = self.caller.db.primaries['con']
        intelligence = self.caller.db.primaries['int']
        wisdom = self.caller.db.primaries['wis']
        charisma = self.caller.db.primaries['cha']
        
        string = "level {level}({xp}/{xp_tnl} xp)\n"
        string += "carry weight: {carry_weight}\n"
        string += "{hp}/{hp_max} hp {mv}/{mv_max} mv\n"
        string += "str: {strength}, dex: {dexterity}, con: {constitution}, int: {intelligence}, wis: {wisdom}, cha: {charisma}\n"
    
        self.caller.msg(
            string.format(
                level=self.caller.db.level,
                xp=self.caller.db.xp,
                xp_tnl=self.caller.db.xp_tnl,
                
                carry_weight=self.caller.db.carry_weight,
                
                hp=self.caller.db.hp,
                hp_max=self.caller.db.hp_max,
                mv=self.caller.db.mv,
                mv_max=self.caller.db.mv_max,
                
                strength=strength,
                dexterity=dexterity,
                constitution=constitution,
                intelligence=intelligence,
                wisdom=wisdom,
                charisma=charisma
                )
            )