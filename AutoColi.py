import pyautogui
import pyautogui_ext
import time

import Battle

#==============================================================================#
#    NOTES

#PyAutoGui's locateOnScreen is Image-based detection,
#used for finding units and image processing and nearly everything,
#since HTML5 Canvas elements are non-capturable

#PyAutoGui.locateOnScreen returns a tuple of coordinates if image was found,
#returns None if not found. (left, top, width, height)
#tuples are truthy and None is falsy

#For locateOnScreen and locateAllOnScreen,
#if region=None, defaults to searching entire screen

#PyAutoGui also has a keyboard thing,
#pyautogui.typewrite('Hello world!') 
#used to actually input battle commands

#Units contains Dragon and Foe classes

#Battle contains helper functions to overview the entire battle;
#It's not a from-import, so I can tell that the functions
#refer to the battle overview

#using the snipping tool DOES NOT WORK for some reason (possibly filenames??)
#Youre better off using GIMP and cutting the reference images needed

#hp, mp are never capitalized, unless in camelCasing
#==============================================================================#

#==============================================================================#
#    Config
#==============================================================================#

#[role, eliminate hotkey if applicable]
configDragons = [
    ["grinder", "s"],
    ["grinder", "s"],
    ["grinder", "a"] 
    ]

numBattles = 50
venueIndex = 2

#Enable to save captchas (require fastmode)
captchaLogging = True

#Use coordinate math instead of fullscreen search
fastMode = True

#Enable if enemies are weak/low-level, and can be instantly Eliminated
instantEliminate = True

#==============================================================================#
#    Main
#Perform some initial setup
#==============================================================================#

print("Bring up battle window within 5 seconds")
time.sleep(5)

state = "mainMenu"

#Every entry is a SEARCH REGION for the button,
#not necessarily the direct coordinate of the button;
#These smaller regions are used to reduce search times
#(as default, pyautogui searches the entire screen)
#They can be set to the exact location of the button,
#In which case the search should automatically succeed
#But of course, coordinate math is always risky
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
    buttonLocsDict = Battle.extrapolateButtonLocs(venueIndex)
    print("Warning: fast mode enabled!")
    print(buttonLocsDict)
else:
    buttonLocsDict["monsterBattleButtonLoc"] = pyautogui.locateOnScreen("monsterBattle.png")

