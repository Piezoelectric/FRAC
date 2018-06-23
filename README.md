# FRAutoColi

Python script which automates the process of playing/grinding the Flight Rising coliseum. Uses `PyAutoGUI` to take screenshots of the current screen, locate buttons, and analyze HP values.

Only tested in Python3 on a windows 7 machine, firefox quantum. In practice OS and browser shouldn't matter too much, as all you really need is to take screenshots. PyAutoGUI works on linux, mac, and windows. I don't know if PyAutoGUI works in Python2.

`AutoColi.py` contains the main battle logic. `Battle.py` contains helper functions. `Units.py` contains the classes Foe and Dragon. 

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

# Usage

Get some level 25 dragons. I don't know or care how.

In `AutoColi.py`, find the following lines:

```
configDragons = [
    ["grinder", "s"],
    ["grinder", "s"],
    ["trainee", None]
    ]
```

This defines your dragons (from top to bottom on the battle screen). Change role between "grinder" and "trainee". The second parameter is the dragon's hotkey for Eliminate. Trainees should not set an Eliminate hotkey. 

Teplace each of the images in the directory with a screenshot from _your_ browser. The screenshots included in the repo are only examples. They were taken on a Windows 7 laptop, Firefox Quantum, at 80% zoom level. They may not look the same across browsers or machines.

Invoke `python3 AutoColi.py` to start the script. Ideally you should split-screen so that your battle window and your Python window are both visible.

Note that Coliseum captchas are not automatically solved. Upon seeing a captcha, the script will pause to wait for you to solve it. You'll need to manually intervene every 10 or so battles. But hey, it's much better than manually doing all 10 battles.

# Why?

Sometimes I see people on the forums say "Coli grinding isn't so bad, I usually watch netflix/listen to podcasts while I do it". When your game is so dull you have to come up with alternate ways to entertain yourself while playing the game ... it's not really worth the time and energy.
