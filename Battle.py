# Implements various battle logic modules.

class BattleLogic: #Abstract class don't use it etc
    def determineAction(self, readyDragon):
        '''
        Based on current battle conditions, returns a string that should be keypressed.
        '''
        pass

    def careAboutDragonReady(self):
        '''
        Do we care if a dragon has the Ready status or not.
        '''
        return False
    
    def careAboutFoeList(self):
        '''
        Do we care about the foe list.
        '''
        return False
    
    def checkIfDragonsWeak(self, dragonList):
        for d in self.dragonList:
            if d.isHpLow():
                return True
        return False

class SpamLogic(BattleLogic):

    def determineAction(self, readyDragon, dragonList = None, foeStatusList=None):
        if readyDragon and readyDragon.isElimReady():
            return "a..%s..qwer"%readyDragon.elimKey
        else:
            return "a..e..qwer"
    
    def careAboutDragonReady(self):
        return False

    def careAboutFoeList(self):
        return False

# TODO - fix this class. Something, SOMEWHERE, broke. Eugh.
class EliminateTrainerLogic(BattleLogic):

    def determineAction(self, readyDragon, dragonList, foeStatusList):
        if self.checkIfDragonsWeak():
            return ["f5"]

        try:
            weakFoeIndex = foeStatusList.index("Weak")
        except ValueError:
            weakFoeIndex = None
        try:
            aliveFoeIndex = foeStatusList.index("Healthy")
        except ValueError:
            aliveFoeIndex = 0
        print("debugging ElimTrainer logic", weakFoeIndex, aliveFoeIndex)

        #If elim is ready and a weak foe exists, eliminate that foe
        d = readyDragon
        if d.isElimReady() == True and weakFoeIndex:
            f = self.foeList[weakFoeIndex]
            print("Sending Eliminate to foe: " + f.posKey)
            keyString = "a" + d.elimKey + f.posKey

        #elif dragon is a trainee, defend
        elif d.role == "trainee":
            print("Sending defend action")
            keyString = "d"
            
        #default: scratch first active foe
        else: 
            f = self.foeList[aliveFoeIndex]
            print("Sending Scratch to foe: " + f.posKey)
            keyString = "a" + "e" + f.posKey
    
        return keyString
    
    def checkIfDragonsWeak(self, dragonList):
        grinderCount = len([d for d in dragonList if d.role != "trainee"])
        weakCount = 0
        
        for d in self.dragonList:
            if d.role == "grinder" and d.isHpLow():
                weakCount+=1

        return(weakCount >= grinderCount)

    def careAboutDragonReady(self):
        return True

    def careAboutFoeList(self):
        return True