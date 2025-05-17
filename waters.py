from waterextras import *


with open("data.json", "r") as file:
    water_data = json.load(file)



# Waters

class Water:
    def __init__(self):
        self.water = water_data[self.water]
        self.fish = self.water["fish"]
        self.fishWeights = []
        self.currentSplashColor = None
        self.waterRect = pygame.Rect(0, 330, WIDTH, HEIGHT-330+5)
        total = 0
        self.fishWeights = []

        if self.water["backgroundImg"] == None:
            self.background = None
        else:
            self.background = pygame.transform.scale_by(pygame.image.load("images/lakeBackgrounds/" + self.water["backgroundImg"]), 4)
        self.waterColorDay = self.water["waterColorDay"]
        self.waterColorNight = self.water["waterColorNight"]
        self.splashColorDay = self.water["splashColorDay"]
        self.splashColorNight = self.water["splashColorNight"]

        if time == "Day":
            self.currentSplashColor = self.splashColorDay
        else: 
            self.currentSplashColor = self.splashColorDay

        for fish in self.fish:
            total += fish_data[fish]["rarity"]
            self.fishWeights.append(fish_data[fish]["rarity"])
        
        for i in range(len(self.fishWeights)):
            self.fishWeights[i] = self.fishWeights[i]/total


    def render(self, screen):
        if self.background != None:
            screen.blit(self.background, (0,0))

        if time == "Day":
            pygame.draw.rect(screen, self.waterColorDay, (self.waterRect.x, self.waterRect.y, self.waterRect.w, self.waterRect.h))
        else: 
            pygame.draw.rect(screen, self.waterColorNight, (self.waterRect.x, self.waterRect.y, self.waterRect.w, self.waterRect.h))

    def update(self):
        pass

    def handleInput(self, events):
        pass


class CrystalGladeLake(Water):
    def __init__(self):
        self.water = "Crystal Glade Lake"
        super().__init__()

class SilverfinLake(Water):
    def __init__(self):
        self.water = "Silverfin Lake"
        super().__init__()

class WillowshadePond(Water):
    def __init__(self):
        self.water = "Willowshade Pond"
        super().__init__()

class BlackwaterRiver(Water):
    def __init__(self):
        self.water = "Blackwater River"
        super().__init__()

class StoneflowCreek(Water):
    def __init__(self):
        self.water = "Stoneflow Creek"
        super().__init__()

class DeepwoodStream(Water):
    def __init__(self):
        self.water = "Deepwood Stream"
        super().__init__()

class EbonDepths(Water):
    def __init__(self):
        self.water = "Ebon Depths"
        super().__init__()

class GhostwaterReef(Water):
    def __init__(self):
        self.water = "Ghostwater Reef"
        super().__init__()

class BlackfinGulf(Water):
    def __init__(self):
        self.water = "Blackfin Gulf"
        super().__init__()

class DriftwoodBay(Water):
    def __init__(self):
        self.water = "Driftwood Bay"
        super().__init__()

class CoralmoonBay(Water):
    def __init__(self):
        self.water = "Coralmoon Bay"
        super().__init__()

class SerpentsDelta(Water):
    def __init__(self):
        self.water = "Serpent's Delta"
        super().__init__()

class ThornrushCreek(Water):
    def __init__(self):
        self.water = "Thornrush Creek"
        super().__init__()

class LilyveilPond(Water):
    def __init__(self):
        self.water = "Lilyveil Pond"
        super().__init__()

class MoonwillowLake(Water):
    def __init__(self):
        self.water = "Moonwillow Lake"
        super().__init__()


class FoxbriarCreek(Water):
    def __init__(self):
        self.water = "Foxbriar Creek"
        super().__init__()

class OwlsongPond(Water):
    def __init__(self):
        self.water = "Owlsong Pond"
        super().__init__()

class ShadefenLake(Water):
    def __init__(self):
        self.water = "Shadefen Lake"
        super().__init__()



waterObjects = {
    "Crystal Glade Lake" : CrystalGladeLake(),
    "Silverfin Lake" : SilverfinLake(),
    "Willowshade Pond" : WillowshadePond(),
    "Blackwater River" : BlackwaterRiver(),
    "Stoneflow Creek" : StoneflowCreek(),
    "Deepwood Stream" : DeepwoodStream(),
    "Ebon Depths" : EbonDepths(),
    "Ghostwater Reef" : GhostwaterReef(),
    "Blackfin Gulf" : BlackfinGulf(),
    "Driftwood Bay" : DriftwoodBay(),
    "Coralmoon Bay" : CoralmoonBay(),
    "Serpent's Delta" : SerpentsDelta(),
    "Thornrush Creek" : ThornrushCreek(),
    "Lilyveil Pond" : LilyveilPond(),
    "Moonwillow Lake" : MoonwillowLake(),
    "Foxbriar Creek" : FoxbriarCreek(),
    "Owlsong Pond" : OwlsongPond(),
    "Shadefen Lake" : ShadefenLake(),

}


