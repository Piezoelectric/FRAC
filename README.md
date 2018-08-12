# 𝓕𝓡 𝓐𝓾𝓽𝓸 𝓒𝓸𝓵𝓲

Python script which automates the process of playing/grinding the 𝓕--𝓵𝓲𝓰 𝓱𝓽 𝓡--𝓲𝓼--𝓲 𝓷𝓰 𝓒--𝓸𝓵𝓲--𝓼𝓮  𝓾--𝓶. Uses `PyAutoGUI` to take screenshots of the current screen, locate buttons, and analyze HP values. Should work on mac, linux, windows.

(Fancy text is to avoid Google's text crawler picking this up, hopefully.)

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

This defines the number of battles, and the index (0-indexed) of the 𝓒𝓸𝓵𝓲𝓼𝓮𝓾𝓶 venue you want to battle in.

You should set your browser zoom level so the 𝓒𝓸𝓵𝓲𝓼𝓮𝓾𝓶 displays with no blurriness or aliasing, and so it fully displays without scrolling the browser window. Browsers, OSes, and monitors may display the coliseum canvas differently, but the actual elements of the coliseum canvas should look the same. 

If stuff isn't working, try replacing each of the images in the directory with a screenshot from _your_ browser. 

Set up the 𝓒𝓸𝓵𝓲𝓼𝓮𝓾𝓶 to enable keyboard hotkeys, and disable animations and visual effects.

## Running

Navigate to the 𝓒𝓸𝓵𝓲𝓼𝓮𝓾𝓶's main menu page (the Monster Battle button should be visible). Then invoke `python3 AutoColi.py` to start the script. Ideally you should split-screen so that your battle window and your Python window are both visible.

Keep the browser window focused as much as possible, so that keystrokes are sent to the correct window.

Note that 𝓒𝓸𝓵𝓲𝓼𝓮𝓾𝓶 captchas are not automatically solved. Upon seeing a captcha, the script will pause to wait for you to solve it. You'll need to manually intervene every 10 or so battles. But hey, it's much better than manually doing all 10 battles.

# Why use this?

Sometimes I see people on the forums say "grinding isn't so bad, I usually watch netflix/listen to podcasts while I do it". When your game is so dull you have to come up with alternate ways to entertain yourself while playing the game ... it's not really worth the time and energy.

[The game...is not fun.](https://www.youtube.com/watch?v=RphXjirD9p4) (If it's not fun, why bother?)

As for using this over other services, this script only uses visual cues and keyboard hotkeys, and does not use websocket code. Its only interaction with the server is using keystrokes, which are a perfectly legitimate way of interacting with the server. Aside from that, all it does is screenshot the screen and tell the user where stuff is on screen, which is all on the user's computer.

# Changelog

(I developed the first few versions on a personal machine before porting my code to Github. Despite this being the first "public" version, there are changes from previous personal versions.)

**Version 11 / 2018-07-31**
* Changed "lowHP" battle ending to use f5 refresh key (previously it used image detection to find the browser refresh button)
* Changed Foe HP threshhold default to 0.95
* More robust code for handling battle end scenarios
    * Rolled "defeat" and "victory" into one condition, since the Fight On button is in the same spot for both end conditions
    * changed loadBattle()
    * changed isBattleWon() -> isBattleOver()
* Faster battle loading
    * Instead of checking the entire screen for the "fight on" button, the coordinates of the fight on button are stored, and used as a much smaller search region. This speeds battles up significantly, as there is no longer a 3 second delay in between each dragon's action
* Better error handling
    * If numFoes or numDragons = 0, the script will try to scan for foes again, as opposed to infinite-looping or immediately breaking. (The number of foes or dragons will never be 0 in a real battle)
* Misc text/print tweaks

**Version 10 / 2018-06-16** 
* Expanded venue select to 2nd page
* Supports exalt-grinding (previously only material grinding)
    * New battle logic which handles trainee/grinder distinction
    * "role" field added to Dragons
    * Trainees only defend with d key
    * Trainees may be KOd and battle will continue
* Added print method to Dragons
* Fixed `Battle.getReadyDragon()` function so it doesnt search entire screen
* Added new parameter to `Battle.loadBattle()`, which takes coordinates of "Fight On" button. Previously the script would search for the Fight On button everytime, though the actual button would not change positions. By re-using known coordinates of this button, the next battle is loaded faster
* Changed Foes default pain threshhold to .75 (from .66), Dragons threshhold to .1 (from .25)
