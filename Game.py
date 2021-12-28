import pyautogui 
import time
import operator

from Units import *

class Game:
    # ==== SETUP AND INITIALIZERS ====
    def __init__(self, configDragons, venueIndex, battleLogicModule, fastMode = True, elimThreshold = 1):

        self.state = self.getStateFromScreen()
        self.configDragons = configDragons
        self.venueIndex = venueIndex
        self.battleLogicModule = battleLogicModule

        self.buttonLocsDict = buttonLocsDict = {
            "canvasLoc": None,
            "monsterBattleButtonLoc": None,
            "fightOnButtonLoc": None,
            "venueNextPageLoc": None, 
            "venueLoc": None,
            "captchaLoc": None,
            "upperRightQuad": None, #quadrant used to find foe MP bars
        }

        if fastMode:
            self.buttonLocsDict = self.extrapolateButtonLocs()
            print("Warning: fast mode enabled!")
            print(self.buttonLocsDict)
        else:
            self.buttonLocsDict["monsterBattleButtonLoc"] = pyautogui.locateOnScreen("monsterBattle.png")

        self.venueNames = [
            # Page 1
            "trainingFields","woodlandPath","scorchedForest","sandsweptDelta",
            "bloomingGrove","forgottenCave","bambooFalls","thunderheadSavanna",
            "redrockCove","waterway","arena","volcanicVents",
            "rainsongJungle","borealWood","crystalPools", None, 
            # Page 2
            None, "harpysRoost", "ghostlightRuins", "mire", 
            "kelpBeds", "golemWorkshop", "forbiddenPortal"
        ]

        self.dragonList = []
        self.foeList = []
        self.elimThreshold = elimThreshold
    
    def getStateFromScreen(self):
        """
        Looks at the screen to get one of two battle states. Wow!
        """
        print("Getting state from screen")

        if pyautogui.locateOnScreen("./fightOn.PNG"):
            return "normal"
        elif pyautogui.locateOnScreen("./monsterBattle.PNG"):
            return "mainMenu"
        else:
            print("Couldn't determine battle state")
    
    def extrapolateButtonLocs(self):
        """Based on the location of the "Monster Battle" button, extrapolate the location of
        other important buttons. 

        Parameters:
        venueIndex: index of the coliseum venue
        default 0 (for Training Fields)

        Returns:
        A dictionary of button/feature locations (buttons, hp bars, etc)
        """

        buttonLocsDict = {}
        canvasLoc = (0,0,0,0)

        #From the focus, obtain the coliseum canvas/region of interest
        if self.state == "mainMenu":
            focus = pyautogui.locateOnScreen("./monsterBattle.PNG", minSearchTime = 20)
            buttonLocsDict["monsterBattleButtonLoc"] = focus
            canvasLoc = (focus[0]-100, focus[1]-375, 800, 600)
        elif self.state == "normal":
            focus = pyautogui.locateOnScreen("./fightOn.PNG", minSearchTime = 20)
            buttonLocsDict["fightOnButtonLoc"] = focus
            canvasLoc = (focus[0]-555, focus[1]-490, 800, 600)
        else:
            print("Couldn't run extrapolateButtonLocs because the game state was", self.state)

        buttonLocsDict["canvasLoc"] = canvasLoc

        #Find location of the particular venue
        venueMenuLoc = (canvasLoc[0]+20, canvasLoc[1]+95, 700, 450) 
        venueIndex = self.venueIndex%16 #Handling if it falls to the next page
        venueRow = int(venueIndex/4)
        venueColumn = venueIndex%4
        buttonLocsDict["venueLoc"] = (venueMenuLoc[0] + 700*(venueColumn/4) - 50, 
                                    venueMenuLoc[1] + 450*(venueRow/4) - 50,
                                    250,
                                    200)

        #Set other loc-regions
        buttonLocsDict["venueNextPageLoc"] = (canvasLoc[0]+540, canvasLoc[1]+425, 175, 120)
        buttonLocsDict["captchaLoc"] = (canvasLoc[0]+250, canvasLoc[1]-20, 250, 100)
        buttonLocsDict["upperRightQuad"] = (canvasLoc[0]+400, canvasLoc[1], 400, 300)
        if self.state == "mainMenu":
            buttonLocsDict["fightOnButtonLoc"] = (canvasLoc[0]+520, canvasLoc[1]+450, 175, 110)
        elif self.state == "normal":
            buttonLocsDict["monsterBattleButtonLoc"] = (canvasLoc[0]+100, canvasLoc[0]+375, 200, 200)

        return buttonLocsDict

    # ==== MENU LOOP ====
    # These functions are about navigating the menu between battles. 
        
    def loadBattle(self):
        """Loads the next battle depending on how the previous battle ended.

        Parameters:
        string state: Indicates how the previous battle was ended, and the current screen state.
            -mainMenu: (Default) Coli main menu screen. Click monsterBattle button, then click a venue.
            -normal: Clicks the fightOn button.
        int venueIndex: determines the venue to load from. Defaults to 0 (Training Fields). 
        Only used if we're on the main menu.
        dict buttonLocsDict: holds coordinates for all buttons to press.
        
        Returns: True if successful, false otherwise
        """
        
        if self.state == "mainMenu":
            #From main menu click Monster battle button
            #Monster Battle button glows when moused over. 
            if not self.buttonLocsDict["monsterBattleButtonLoc"]:
                self.buttonLocsDict["monsterBattleButtonLoc"] = pyautogui.locateOnScreen("./monsterBattle.PNG")
            buttonLoc = self.buttonLocsDict["monsterBattleButtonLoc"]
            buttonCenterX, buttonCenterY = pyautogui.center(buttonLoc)
            pyautogui.click(buttonCenterX, buttonCenterY)
            time.sleep(3)

            #Click the appropriate venue
            venueName = self.venueNames[self.venueIndex]
            print("Selected venue %s, index number %s"%(venueName,self.venueIndex))

            if self.venueIndex > 14: #it's not on current page, go to next page
                print("On venue select, skipping to next page")
                nextButtonLoc = self.buttonLocsDict["venueNextPageLoc"] or pyautogui.locateOnScreen("./venueNext.png")
                nextCenterX, nextCenterY = pyautogui.center(nextButtonLoc)
                pyautogui.click(nextCenterX, nextCenterY)

            venueLoc = self.buttonLocsDict["venueLoc"] or pyautogui.locateOnScreen("venues/"+venueName+".png")
            venueCenterX, venueCenterY = pyautogui.center(venueLoc)
            pyautogui.click(venueCenterX, venueCenterY)

            self.state = "normal"
            return True

        elif self.state == "normal":
            #both victory and defeat have a fightOn button which we locate on,
            #conveniently in the same location
            if not self.buttonLocsDict["fightOnButtonLoc"]:
                self.buttonLocsDict["fightOnButtonLoc"] = pyautogui.locateOnScreen("./fightOn.PNG")
            buttonLoc = self.buttonLocsDict["fightOnButtonLoc"]
            buttonCenterX, buttonCenterY = pyautogui.center(buttonLoc)
            pyautogui.click(buttonCenterX, buttonCenterY)
            return True

        else:
            print("Could not load battle due to weird state", self.state)
            return False

    
    def checkCaptcha(self):
        """
        Check for captcha.
        Returns: bool
        """
        return bool(pyautogui.locateOnScreen("./camping.png") or pyautogui.locateOnScreen("./campingZoomed.png"))

    def __isBattleOver(buttonLocsDict):
        """
        During battleturns, check if the battle is over, and has ended in Victory or Defeat.
        Both Victory and Defeat have a Fight On button, so they're lumped in together.
        """
        return bool(pyautogui.locateOnScreen("./fightOn.PNG"))

    # ==== INSIDE A BATTLE - INITIAL SETUP ====
    
    def setupBattle(self, shouldCreateDragons = False):
        if shouldCreateDragons:
            self.dragonList = self.__createDragons()
        
        if self.battleLogicModule.careAboutFoeList():
            self.foeList = self.__createFoes()


    def __createDragons(self):
        """At battlestart, locate Dragons based on the READY / not ready icons.

        Parameters:
        -list-of-lists configDragons: required parameter which describes dragon
        configs (Roles such as grinder/trainee and eliminate hotkey)
        Creates dragons based on specified configs.
        -dict buttonLocsDict
        
        Returns: a list of Dragon objects
        """
        dragonList = []
        dragonHPLocs = []

        loc = pyautogui.locateOnScreen("./ready.png")
        if loc:
            dragonHPLocs.append((loc[0]-220, loc[1], 203, 17))

        for loc in pyautogui.locateAllOnScreen("./notReady.png"):
            dragonHPLocs.append((loc[0]-220, loc[1], 203, 17))

        #Sort dragonHPLocs by height, and assign index from top to bottom
        dragonHPLocs.sort(key=operator.itemgetter(1))
        #https://stackoverflow.com/a/8459243
        
        for i in range(len(dragonHPLocs)):
            loc = dragonHPLocs[i]
            hpLoc = loc
            mpLoc = (loc[0], loc[1]+loc[3], loc[2], loc[3]/2)
            #Dragon MP bars are just below their HP bars,
            #and are about half as wide
    
            dragonList.append(Dragon(hpLoc = hpLoc,
                                    mpLoc = mpLoc,
                                    role = self.configDragons[i]['role'],
                                    elimKey = self.configDragons[i]['eliminate']))
        return dragonList
    
    def __createFoes(self):
        #print("DEBUG: inputThresh == " + str(inputThresh))
        
        """At battlestart, locate Foes based on MP bars,
        and create Foe objects.

        Parameters: 
        dict buttonLocsDict: (see loadBattle)
        int/float inputThresh: (optional) use a custom foe HP threshhold
        instead of the default in Units.py
        
        Returns: a list of Foe objects
        """
        foeList = []
        foeMPLocs = []
        for loc in pyautogui.locateAllOnScreen("foeMP.png",
            region = self.buttonLocsDict["upperRightQuad"]):
            foeMPLocs.append(loc) #A set of coords describing enemy MP bar position

        #Determine which foe has which keybind
        possibleKeybinds = [
            ["q"],              #if just one foe at battlestart
            ["q", "w"],         #if two foes
            ["q", "w", "e"],    #if three foes
            ["r", "q", "e", "w"]#if four
        ]

        keybind = possibleKeybinds[len(foeMPLocs)-1]
        #the actual keybind used in this battle

        #Sort foeMPLocs by height, and assign hotkeys from top to bottom
        foeMPLocs.sort(key=operator.itemgetter(1))
        #https://stackoverflow.com/a/8459243
        
        for i in range(len(foeMPLocs)):
            loc = foeMPLocs[i] 
            mpLoc = loc
            hpLoc = (loc[0], loc[1]-loc[3]-3, loc[2], loc[3]+2)
            #Foe HP bars are a little above the MP bars (by 1 pixel)
            #and also a little wider
            if self.elimThreshold == None:
                foeList.append(Foe(hpLoc = hpLoc, mpLoc = mpLoc,
                                posKey = keybind[i]))
            else:
                foeList.append(Foe(hpLoc = hpLoc, mpLoc = mpLoc,
                                posKey = keybind[i],
                                threshhold = self.elimThreshold)) 
        return foeList

    # ==== INSIDE A BATTLE - LOOPING FOREVER AND UNIT/FOE STATUS CHECKS ====
    def battleLoop(self, battleNumber):
        '''
        While inside a single battle, loop this procedure endlessly.
        -Check if battle ended; if so, break the loop
        -If battle isn't over, check if dragons ready
            -If dragons ready, ask battleLogicModule what to do, then continue the loop
            -If dragons are not ready, continue the loop

        Params:
        -battleNumber: Just indicates how many times we've battled so far.

        Returns: end state of battle
        '''

        while True:
            #Check if battle ended normally (victory or defeat)
            if self.__isBattleOver():
                print("Battle [" + str(battleNumber) + "] ended normally")
                return "normal"

            # Since the battle is not over, we should perform some actino
            readyDragon = self.__getReadyDragon()
            if not readyDragon:
                print("No dragons ready, waiting")
                time.sleep(0.25) #Allow foe animations to finish
                continue

            # Dragon ready --> check statuses of dragons and foes, then determine the action
            foeStatusList = self.__checkFoeStatuses() if self.battleLogicModule.careAboutFoeList() else []

            keyString = self.battleLogicModule.determineAction(readyDragon, self.dragonList, foeStatusList)
            print("keyString to be pressed", keyString)
            if keyString == ["f5"]:
                pyautogui.press(keyString) 
                return "mainMenu"
            else:
                pyautogui.typewrite(keyString, interval = 0.1)

            time.sleep(0.25) #Allow dragon's attack anim to finish
        
    def __getReadyDragon(self):
        """During battleturns, check which dragon is ready, if any.

        Parameters: A list of Dragons created at battlestart by createDragons()
        Returns: Dragon object or None
        If no dragon is ready, returns -1
        """
        #One could use image processing on the entire screen,
        #but limiting the search to the region next to the dragon HP bar
        #limits the search, and also is easier to assign "ready" to "dragon"
        #brittle--may change depend on screen reso

        d = None
        for i in range(len(self.dragonList)):
            d = self.dragonList[i]
            searchRegion = (d.hpLoc[0]-d.hpLoc[2], d.hpLoc[1]-30,
                            250, 70)
            # print("DEBUG: searchRegion == " + str(searchRegion))

            tempLoc = pyautogui.locateOnScreen("./ready.png", region=searchRegion)
            
            if bool(tempLoc) == True:
                return i
        return d

    def __checkFoeStatuses(self):
        """During battleturns, check which of the foes created at battlestart
        are not dead.

        Parameters:
        -a list of Foes created at battlestart by createFoes()

        Returns: list of various statuses ("Healthy", "Weak", etc)
        """
        foeStatuses = []
        for foe in self.foeList:
            if foe.isAlive() and foe.isHpLow():
                foeStatuses.append("Weak")
            elif foe.isAlive():
                foeStatuses.append("Healthy")
            else:
                foeStatuses.append("Dead")
        return foeStatuses
