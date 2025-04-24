from utils import *

with open("fishdata.json", "r") as file:
    fish_data = json.load(file)



class Fish:
    rarityScale = {
        1: "Ultra Rare",
        2: "Very Rare",
        3: "Rare",
        4: "Somewhat Rare",
        5: "Uncommon",
        6: "Moderate",
        7: "Frequent",
        8: "Common",
        9: "Very Common",
    }

    def __init__(self, fish, dict=None):
        if dict == None:
            self.fishData = fish_data[fish]
            self.fishType = fish.replace("_", " ").title()
            self.weight = random.randint(1,int(self.fishData["max weight"]))
        else:
            self.fishData = dict["fishData"]
            self.fishType = dict["fishType"]
            self.weight = dict["weight"]
        self.imageStr = "images/inventory_fish/" + self.fishData["image"]
        self.image = pygame.transform.scale_by(pygame.image.load(self.imageStr), 3)
        self.rarity = Fish.rarityScale[self.fishData["rarity"]]
        self.value = self.fishData["price per pound"] * self.weight

    def render(self, screen, pos):
        screen.blit(pygame.transform.scale_by(self.image, GameData.scaleFactor), (pos[0]*GameData.scaleFactor, pos[1]*GameData.scaleFactor))

    def update(self):
        pass

    def convertToDict(self):
        return {
            "fishData" : self.fishData,
            "fishType" : self.fishType,
            "weight": self.weight
        }