for i in range(numBattles):
    #==========================================================================#
    #    Perform a single battle
    #Loads the next battle depending on how the previous battle ended ('state').
    #States: "normal" (victory or defeat, click fightOn),
    #"lowHp" (causes the page to refresh and redirect to main menu),
    #"mainMenu" (navigate the menu to the venue)
    #==========================================================================#

    print("Loading battle with state " + state)
    Battle.loadBattle(state, venueIndex, buttonLocsDict)
   
    time.sleep(2) #may need to wait for the battle to load in

    #==========================================================================#
    #    Battle Start
    #Create the initial list of foes and dragons
    #==========================================================================#

    battleActive = True

    foeList = []
    foeHpThreshhold = None
    if instantEliminate == True:
        foeHpThreshhold = 1

    #Captchas appear before a battle starts.
    #If captchaLogging is enabled, this code saves the captcha to disk,

    if captchaLogging and buttonLocsDict["captchaLoc"] and buttonLocsDict["canvasLoc"]:
        print("DEBUG: captchaLogging active",
              str(buttonLocsDict["captchaLoc"]))
        coords = pyautogui.locateOnScreen("camping.png",
                                          region=buttonLocsDict["captchaLoc"])
        coords2 = pyautogui.locateOnScreen("campingZoomed.png",
                                          region=buttonLocsDict["captchaLoc"])
        #account for both zoom levels
        
        if coords or coords2: #if captcha was found, i.e. coords not (0,0)
            print("DEBUG: captcha found")
            epochTime = str(time.time()).split('.')[0] #gets seconds since epoch start

            centerOfColi = pyautogui.center(buttonLocsDict["canvasLoc"])
            pyautogui.click(x=centerOfColi[0], y=centerOfColi[1], button='right')
            pyautogui.press(['v', 'enter']) #navs to "save image as" in menu
            time.sleep(0.3)
            
            pyautogui.typewrite(epochTime+".png") #enter image filename
            time.sleep(0.3)
            pyautogui.press('enter')

            #user has solved captcha so while loop exited;
            #record user's mouse position and save
            #What about the problem of user solves the first captcha incorrectly?? -TODO
            #solution = pyautogui.position()
            print("DEBUG: captcha saved, proceeding")

    #rescan until foes found (len foeList > 0)
    #Notably, foes only appear after captcha is solved.
    #So this loop acts as a backup "captcha check".
    #the program will never proceed until the captcha is solved,
    #since no enemies are loaded/can be found,
    #and will automatically proceed once the captcha is solved
    while len(foeList) == 0:
        foeList = Battle.createFoes(buttonLocsDict, foeHpThreshhold)

    #This should only be done at the start of the FIRST battle
    #The unit may have lost some HP after the first battle, but
    #its HP coords are still known. dragons dont move.
    #Attempt to recreate dragonList if 0 dragons found
    if i < 1:
        dragonList = Battle.createDragons(configDragons, buttonLocsDict)
        while len(dragonList) == 0:
            dragonList = Battle.createDragons(configDragons, buttonLocsDict)
        for d in dragonList:
            print(d)

    print("Begin Battle [" + str(i) + "]")
    print("Number of dragons: " + str(len(dragonList)))
    print("Number of foes: " + str(len(foeList)))

    #==========================================================================#
    #    Battle Active
    #Endlessly make Turns until battle is over
    #==========================================================================#

    while battleActive:
        #======================================================================#
        #    Battle End Checks
        #At each turn, check if battle is over
        #If so, break (skip the rest of the while loop)
        #======================================================================#

        #If we need to find the fightOn button
        if buttonLocsDict["fightOnButtonLoc"] == False: 
            fightOnButtonLoc = pyautogui.locateOnScreen("fightOn.png")
            
        #Check if battle ended normally (victory or defeat)
        if Battle.isBattleOver(buttonLocsDict) == True:
            print("Battle [" + str(i) + "] ended normally")
            state = "normal"
            battleActive = False
            break

        #If any non-trainee's HP is too low (Trainees can die no problem)
        #Refresh page (don't wait for defeat)
        if Battle.areDragonsWeak(dragonList) == True:
            print("Battle [" + str(i) + "] ended with lowHp")
            state = "lowHp"
            battleActive = False
            break

        #======================================================================#
        #    Battle Turn
        #Since the battle is not over, make an attack
        #======================================================================#
        readyDragonIndex = Battle.getReadyDragon(dragonList)
        print("readyDragonIndex == " + str(readyDragonIndex))

        #No dragons ready --> foe attacking
        if readyDragonIndex == -1:
            print("No dragons active, waiting")
            time.sleep(0.25) #Allow foe animations to finish

        #Dragon ready --> have it make an action
        else:
            d = dragonList[readyDragonIndex]
            foeIndex = Battle.getActiveFoe(foeList, searchForWeak = True)
            #getActiveFoe returns first active foe that meets the conditions

            #If elim is ready and a weak foe exists, eliminate that foe
            if d.isElimReady() == True and foeIndex != -1:
                f = foeList[foeIndex]
                print("Sending Eliminate to foe: " + f.posKey)
                keyString = "a" + d.elimKey + f.posKey
                pyautogui.typewrite(keyString, interval = 0.1) 
                #TODO: Consider moving elim and scratch into the Dragon class.

            #elif dragon is a trainee, defend
            elif d.role == "trainee":
                print("Sending defend action")
                pyautogui.typewrite("d", interval = 0.3)
                
            #else (default), scratch first active foe
            else:
                f = foeList[Battle.getActiveFoe(foeList)]
                print("Sending Scratch to foe: " + f.posKey)
                keyString = "a" + "e" + f.posKey
                pyautogui.typewrite(keyString, interval = 0.1) 
                #scratch key will ALWAYS be e

            time.sleep(0.25) #Allow dragon's attack anim to finish

        print("Battle Turn completed")

    #==========================================================================#
    #    Battle End
    #The while loop of endless turns is over,
    #so the battle has ended for one reason or another
    #Jump back up to top of for loop
    #==========================================================================#
    print("----------")

#==============================================================================#
#    End For Loop
#==============================================================================#
print("Finished all battles.")
