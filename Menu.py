import pyautogui 
import time
import operator

from Units import *

#==============================================================================#
#    FUNCTIONS

#These functions are helper functions for battles
#Operator is used to sort tuples (coords) by element
#==============================================================================#

#==============================================================================#
#    Extrapolate Coordinates
#This function DOES NOT interact with the server.
#Used to restrict search spaces (instead of searching the entire screen)
#==============================================================================#

def extrapolateButtonLocs(venueIndex = 0):
    """Based on the location of the "Monster Battle" button, extrapolate the location of
    other important buttons. 

    Parameters:
    venueIndex: index of the coliseum venue
    default 0 (for Training Fields)

    Returns:
    A dictionary of button/feature locations (buttons, hp bars, etc)
    """

    buttonLocsDict = {}

    #From the focus, obtain the coliseum canvas/region of interest
    buttonLocsDict["monsterBattleButtonLoc"] = pyautogui.locateOnScreen("monsterBattle.png", minSearchTime = 20)
    focus = buttonLocsDict["monsterBattleButtonLoc"]
    canvasLoc = (focus[0]-100, focus[1]-375, 800, 600)
    buttonLocsDict["canvasLoc"] = canvasLoc

    #Find location of the particular venue
    venueMenuLoc = (canvasLoc[0]+20, canvasLoc[1]+95, 700, 450) 
    venueIndex = venueIndex%16 #Handling if it falls to the next page
    venueRow = int(venueIndex/4)
    venueColumn = venueIndex%4
    buttonLocsDict["venueLoc"] = (venueMenuLoc[0] + 700*(venueColumn/4) - 50, 
                                  venueMenuLoc[1] + 450*(venueRow/4) - 50,
                                  250,
                                  200)

    #Set other loc-regions
    buttonLocsDict["fightOnButtonLoc"] = (canvasLoc[0]+520, canvasLoc[1]+450, 175, 110)
    buttonLocsDict["venueNextPageLoc"] = (canvasLoc[0]+540, canvasLoc[1]+425, 175, 120)
    buttonLocsDict["captchaLoc"] = (canvasLoc[0]+250, canvasLoc[1]-20, 250, 100)
    buttonLocsDict["lowerLeftQuad"] = (canvasLoc[0], canvasLoc[1]+300, 400, 300)
    buttonLocsDict["upperRightQuad"] = (canvasLoc[0]+400, canvasLoc[1], 400, 300)

    return buttonLocsDict

#==============================================================================#
#    LOAD BATTLE
#This function DOES interact with the server.
#Loads battle depending on how the previous battle ended.
#==============================================================================#

def loadBattle(state, venueIndex, buttonLocsDict):
    """Loads the next battle depending on how the previous battle ended.

    Parameters:
    string state: Indicates how the previous battle was ended, and the current screen state.
        -mainMenu: (Default) Coli main menu screen. Click monsterBattle button, then click a venue.
        -normal: Clicks the fightOn button.
        -lowHp: A dragon has low health. Refresh the page to get to main menu.
    int venueIndex: determines the venue to load from. Defaults to 0 (Training Fields). 
    Only used if we're on the main menu.
    dict buttonLocsDict: holds coordinates for all buttons to press.
    
    Returns: None
    """

    venueNames = [
        "trainingFields",
        "woodlandPath",
        "scorchedForest",
        "sandsweptDelta",
        "bloomingGrove",
        "forgottenCave",
        "bambooFalls",
        "thunderheadSavanna",
        "redrockCove",
        "waterway",
        "arena",
        "volcanicVents",
        "rainsongJungle",
        "borealWood",
        "crystalPools", #index 14, end of first page
        None, #This is the next page button
        None, #this is the previous page button
        "harpysRoost", 
        "ghostlightRuins",
        "mire",
        "golemWorkshop", #DO NOT EVER DO THE GOLEM WORKSHOP
        "kelpBeds"
        ]
    
    if state == "mainMenu":
        #From main menu click Monster battle button
        #Monster Battle button glows when moused over. 
        buttonLoc = buttonLocsDict["monsterBattleButtonLoc"] or pyautogui.locateOnScreen("monsterBattle.png")
        buttonCenterX, buttonCenterY = pyautogui.center(buttonLoc)
        pyautogui.click(buttonCenterX, buttonCenterY)
        time.sleep(3)

        #Click the appropriate venue
        venueName = venueNames[venueIndex]
        print("Selected venue %s, index number %s"%(venueName,venueIndex))

        if venueIndex > 14: #it's not on current page, go to next page
            print("On venue select, skipping to next page")
            nextButtonLoc = buttonLocsDict["venueNextPageLoc"] or pyautogui.locateOnScreen("venueNext.png")
            nextCenterX, nextCenterY = pyautogui.center(nextButtonLoc)
            pyautogui.click(nextCenterX, nextCenterY)

        venueLoc = buttonLocsDict["venueLoc"] or pyautogui.locateOnScreen("venues/"+venueName+".png")
        venueCenterX, venueCenterY = pyautogui.center(venueLoc)
        pyautogui.click(venueCenterX, venueCenterY)

    elif state == "normal":
        #both victory and defeat have a fightOn button which we locate on,
        #conveniently in the same location
        buttonLoc = buttonLocsDict["fightOnButtonLoc"] or pyautogui.locateOnScreen("fightOn.png")
        buttonCenterX, buttonCenterY = pyautogui.center(buttonLoc)
        pyautogui.click(buttonCenterX, buttonCenterY)

    elif state == "lowHp": 
        pyautogui.press("f5")

        #After refreshing page, this becomes the main menu case
        time.sleep(5) #Wait for page to load
        loadBattle(state="mainMenu", venueIndex=venueIndex, buttonLocsDict = buttonLocsDict)

    else:
        print("Check your state input")

