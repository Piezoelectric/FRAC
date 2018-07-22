import pyautogui

#==============================================================================#
#    NOTES

#Pixel Coordinates (Locs) are a 4-tuple of (left, top, width, height) like gimp
#(0,0) is the top-left corner. X grows to the right, Y grows down.

#The backdrop of HP bars varies because of gradients and other things;
#However the bright green of "has HP there"
#is much different from the dark background
#The other (Red, Blue) colors vary ~20 points but are too close to call

#Apply similar principle to dragon MP bar,
#But with Blue instead of green
#==============================================================================#

#Private class, should never be used by actual things
class Unit:
    def __init__(self, hpLoc=(0,0,0,0), mpLoc = (0,0,0,0), threshhold = .5):
        self.hpLoc = hpLoc #Location of HP bar
        self.mpLoc = mpLoc #Location of MP bar
        self.threshhold = threshhold #Threshhold of "low health"

    def isHpLow(self):
        img = pyautogui.screenshot(region=self.hpLoc)
        pixelLoc = (int(self.hpLoc[2]*self.threshhold), int(self.hpLoc[3]/2))
        #Threshhold% of the width of the HPbar, 50% of the height

        pixel = img.getpixel(pixelLoc) #tuple of (R,G,B, addtl. args..., ...)
        return (pixel[1] < 150)

class Foe(Unit):
    def __init__(self, hpLoc=(0,0,0,0), mpLoc = (0,0,0,0),
                 threshhold = .95, posKey = None):
        super().__init__(hpLoc, mpLoc, threshhold)
        self.posKey = posKey #positional keybind of enemy
    def isAlive(self):
        #if foeMP not found in known foeMP coordinates, unit is dead;
        #img is None
        img = pyautogui.locateOnScreen("foeMP.png", region=self.mpLoc)
        return bool(img)

class Dragon(Unit):
    def __init__(self, hpLoc=(0,0,0,0), mpLoc = (0,0,0,0),
                 threshhold = .1, role = None, elimKey = None):
        super().__init__(hpLoc, mpLoc, threshhold)
        self.role = role #Role, grinder trainee other
        self.elimKey = elimKey #keybind assigned to Eliminate

    def __str__(self):
        return ("HPLoc: " + str(self.hpLoc) + "\n"
                + "MPLoc: " + str(self.mpLoc) + "\n"
                + "threshhold: " + str(self.threshhold) + "\n"
                + "role: " + str(self.role) + "\n"
                + "elimKey" + str(self.elimKey))

    def isElimReady(self):
        img = pyautogui.screenshot(region=self.mpLoc)
        pixelLoc = (int(self.mpLoc[2]*(35/120)), int(self.mpLoc[3]/2))
        #35MP/120maxMP needed for eliminate

        pixel = img.getpixel(pixelLoc)
        return (pixel[2] > 100)
