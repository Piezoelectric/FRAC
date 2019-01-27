# 𝓕𝓡 𝓐𝓾𝓽𝓸 𝓒𝓸𝓵𝓲

Python script which automates the process of playing/grinding the 𝓕--𝓵𝓲𝓰 𝓱𝓽 𝓡--𝓲𝓼--𝓲 𝓷𝓰 𝓒--𝓸𝓵𝓲--𝓼𝓮  𝓾--𝓶. Uses `PyAutoGUI` to take screenshots of the current screen, locate buttons, and analyze HP values. Should work on mac, linux, windows.

(Fancy text is to avoid Google's text crawler picking this up, hopefully.)

`AutoColi.py` contains the main battle logic. `Battle.py` contains helper functions. `Units.py` contains the classes Foe and Dragon. 

Use at your own risk. I'm not responsible for any damages to your account. Don't go bragging that you use a bot, obviously. Don't run the bot 24/7 (not that it'll work anyway).

If you appreciate the program, feel free to donate at [a paypal link I didn't make yet].

# Usage

## Config

Get some level 25 dragons. I don't know or care how. Follow one of the physical glass cannon builds (STR focus with Eliminate).

Set up the 𝓒𝓸𝓵𝓲𝓼𝓮𝓾𝓶 to enable keyboard hotkeys, and disable animations and visual effects.

Download this repo as a zipfile and unzip it. Be sure to download [pyautogui_ext](https://github.com/Piezoelectric/PyAutoGui-Extensions) as well, and place that in the same directory.

In `AutoColi.py`, find the following lines:

```
configDragons = [
    ["grinder", "s"],
    ["grinder", "s"],
    ["trainee", None]
    ]
```

This defines your dragons (from top to bottom on the battle screen). Change role between "grinder" and "trainee". The second parameter is the dragon's hotkey for Eliminate. Trainees can set an Eliminate hotkey but it won't be used.

```
numBattles = 20
venueIndex = 18
```

This defines the number of battles, and the index of the 𝓒𝓸𝓵𝓲𝓼𝓮𝓾𝓶 venue you want to battle in. Indexes should start at 0, and indexes should include the next page buttons (so Next Page is index 15, Previous Page is index 16, Harpy's Roost is index 17, Ghostlight Ruins is index 18)

You should set your browser zoom level so the 𝓒𝓸𝓵𝓲𝓼𝓮𝓾𝓶 displays with no blurriness or aliasing, and so it fully displays without scrolling the browser window. Browsers, OSes, and monitors may display the coliseum canvas differently, but the actual elements of the coliseum canvas should look the same. You can use Glimm/Gloom to help adjust; the GG window should be 700 pixels wide, 600 px tall.

If stuff isn't working, try replacing each of the images in the directory with a screenshot from _your_ browser. 

```
fastMode = True
```

Enables/disables fast mode. Normal mode searches the entire screen for buttons and other features (the fight on button, unit HP bars, etc). Fast mode uses coordinate math to restrict the search area to a small region, and in some cases it directly locates the buttons without searching. Coordinate math may break depending on your screen settings, but it's much faster than searching the entire screen repeatedly.

```
captchaLogging = True
```

Enables/disables saving captchas to disk. Requires fastmode. (Only saves the first captcha. Does not record solution to captcha.)

```
instantEliminate = True
```

If a foe is low-level, a unit can use eliminate on it without using scratch first. Setting `instantEliminate` to True bypasses the scratch step and directly uses eliminate. Under the hood, it sets the "foe is in eliminate range" threshhold to 100% of its HP.

## Running

Navigate to the 𝓒𝓸𝓵𝓲𝓼𝓮𝓾𝓶's main menu page (the Monster Battle button should be visible). Then invoke `python3 AutoColi.py` to start the script. Ideally you should split-screen so that your battle window and your Python window are both visible.

Keep the browser window focused as much as possible, so that keystrokes are sent to the correct window. 

Note that 𝓒𝓸𝓵𝓲𝓼𝓮𝓾𝓶 captchas are not automatically solved. Upon seeing a captcha, the script will pause to wait for you to solve it. You'll need to manually intervene every 10 or so battles. But hey, it's much better than manually doing all 10 battles.

# Why use this?

Sometimes I see people on the forums say "grinding isn't so bad, I usually watch netflix/listen to podcasts while I do it". When your game is so dull you have to come up with alternate ways to entertain yourself while playing the game ... it's not really worth the time and energy.

[The game...is not fun.](https://www.youtube.com/watch?v=RphXjirD9p4) (If it's not fun, why bother?)

As for using this over other services, this script only uses visual cues and keyboard hotkeys, and does not use websocket code. Its only interaction with the server is using keystrokes, which are a perfectly legitimate way of interacting with the server. Aside from that, all it does is screenshot the screen and tell the user where stuff is on screen, which is all on the user's computer.

# Changelog

(I developed the first few versions on a personal machine before porting my code to Github. The "published" version numbers also account for changes from previous personal versions.) I should also figure out a better location to put these notes.

**Version 12.5 / 2018-12-28**

Added code which automatically saves captcha images to disk. Maybe, some day, we will be able to crack captchas. 

**Version 12.4 / 2018-12-23**

Updated to use [pyautogui_ext](https://github.com/Piezoelectric/PyAutoGui-Extensions). If you don't like pyautogui_ext (which is reasonable I guess), you can change all pyautogui_ext.function() calls back to pyautogui, since they're named similarly.

**Version 12.3 / 2018-11-05**

* Changed the venue indexes to support the new Thunderhead Savanna.

**Version 12.2 / 2018-08-26**

Smaller adjustments:
* Added instantEliminate functionality. This will make some battles move faster (for festival grinding scenarios)
    * instantEliminate sets all foe HP threshholds to 1
    * If a foe has an HP threshhold of 1, isHpLow() always returns true, indicating that the foe can be immediately Eliminated (instead of scratch -> eliminate). This does not apply to the Unit base class or Dragon class.
    * Old Foe behavior should still be in place. That is, if a foe has an HP threshhold that's not 1, then the dragon uses Eliminate only when the foe's HP is below the thresshold.
* Removed the "press enter" from the start of the program.

**Version 12.1 / 2018-08-16**

This update focuses on smaller adjustments:
* Improved the "is dragon weak" battle ending scenario
    * Old: Triggers the refresh if one grinder has HP below threshhold
    * New: Triggers the refresh only if *all* grinders have HP below threshhold. 
    * While this won't make battles move any faster, it will not trigger the refresh as often, continuing the streak and making levelup progress faster
    * Adjusted Dragon default threshhold to compensate (.1 -> .25)
    * Renamed: isDragonWeak() -> areDragonsWeak()
* Adjusted the captcha check/small QoL improvement
    * Old: Required the user to solve the captcha, focus on program window, hit enter to proceed, refocus on battle window
    * New: Program continues to scan for foes if none are found. Thus, after solving captcha, program automatically rescans for foes; no need to manually resume program. 
* Changed timing on the main menu (After clicking the "next page" button, wait 5 seconds -> wait 3 seconds)

**Version 12 / 2018-08-12**

* **"Fast mode" added.** FR's coliseum has a static layout, so buttons will maintain location. Therefore, it's possible to precompute the general location of all these buttons, instead of searching for them.
     * Focuses on one feature, then extrapolates other button regions from the one feature's location. (Currently the feature is the "monster battle" button.)
    * The idea is to restrict the "locateOnScreen"/"locateAllOnScreen" search areas to smaller regions, instead of the entire screen (which is slower).
    * This was partially implemented in v12 by reusing the fightOnButton coordinates. Now _many_ relevant coordinates are reused.
    * May not retrieve _exact_ location of button, but close enough (a 200x200 region instead of 1920x1080).
    * Eliminates searching the entire screen for foe MP bars, captcha text, and fightOn button (overall savings of 10 seconds at the start of each battle)
* Functions rewritten to be compatible with fast mode, both enabled and disabled. (Functions now read from a dictionary of button coordinates, where some locations can be set to None, instead of only taking a single parameter  for coordinates)
* Time for animations to finish decreased to .25 seconds (from 1 second)
* misc text fixes

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