#===========
#    SETUP before first battle
#===========


def createDragons(configDragons, buttonLocsDict):
    """At battlestart, locate Dragons based on full HP bars.

    Parameters:
    list-of-lists configDragons: required parameter which describes dragon
    configs (Roles such as grinder/trainee and eliminate hotkey)
    Creates dragons based on specified configs.

    dict buttonLocsDict: (see loadBattle)
    
    Returns: a list of Dragon objects
    """
    dragonList = []
    dragonHPLocs = []
    for loc in pyautogui.locateAllOnScreen("unitFullHP.png", 
        region = buttonLocsDict["lowerLeftQuad"]):
        dragonHPLocs.append(loc) #A set of coords describing unit HP bar position

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
                                 role = configDragons[i][0],
                                 elimKey = configDragons[i][1]))
    return dragonList

#HP can change during battle, but as long as a foe is alive,
#their MP bar looks the same
#That having been said, since this is only run at start of battle,
#This measure may be unnecessary. But it works as-is.
def createFoes(buttonLocsDict, inputThresh=None):
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
        region = buttonLocsDict["upperRightQuad"]):
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
        if inputThresh == None:
            foeList.append(Foe(hpLoc = hpLoc, mpLoc = mpLoc,
                               posKey = keybind[i]))
        else:
            foeList.append(Foe(hpLoc = hpLoc, mpLoc = mpLoc,
                               posKey = keybind[i],
                               threshhold = inputThresh)) 
    return foeList


def areDragonsWeak(dragonList):
    """During battleturns, check if a grinder dragon is weak.

    Parameters: A list of Dragons created at battlestart by createDragons()
    Returns: boolean
    True if all grinder dragons are missing HP below their
    pain threshhold (Dragon.threshhold). Ignores non-grinders
    False otherwise.
    """
    grinderCount = len([d for d in dragonList if d.role == "grinder"])
    weakCount = 0
    
    for d in dragonList:
        if d.role == "grinder" and d.isHpLow():
            weakCount+=1

    return(weakCount >= grinderCount)

    #for d in dragonList:
    #    if d.role != "trainee" and d.isHpLow():
    #        return True
    #return False

#==============================================================================#
#    CHECK BATTLE STATUS
#==============================================================================#

def checkCaptcha(buttonLocsDict):
    """At battlestart, check for captcha.
    If captcha is found, halts execution to ask user to solve.
    
    Parameters:
    dict buttonLocsDict: (see loadBattle)
    Returns: bool
    """
    captchaPresence = pyautogui.locateOnScreen("camping.png")
    # if captchaPresence != None:
    #     input("Captcha detected, please solve then hit enter.")
    #     time.sleep(5)
    # return None

    return bool(captchaPresence)

def isBattleOver(buttonLocsDict):
    """During battleturns, check if the battle is over,
    and has ended in Victory or Defeat.
    Both states have a Fight On button, so they're collapsed into
    one function.

    Parameters:
    dict buttonLocsDict: (see loadBattle)    
    
    Returns: True if battle is over, False otherwise
    """
    
    return bool(pyautogui.locateOnScreen("fightOn.png"))

def getReadyDragon(dragonList):
    """During battleturns, check which dragon is ready, if any.

    Parameters: A list of Dragons created at battlestart by createDragons()
    Returns: Positional index of ready dragon (0, 1, or 2)
    If no dragon is ready, returns -1
    """
    #One could use image processing on the entire screen,
    #but limiting the search to the region next to the dragon HP bar
    #limits the search, and also is easier to assign "ready" to "dragon"
    #brittle--may change depend on screen reso--TODO?

    for i in range(len(dragonList)):
        d = dragonList[i]
        searchRegion = (d.hpLoc[0]+d.hpLoc[2], d.hpLoc[1]-30,
                        150, 70)
        # print("DEBUG: searchRegion == " + str(searchRegion))

        tempLoc = pyautogui.locateOnScreen("ready.png", region=searchRegion)
        
        if bool(tempLoc) == True:
            return i
    return -1

def checkFoes(foeList, searchForWeak = False):
    """During battleturns, check which of the foes created at battlestart
    are not dead.

    Parameters:
    -a list of Foes created at battlestart by createFoes()

    Returns: list of various statuses ("Healthy", "Weak", etc)
    """
    foeStatuses = []
    for foe in foeList:
        if foe.isAlive() and foe.isHpLow():
            foeStatuses.append("Weak")
        elif foe.isAlive():
            foeStatuses.append("Healthy")
        else:
            foeStatuses.append("Dead")
    return foeStatuses

