# About

Automates the Coliseum. What coliseum? That's for you to figure out. 

If you appreciate the program, feel free to donate at (a paypal link I didn't make yet).

**Captchas are not automatic yet.** I am still working on this.

# Usage

Short version: `py -m AutoColi --venueIndex 1`

## Detailed instructions

Set up the Coliseum to enable keyboard hotkeys, and disable animations and visual effects.

Set your browser zoom level so the game displays with no blurriness or aliasing, and you don't need to scroll to find it. You can use GG to help adjust; the GG window should be 700 pixels wide, 600 px tall.

If stuff isn't working, try replacing each of the images in the directory with a screenshot from _your_ browser. 

Open a game window, then run the program. The game should either be at the main menu (with "Monster Battle" visible), or on a battle end screen (with the "Fight On" button visible). 

## Configuration

In `config.yml` you'll find the following:

```
dragons:
    - dragonInfo:
        role: grinder
        scratch: e
        eliminate: s
    - dragonInfo:
        role: grinder
        scratch: e
        eliminate: s
    - dragonInfo:
        role: grinder
        scratch: e
        eliminate: s
captchaLogging: true
fastMode: true
numBattlesDefault: 50
battleLogic: SpamLogic
eliminateThreshold: 1
```

Some fields can be passed in at the command line. The priority for configuration is

1) Command line arguments
2) `config.yml`
3) system defaults

| Field | Description |
| --- | --- |
| `venueIndex` | **Must be specified at command line.** An integer specifying which Venue to battle in. Specify using `--venueIndex 1`. | 
| `dragonInfo` | **Must be configured in `config.yml`** (no command line specification). Corresponds to each of your dragons. The order of your team in the Coliseum, top to bottom, should also be the order of your team in the `yml` file. | 
| `captchaLogging` | If set to `true`, enables right-click saving captchas to disk. Captcha logging will be useful for another project. 
| `fastMode` | If enabled, extrapolates button coordinates using fancy geometry math. If disables, takes a screenshot and finds the button manually each time, which is safer but takes longer. Defaults to true.|
| `numBattlesDefault` | The number of battles to perform. **Can be overridden from command line** argument `--numBattles ##`. If not specified in `config.yml`, defaults to 5.
| `battleLogic` | Determines which coliseum logic module to use. Currently the only logic supported is `SpamLogic`. 
| `eliminateThreshhold` | The threshold at which Eliminate will refund MP. If not set, default to 1. |
