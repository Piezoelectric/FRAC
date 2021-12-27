import Menu
import pyautogui

# Implements various battle logic modules.

class BattleLogic:
    def __init__(self, dragonList, foeList):
        self.foeList = foeList
        self.dragonList = dragonList

    def determineAction(self, readyDragonIndex):
        '''
        Based on current battle conditions, returns a string that should be keypressed.
        '''
        pass

    def careAboutDragonReady(self):
        '''
        Do we care if a dragon has the Ready status or not.
        '''
        return False

class SpamLogic(BattleLogic):
    def __init__(self, dragonList, foeList):
        super().__init__(dragonList, foeList)

    def determineAction(self, readyDragonIndex):
        d = self.dragonList[readyDragonIndex]
        if d.isElimReady():
            return "a..%s..qwer"%d.elimKey
        else:
            return "a..e..qwer"
    
    def careAboutDragonReady(self):
        return False

# TODO - fix this class. Something, SOMEWHERE, broke. Eugh.
class BasicEliminateTrainerLogic(BattleLogic):

    def __init__(self, dragonList, foeList):
        super().__init__(dragonList, foeList)

    def determineAction(self, readyDragonIndex):
        foeStatuses = Menu.checkFoes(self.foeList)
        try:
            weakFoeIndex = foeStatuses.index("Weak")
        except ValueError:
            weakFoeIndex = None
        try:
            aliveFoeIndex = foeStatuses.index("Healthy")
        except ValueError:
            aliveFoeIndex = 0
        print("debug", weakFoeIndex, aliveFoeIndex)

        #If elim is ready and a weak foe exists, eliminate that foe
        d = self.dragonList[readyDragonIndex]
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
    
    def careAboutDragonReady(self):
        return True