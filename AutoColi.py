import pyautogui
import pyautogui_ext
import time

import Battle

from PIL import Image, ImageOps, ImageEnhance
import pytesseract

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

#Use coordinate math instead of fullscreen search
fastMode = True

#Enable if you want to log data (slows program execution, requires fastmode)
#Needs debugging or removal tbh
dataLogging = False

#Enable if you want to log enemy names (slows program exec, requires fast)
logNames = False

#For datalogging, specify location of tesseract.exe
pytesseract.pytesseract.tesseract_cmd = "C:\\Program Files (x86)\\Tesseract-OCR\\tesseract.exe"

#Enable to track specific items and how frequently they drop
drops = [
    "drops/StrangeChest.png",
    "drops/leporidaeGuise.png",
    "drops/giantCaterpillar.png",
    "drops/hourglass.png",
    "drops/beeOrchid.png"
    ]

#Enable if enemies are weak/low-level, and can be instantly Eliminated
instantEliminate = True

#==============================================================================#
#    Main
#Perform some initial setup
#==============================================================================#

print("Starting the program")

state = "mainMenu"

if dataLogging:
    now = Battle.nowStr()
    logFileHandle = open("logs/"+now+".csv", 'w')
    logFileHandle.write("Start Time,")
    logFileHandle.write("Foes,")
    for d in drops:
        logFileHandle.write(d+",")
    logFileHandle.write("Venue #,"+str(venueIndex))
    logFileHandle.write("\n")

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
    #==========================================================================#

    print("Loading battle with state " + state)
    if state == "normal":
        Battle.loadBattle(state, venueIndex, buttonLocsDict)
    elif state == "lowHp" or state == "mainMenu":
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

    #rescan until foes found (len foeList > 0)
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

    if dataLogging and buttonLocsDict["upperRightQuad"]:
        #If datalogging enabled and coordinates of upperRightQuad have been set,
        #log start time.
        startTime = Battle.nowStr()
        logFileHandle.write(startTime+",")
    
        if logNames: 
            #filename = "logs//"+startTime+"-Start.png" #Debugging
            #pyautogui.screenshot(filename, region=buttonLocsDict["upperRightQuad"])

            #Log each enemy's name
            for foe in foeList:
                foeNameRegion = (foe.mpLoc[0] - 50,
                                 foe.mpLoc[1] - 30,
                                 120, #Lmao I am just guessing
                                 15)
                print(foeNameRegion)
                foeNameScreenShot = pyautogui.screenshot(region=foeNameRegion)

                #Enhance screenshot so tesseract has an easier time working w it
                #foeNameScreenShot.show()

                foeNameScreenShot = foeNameScreenShot.resize((600,75),
                                                             resample=Image.BICUBIC)
                foeNameScreenShot = ImageOps.invert(foeNameScreenShot)
                brightener = ImageEnhance.Brightness(foeNameScreenShot)
                foeNameScreenShot = brightener.enhance(1.5)
                contraster = ImageEnhance.Contrast(foeNameScreenShot)
                foeNameScreenShot = contraster.enhance(2)

                #foeNameScreenShot.show()

                #Pass the enhanced screenshot to tesseract for analysis
                foeName = pytesseract.image_to_string(foeNameScreenShot, config="--psm 7")

                #Write text to file (remove any stray commas)
                text = "".join(char for char in foeName if char != ',')
                logFileHandle.write(text+";")
                print(text)
        else: #do not log names
            logFileHandle.write("--")
            pass
    
        #Move on to next log field
        logFileHandle.write(",")
    #end logging function     

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

    #If datalogging enabled and coordinates of upperRightQuad have been set,
    #capture battle end/loot drops
    if dataLogging and buttonLocsDict["upperRightQuad"]:
        filename = "logs/"+startTime+"-End.png"
        #pyautogui.screenshot(filename, region=buttonLocsDict["upperRightQuad"])

        for d in drops:
            located = pyautogui.locateOnScreen(d, region=buttonLocsDict["upperRightQuad"])
            if located: #Determine how many of that item was dropped
                located2 = (located[0], located[1], 50, 50)
                twoLocated = pyautogui.locateOnScreen("2items.png", region=located2)
                threeLocated = pyautogui.locateOnScreen("3items.png", region=located2)
                if twoLocated:
                    logFileHandle.write("2,")
                elif threeLocated:
                    logFileHandle.write("3,")
                else:
                    logFileHandle.write("1,")
            else:
                logFileHandle.write("0,")

        logFileHandle.write("\n")
        logFileHandle.flush()
        
    
    print("----------")

#==============================================================================#
#    End For Loop
#==============================================================================#
print("Finished all battles.")

if dataLogging:
    logFileHandle.close()
