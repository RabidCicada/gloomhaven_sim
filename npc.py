'''
'''

from unit import Unit

class NPC(Unit):
    def __init__(self, name, decktype, id=0, difficulty=0, elite=False, spawn=False, boss=False):
        super().__init__(name, id)
        self.decktype   = decktype
        self.difficulty = difficulty
        self.elite      = elite
        self.spawn      = spawn
        self.buffs      = list()
        self.move       = 0
        self.attack     = 0
        self.range      = 0
        self.immunities = list()
        self.causes     = list()

    def takeDamage(self, amount, effList=[]):
        self.curr_hp = max(self.curr_hp - amount, 0)
        if self.curr_hp > 0:
            self.effects.extend(effList)

    def setMAR(self, move, attack, range):
        self.move   = int(move)
        self.attack = int(attack)
        self.range  = int(range)

    def setBuffs(self, buffList):
        self.buffs.extend(buffList)

    def setImmunities(self, immuneList):
        self.immunities.extend(immuneList)

    def setCauses(self, causeList):
        self.causes.extend(causeList)

    def canAttack(self):
        return self.attack > 0 and not hasEffect(self.effects, "Disarm") and not hasEffect(self.effects, "Stun")

    def canMove(self):
        return self.move > 0 and not hasEffect(self.effects, "Immobilize") and not hasEffect(self.effects, "Stun")

    def isMelee(self):
        return self.range == 0

    def isRanged(self):
        return self.range > 0

    def isDead(self):
        return self.curr_hp <= 0

    def isElite(self):
        return self.elite

    def isSpawn(self):
        return self.spawn

    def isBoss(self):
        return self.boss

    def isFlying(self):
        return "Flying" in self.buffs

    def shieldValue(self):
        for buff in self.buffs:
            if "Shield" == buff[:6]:
                return int(buff[7:])
        return 0

    def __repr__(self):
        ret  = super().__repr__()
        sType = "Normal"
        if self.isElite():
            sType = "Elite"
        ret += "Type: %s\t\tDifficulty: %d\n" % (sType, self.difficulty)
        ret += "Health: %d, Move: %d, Attack: %d, Range: %d\n" % (self.curr_hp, self.move, self.attack, self.range)
        if len(self.buffs) > 0:
            ret += "Buffs: %s\n" % (self.buffs)
        if len(self.immunities) > 0:
            ret += "Immunities: %s\n" % (self.immunities)
        if len(self.causes) > 0:
            ret += "Causes Effects: %s\n" % (self.causes)
        return ret

if __name__ == "__main__":
    import global_vars as gv
    gv.init()

    for monName in gv.monsterDataJson.keys():
        monster = gv.monsterDataJson[monName]

        #print(monster)

        isBoss = False
        if "Boss" in monster:
            isBoss = True
        un = NPC(monName, monster["DeckType"], monster["Id"], boss=isBoss)

        stats = monster["Stats"]

        template = stats[str(un.difficulty)]["Normal"]
        if un.isElite():
            template = stats[str(un.difficulty)]["Elite"]
        un.setHealth(template["Health"])
        un.setBuffs(template["Buffs"])
        un.setImmunities(template["Immunities"])
        un.setCauses(template["Effects"])
        un.setMAR(template["Movement"], template["Attack"], template["Range"])
        print(un)
