import pyautogui
import time

import Battle

#==============================================================================#
#    NOTES

#Written for Firefox (post Quantum) versions, at 80% zoom
#on windows 7, 1920x1080
#May need to replace images

#NEW TO VERSION0010 (Jun 16 2018)
#-Expanded venue select to 2nd page
#-Supports exalt-grinding
#-New battle logic which handles trainee/grinder distinction
#--"role" field added to Dragons
#--Trainees only defend with d key
#--Trainees may be KOd and battle will continue
#-added print method to Dragons
#-Refined the getReadyDragon function so it doesnt saerch entire screen (bugfix)
#-Storing coordinates of "Fight On" button, so next battle is loaded faster
#-Changed Foes threshhold to .75 (from .66), Dragons threshhold to .1 (from .25)

#PyAutoGui's locateOnScreen is Image-based detection,
#used for finding units and image processing and nearly everything,
#since HTML5 Canvas elements are non-capturable

#PyAutoGui.locateOnScreen returns a tuple of coordinates if image was found,
#returns None if not found. (left, top, width, height)
#tuples are truthy and None is falsy.
#This trick is used in many places.

#PyAutoGui also has a keyboard thing,
#pyautogui.typewrite('Hello world!') 
#used to actually input battle commands

#Units contains Dragon and Foe classes

#Battle contains helper functions to overview the entire battle;
#It's not a from-import, so I can tell that the functions
#refer to the battle overview

#using the snipping tool DOES NOT WORK for some reason (possibly filenames??)
#Youre better off using GIMP and cutting the reference images needed

#TODO:
#Come up with a cleaner way to detect a dragon's eliminate hotkey
#Right now it's hardcoded, and buried in

#hp, mp are never capitalized, unless in camelCasing
#==============================================================================#

#==============================================================================#
#    Config
#==============================================================================#

#[role, eliminate hotkey if applicable]
configDragons = [
    ["grinder", "s"],
    ["grinder", "s"],
    ["trainee", None] 
    ]

numBattles = 1000
venueIndex = 15

#==============================================================================#
#    Main
#Perform some initial setup
#==============================================================================#

input("Press any key, bring up battle window in 5 seconds")
time.sleep(5)

state = "mainMenu"

#These two Coordinates will be fed into loadBattle,
#either as nonetype or as a tuple of coordinates
#See loadBattle documentation
monsterBattleButtonLoc = pyautogui.locateOnScreen("monsterBattle.png")
fightOnButtonLoc = None

for i in range(numBattles):
    #==========================================================================#
    #    Perform a single battle
    #Loads the next battle depending on how the previous battle ended ('state').
    #After that, resets state to mainMenu-- current battle may end differently.
    #==========================================================================#

    print("Loading battle with state " + state)
    if state == "normal":
        Battle.loadBattle(state, venueIndex, fightOnButtonLoc)
    elif state == "lowHp" or state == "mainMenu":
        Battle.loadBattle(state, venueIndex, monsterBattleButtonLoc)
        
    # state = "mainMenu" possibly unnecessary
    time.sleep(2) #may need to wait for the battle to load in

    #==========================================================================#
    #    Battle Start
    #Create the initial list of foes and dragons
    #==========================================================================#

    battleActive = True

    Battle.checkCaptcha()
    numFoeScans = 0
    foeList = Battle.createFoes()

    # in case foes not found (0 foes), rescan some times
    while numFoeScans < 10 and len(foeList) == 0:
        foeList = Battle.createFoes()
    #...and if numFoes still 0, pause for input
    if len(foeList) == 0:
        input("No foes found, check the Coliseum--press enter to resume")
        time.sleep(5)

    #This should only be done at the start of the FIRST battle
    #The unit may have lost some HP after the first battle, but
    #its HP coords are still known. dragons dont move.
    if i < 1:
        dragonList = Battle.createDragons(configDragons)
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
        if bool(fightOnButtonLoc) == False: 
            fightOnButtonLoc = pyautogui.locateOnScreen("fightOn.png")
            
        #Check if battle ended normally (victory or defeat)
        if Battle.isBattleOver(fightOnButtonLoc) == True:
            print("Battle [" + str(i) + "] ended normally")
            state = "normal"
            battleActive = False
            break

        #If any non-trainee's HP is too low (Trainees can die no problem)
        #Refresh page (don't wait for defeat)
        if Battle.isDragonWeak(dragonList) == True:
            print("Battle [" + str(i) + "] ended with lowHp")
            state = "lowHp"
            battleActive = False
            break

        #======================================================================#
        #    Battle Turn
        #Since the battle is not over, make an attack
        #======================================================================#
        readyDragonIndex = Battle.getReadyDragon(dragonList)
        print("DEBUG readyDragonIndex == " + str(readyDragonIndex))

        #No dragons ready --> foe attacking
        if readyDragonIndex == -1:
            print("No dragons active, waiting")
            time.sleep(1) #Allow foe animations to finish

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

            time.sleep(0.5) #Allow dragon's attack anim to finish

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
