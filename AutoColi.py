import pyautogui
import time
from Battle import *
from Game import Game

# from PIL import ImageFont
# from PIL import Image
# from PIL import ImageDraw #For debugging logging features

#==============================================================================#
#    NOTES

#PyAutoGui's locateOnScreen is Image-based detection,
#used for finding units and image processing and nearly everything,
#since HTML5 Canvas elements are non-capturable

#PyAutoGui.locateOnScreen returns a tuple of coordinates if image was found,
#returns None if not found. (left, top, width, height)

#hp, mp are never capitalized, unless in camelCasing
#==============================================================================#

def epochTime():
    '''Return seconds since epoch as a string;
    used for filenames.
    Parameters: None'''
    return str(time.time()).split('.')[0] 

def logCaptcha(coord):
    pyautogui.click(x=coord[0], y=coord[1], button='right')
    pyautogui.press(['v', 'enter']) #navs to "save image as" in menu
    time.sleep(0.3)
    
    pyautogui.typewrite(epochTime()+".png") #enter image filename
    time.sleep(1)
    pyautogui.press(['enter'])
    time.sleep(1)
    pyautogui.press(['enter'])

    #user has solved captcha so while loop exited;
    #record user's mouse position and save
    #What about the problem of user solves the first captcha incorrectly?? -TODO
    #solution = pyautogui.position()
    print("[CAPTCHA] saved, proceeding")

def parse_args(args_line):
    configDragons = [
        ["grinder", "s"],
        ["grinder", "s"],
        ["grinder", "s"] 
        ]

    numBattles = 5
    venueIndex = 11

    battleLogicModule = SpamLogic()

    #Use coordinate math instead of fullscreen search
    fastMode = True

    #Enable to save captchas (require fastmode)
    captchaLogging = True

    elimThreshold = 1

    return numBattles, configDragons, venueIndex, battleLogicModule, fastMode, elimThreshold, captchaLogging

def main(numBattles, configDragons, venueIndex, battleLogicModule, fastMode=True, elimThreshold=1, captchaLogging=False):
    game = Game(configDragons, venueIndex, battleLogicModule, fastMode, elimThreshold)
    # The initialization also calls getStateFromScreen automatically. Wowie
        
    for i in range(1,numBattles+1):
        print("Loading battle %s with state %s"%(i,game.state))
        
        if not game.loadBattle():
            break #The game couldn't load the battle correctly

        time.sleep(2) #may need to wait for the battle to load in

        if game.checkCaptcha():
            print("[CAPTCHA] Captcha found")
            if captchaLogging:
                coord = pyautogui.center(game.buttonLocsDict["canvasLoc"])
                logCaptcha(coord)

        # Perform setup
        shouldCreateDragons = i==1
        game.setupBattle(shouldCreateDragons)

        # Perform the game infinite loop
        print("Begin Battle [%s]"%i)
        print("Number of dragons: %s"%len(game.dragonList))
        print("Number of foes: %s"%(len(game.foeList) if game.foeList else "who cares"))
        game.battleLoop(i)
        # battleLoop contains an infinite While loop that will break on its own, returning to the main for-loop

    print("All battles done")


# TODO LIST
# - Refactor to read all config from a config.yml file
# - Fix the broken BasicEliminateTrainerLogic to be less, uh, broken
# [DONE] a main() function and if name == __main__ 

if __name__ == '__main__':
    # Get configs from command line

    # Get configs from YML
    #[role, eliminate hotkey if applicable]
    numBattles, configDragons, venueIndex, battleLogicModule, fastMode, elimThreshold, captchaLogging = parse_args('')

    main(numBattles, configDragons, venueIndex, battleLogicModule, fastMode, elimThreshold, captchaLogging)