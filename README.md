# FRAutoColi

Python script which automates the process of playing/grinding the Flight Rising coliseum. Uses `PyAutoGUI` to take screenshots of the current screen, locate buttons, and analyze HP values. Should work on mac, linux, windows.

`AutoColi.py` contains the main battle logic. `Battle.py` contains helper functions. `Units.py` contains the classes Foe and Dragon. 

# Usage

## Config

Get some level 25 dragons. I don't know or care how. Follow one of the physical glass cannon builds (STR focus with Eliminate).

In `AutoColi.py`, find the following lines:

```
configDragons = [
    ["grinder", "s"],
    ["grinder", "s"],
    ["trainee", None]
    ]
```

This defines your dragons (from top to bottom on the battle screen). Change role between "grinder" and "trainee". The second parameter is the dragon's hotkey for Eliminate. Trainees should not set an Eliminate hotkey. 

```
numBattles = 20
venueIndex = 15
```

This defines the number of battles, and the index (0-indexed) of the Coliseum venue you want to battle in. This is set to 15 (Ghostlight Ruins) by default (best place for exalt training IMO).

Ideally, you should set your browser zoom level so the FR coliseum displays with no blurriness or aliasing. Browsers, OSes, and monitors may display the coliseum canvas differently, but the actual elements of the coliseum canvas should look the same. 

If stuff isn't working, try replacing each of the images in the directory with a screenshot from _your_ browser. 

Set up the FR Coliseum to enable keyboard hotkeys, and disable animations and visual effects.

## Running

Navigate to the coliseum's main menu page (the Monster Battle button should be visible). Then invoke `python3 AutoColi.py` to start the script. Ideally you should split-screen so that your battle window and your Python window are both visible.

Keep the browser window focused as much as possible, so that keystrokes are sent to the correct window.

Note that Coliseum captchas are not automatically solved. Upon seeing a captcha, the script will pause to wait for you to solve it. You'll need to manually intervene every 10 or so battles. But hey, it's much better than manually doing all 10 battles.

# Why?

Sometimes I see people on the forums say "Coli grinding isn't so bad, I usually watch netflix/listen to podcasts while I do it". When your game is so dull you have to come up with alternate ways to entertain yourself while playing the game ... it's not really worth the time and energy.


# Changelog

(I developed the first few versions on a personal machine before porting my code to Github. Despite this being the first "public" version, there are changes from previous personal versions.)

**Current Version 10 / 2018-06-16** 
* Expanded venue select to 2nd page
* Supports exalt-grinding (previously only material grinding)
    * New battle logic which handles trainee/grinder distinction
    * "role" field added to Dragons
    * Trainees only defend with d key
    * Trainees may be KOd and battle will continue
* Added print method to Dragons
* Fixed `Battle.getReadyDragon()` function so it doesnt search entire screen
* Added new parameter to `Battle.loadBattle()`, which takes coordinates of "Fight On" button. Previously the script would search for the Fight On button everytime, though the actual button would not change positions. By re-using known coordinates of this button, the next battle is loaded faster
* Changed Foes pain threshhold to .75 (from .66), Dragons threshhold to .1 (from .25)
