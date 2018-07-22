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
#    LOAD BATTLE
#==============================================================================#

def loadBattle(state="mainMenu", venueIndex = 0, inputLoc = None):
    """Loads the next battle depending on how the previous battle ended.

    Parameters:
    string state: Indicates how the previous battle was ended,
    and the current screen state.
    -mainMenu: (Default) Coli main menu screen.
    Click monsterBattle button, then click a venue.
    (Currently hardcoded to Training Fields.)
    -victory: Clicks the fightOn button.
    -defeat: Not yet coded
    -lowHp: A dragon has low health. Refresh the page to get to main menu.

    int venueIndex: determines the venue to load from. 0 indexd.
    Defaults to 0 (Training Fields)
    Only used if we're on the main menu

    buttonCoords: optional parameter, holds coordinates for any button to press.
    Default none.
    Can be used to save time if clicking the same button over and over,
    by bypassing the screenshot-based image matching.
    (for example, the Fight On button--which is where its currently used--
    it's in the same location every time).
    If buttonCoords for the button to click are not specified or are invalid,
    defaults to image matching.
    
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
        "redrockCove",
        "waterway",
        "arena",
        "volcanicVents",
        "rainsongJungle",
        "borealWood",
        "crystalPools",
        "harpysRoost", #index 14, end of first page
        "ghostlightRuins",
        "mire",
        "kelpBeds",
        "golemWorkshop" #DO NOT EVER DO THE GOLEM WORKSHOP
        ]
    
    if state == "mainMenu":
        #Click seizure warning, if it exists
        seizureWarningLoc = pyautogui.locateOnScreen("seizureWarning.png")
        if bool(seizureWarningLoc):
            seizeCenterX, seizeCenterY = pyautogui.center(seizureWarningLoc)
            pyautogui.click(seizeCenterX, seizeCenterY)
        time.sleep(1)

        #From main menu click Monster battle button
        buttonLoc = pyautogui.locateOnScreen("monsterBattle.png")
        #Monster Battle button glows when moused over. be careful!
        buttonCenterX, buttonCenterY = pyautogui.center(buttonLoc)
        pyautogui.click(buttonCenterX, buttonCenterY)
        time.sleep(1)

        #Click the appropriate venue
        venueName = venueNames[venueIndex]
        print(venueName + " index num " + str(venueIndex))

        if venueIndex > 14: #it's not on current page, go to next page
            print("On venue select, skipping to next page")
            nextButtonLoc = pyautogui.locateOnScreen("venueNext.png")
            nextCenterX, nextCenterY = pyautogui.center(nextButtonLoc)
            pyautogui.click(nextCenterX, nextCenterY)
            time.sleep(1)
            
        venueLoc = pyautogui.locateOnScreen(venueName+".png")
        venueCenterX, venueCenterY = pyautogui.center(venueLoc)
        pyautogui.click(venueCenterX, venueCenterY)
        
    elif state == "victory":
        if bool(inputLoc) == True: #if loc specified use it
            buttonCenterX, buttonCenterY = pyautogui.center(inputLoc)
        else: #if loc not specified default to the usual image-based search
            buttonLoc = pyautogui.locateOnScreen("fightOn.png")
            buttonCenterX, buttonCenterY = pyautogui.center(buttonLoc)

        pyautogui.click(buttonCenterX, buttonCenterY)

    elif state == "defeat":
        pass #TODO

    elif state == "lowHp": 
        #buttonLoc = pyautogui.locateOnScreen("refresh.png")
        #buttonCenterX, buttonCenterY = pyautogui.center(buttonLoc)
        #pyautogui.click(buttonCenterX, buttonCenterY)
        pyautogui.press("f5")

        #After refreshing page, this becomes the main menu case
        time.sleep(5) #Wait for page to load
        loadBattle(state="mainMenu", venueIndex=venueIndex)

    else:
        print("Check your state input")
    
    return None

#==============================================================================#
#    BATTLESTART
#==============================================================================#

def checkCaptcha():
    """At battlestart, check for captcha.
    If captcha is found, halts execution to ask user to solve.
    
    Parameters: None
    Returns: None
    """
    captchaPresence = pyautogui.locateOnScreen("camping.png")
    if captchaPresence:
        input("Captcha detected, please solve then hit enter.")
        time.sleep(5)
    return None

def createDragons(configDragons):
    """At battlestart, locate Dragons based on full HP bars.

    Parameters:
    list-of-lists configDragons: required parameter which describes dragon
    configs (Roles such as grinder/trainee and eliminate hotkey)
    Creates dragons based on specified configs.
    
    Returns: a list of Dragon objects
    """
    dragonList = []
    dragonHPLocs = []
    for loc in pyautogui.locateAllOnScreen("unitFullHP.png"):
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
def createFoes():
    """At battlestart, locate Foes based on MP bars,
    and create Foe objects.

    Parameters: None
    Returns: a list of Foe objects
    """
    foeList = []
    foeMPLocs = []
    for loc in pyautogui.locateAllOnScreen("foeMP.png"):
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
        foeList.append(Foe(hpLoc = hpLoc, mpLoc = mpLoc,
                           posKey = keybind[i])) 
    return foeList

#==============================================================================#
#    Check Battle End Functions
#==============================================================================#

def isBattleWon():
    """During battleturns, check if the battle is over.

    Parameters: None (image processing on entire screen)
    Returns: True if battle is over, False otherwise
    """
    tempLoc = pyautogui.locateOnScreen("experience.png")
    return bool(tempLoc)

def isDragonWeak(dragonList):
    """During battleturns, check if a grinder dragon is weak.

    Parameters: A list of Dragons created at battlestart by createDragons()
    Returns: boolean
    True if one (or more) grinder dragons is missing HP below their
    pain threshhold (Dragon.threshhold)
    False otherwise.
    Ignores trainees
    """
    for d in dragonList:
        if d.role != "trainee" and d.isHpLow():
            return True
    return False

#==============================================================================#
#    BATTLETURN
#Assuming battle hasn't hit an end condition--proceed as normal
#==============================================================================#


def getReadyDragon(dragonList):
    """During battleturns, check which dragon is ready, if any.

    Parameters: A list of Dragons created at battlestart by createDragons()
    Returns: Positional index of ready dragon (0, 1, or 2)
    If no dragon is ready, returns -1
    """
    #One could use image processing on the entire screen,
    #but limiting the search to the region next to the dragon HP bar
    #limits the search, and also is easier to assign "ready" to "dragon"

    for i in range(len(dragonList)):
        d = dragonList[i]
        searchRegion = (d.hpLoc[0]+d.hpLoc[2], d.hpLoc[1]-30,
                        150, 70)
        print("DEBUG: searchRegion == " + str(searchRegion))

        #brittle--may change depend on screen reso--TODO?
        #pyautogui.screenshot("aaaaa.png", region=searchRegion)
        tempLoc = pyautogui.locateOnScreen("ready.png", region=searchRegion)
        
        if bool(tempLoc) == True:
            return i
    return -1

def getActiveFoe(foeList, searchForWeak = False):
    """During battleturns, check which of the foes created at battlestart
    are not dead.

    Parameters:
    -a list of Foes created at battlestart by createFoes()
    -optional searchForWeak boolean, default false. If set to true,
    Must return a foe that is both alive and has low Hp;
    otherwise just searches for a foe that's alive.
    
    Returns: the positional index of the first non-dead foe (0,1,2,3)
    If no foe meets the search criteria, returns -1
    """
    for i in range(len(foeList)):
        f = foeList[i]
        if searchForWeak:
            if f.isAlive() and f.isHpLow():
                return i
        else:
            if f.isAlive() == True:
                return i
    return -1

