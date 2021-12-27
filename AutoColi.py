import pyautogui
import time
from Battle import *
import Menu
import Battle

from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw #For debugging logging features

#==============================================================================#
#    NOTES

#PyAutoGui's locateOnScreen is Image-based detection,
#used for finding units and image processing and nearly everything,
#since HTML5 Canvas elements are non-capturable

#PyAutoGui.locateOnScreen returns a tuple of coordinates if image was found,
#returns None if not found. (left, top, width, height)

#hp, mp are never capitalized, unless in camelCasing
#==============================================================================#

#==============================================================================#
#    Config
#==============================================================================#

# TODO - move all this to a YAML file or command line prompts

#[role, eliminate hotkey if applicable]
configDragons = [
    ["grinder", "s"],
    ["grinder", "s"],
    ["grinder", "s"] 
    ]

numBattles = 5
venueIndex = 11

#Use coordinate math instead of fullscreen search
fastMode = True

#Enable to save captchas (require fastmode)
captchaLogging = True

#Enable if enemies are weak/low-level, and can be instantly Eliminated
instantEliminate = False

#==============================================================================#
#    Main
#Perform some initial setup
#==============================================================================#

def epochTime():
    '''Return seconds since epoch as a string;
    used for filenames.
    Parameters: None'''
    return str(time.time()).split('.')[0] 

print("Main program started")

state = "mainMenu"

buttonLocsDict = {
    "canvasLoc": None,
    "monsterBattleButtonLoc": None,
    "fightOnButtonLoc": None,
    "venueNextPageLoc": None, 
    "venueLoc": None,
    "captchaLoc": None,
    "lowerLeftQuad": None, #quadrant used to find dragon HP bars
    "upperRightQuad": None, #quadrant used to find foe MP bars
    }

if fastMode:
    buttonLocsDict = Menu.extrapolateButtonLocs(venueIndex)
    print("Warning: fast mode enabled!")
    print(buttonLocsDict)
else:
    buttonLocsDict["monsterBattleButtonLoc"] = pyautogui.locateOnScreen("monsterBattle.png")

for i in range(numBattles):
    #==========================================================================#
    #    Perform a single battle
    # Loads the next battle depending on how the previous battle ended ('state').
    # States: "normal" (victory or defeat, click fightOn),
    # "lowHp" (causes the page to refresh and redirect to main menu),
    # "mainMenu" (navigate the menu to the venue)
    #==========================================================================#

    print("Loading battle with state " + state)
    Menu.loadBattle(state, venueIndex, buttonLocsDict)
   
    time.sleep(2) #may need to wait for the battle to load in

    #==========================================================================#
    #    Battle Start
    #Create the initial list of foes and dragons
    #==========================================================================#

    battleActive = True

    foeList = []
    foeHpThreshhold = 1 if instantEliminate else None

    #Captchas appear before a battle starts.
    #If captchaLogging is enabled, save captcha to file

    coords = pyautogui.locateOnScreen("camping.png")
    coords2 = pyautogui.locateOnScreen("campingZoomed.png")
    #account for both zoom levels
    
    if coords or coords2: #if captcha was found, i.e. coords not (0,0)
        print("[CAPTCHA] Captcha found")

        if captchaLogging:
            centerOfColi = pyautogui.center(buttonLocsDict["canvasLoc"])
            pyautogui.click(x=centerOfColi[0], y=centerOfColi[1], button='right')
            pyautogui.press(['v', 'enter']) #navs to "save image as" in menu
            time.sleep(0.3)
            
            pyautogui.typewrite(epochTime()+".png") #enter image filename
            time.sleep(1)
            pyautogui.press(['enter'])
            time.sleep(.3)
            pyautogui.press(['enter'])

            #user has solved captcha so while loop exited;
            #record user's mouse position and save
            #What about the problem of user solves the first captcha incorrectly?? -TODO
            #solution = pyautogui.position()
            print("[CAPTCHA] saved, proceeding")

    #Dragon setup -- should only be done at the start of the first battle
    if i == 0:
        dragonList = []
        while len(dragonList) == 0:
            dragonList = Menu.createDragons(configDragons, buttonLocsDict)
        for d in dragonList:
            print(d)

    #Logic module setup
    #battleLogicModule = BasicEliminateTrainerLogic(dragonList, foeList)
    battleLogicModule = SpamLogic(dragonList)

    #rescan until foes found (len foeList > 0);
    #Menu.createFoes creates foes and assigns their hotkey.
    #Notably, foes only appear after captcha is solved.
    #So this loop acts as a backup "captcha check".
    #the program will never proceed until the captcha is solved,
    #since no enemies are loaded/can be found.
    while len(foeList) == 0 and battleLogicModule.careAboutFoeList():
        "Initializing foe list"
        foeList = Menu.createFoes(buttonLocsDict, foeHpThreshhold)
        battleLogicModule.setFoeList(foeList)

    print("Begin Battle [" + str(i) + "]")
    print("Number of dragons: " + str(len(dragonList)))
    print("Number of foes: %s"%(len(foeList) if foeList else "who cares"))

    #==========================================================================#
    #    Battle Active
    # Endlessly loop until battle is over
    #==========================================================================#

    while battleActive:
        #======================================================================#
        #    Battle End Checks
        # At each moment, check if battle is over
        # If so, break (skip the rest of the while loop)
        #======================================================================#
            
        #Check if battle ended normally (victory or defeat)
        if Menu.isBattleOver(buttonLocsDict):
            print("Battle [" + str(i) + "] ended normally")
            state = "normal"
            battleActive = False
            break

        #If any non-trainee's HP is too low (Trainees can die no problem)
        #Refresh page (don't wait for defeat)
        if Menu.areDragonsWeak(dragonList):
            print("Battle [" + str(i) + "] ended with lowHp")
            state = "lowHp"
            battleActive = False
            break

        #======================================================================#
        #    Battle Turn
        # Since the battle is not over, make an attack
        #======================================================================#
        readyDragonIndex = Menu.getReadyDragon(dragonList)

        # No dragons ready --> foe attacking. Sometimes we don't care if the dragon is ready.
        if readyDragonIndex == -1 and battleLogicModule.careAboutDragonReady():
            print("No dragons active, waiting")
            time.sleep(1) #Allow foe animations to finish
            continue

        # Dragon ready (or the ready check was ignored) --> have it make an action
        keyString = battleLogicModule.determineAction(readyDragonIndex)
        print("keyString", keyString)
        pyautogui.typewrite(keyString, interval = 0.1) 

        time.sleep(0.25) #Allow dragon's attack anim to finish

        #print("Battle Turn completed")

#==============================================================================#
#    End For Loop
#All battles are now over.
#==============================================================================#

print("Finished all battles.")


# TODO LIST
# - Refactor to read all config from a config.yml file
# - Fix the broken BasicEliminateTrainerLogic to be less, uh, broken
# - add a main() function and if name == __main__ 