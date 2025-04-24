from fishes import *


class WaterBody:
    def __init__(self, rects, name, price):
        self.rects = rects
        self.name = name
        self.locked = True
        self.price = price
        self.lock = pygame.transform.scale_by(pygame.image.load("images/uiElements/lock.png"), 4)
        self.getRectCenter()
        self.text = Text(self.name, 10, self.rectCenter, True)

    def getRectCenter(self):
        self.rectCenter = [0,0]
        self.rectCenter[0] = self.rects[0].x + (self.rects[-1].right - self.rects[0].left)/2
        self.rectCenter[1] = self.rects[0].y + (self.rects[-1].bottom - self.rects[0].top)/2

    def render(self, screen):
        if self.locked:
            screen.blit(pygame.transform.scale_by(self.lock, GameData.scaleFactor), ((self.rectCenter[0] - self.lock.get_width()/2)*GameData.scaleFactor, (self.rectCenter[1] - self.lock.get_height()/2)*GameData.scaleFactor))
        if self.checkMouseOver():
            self.text.render(screen)

    def update(self):
        pass

    def checkMouseOver(self):
        for rect in self.rects:
            tempRect = pygame.Rect(rect.x*GameData.scaleFactor, rect.y*GameData.scaleFactor, rect.w*GameData.scaleFactor, rect.h*GameData.scaleFactor)
            if tempRect.collidepoint(pygame.mouse.get_pos()):
                return True

    def handleInput(self, events):
        for event in events:
            pass



waterbodies = {
    "Crystal Glade Lake": WaterBody([pygame.Rect(345,155, 100,70)], "Crystal Glade Lake", 0),
    "Silverfin Lake": WaterBody([pygame.Rect(560,185, 35,35), pygame.Rect(590,200, 40,30)], "Silverfin Lake", 300),
    "Willowshade Pond": WaterBody([pygame.Rect(285,300,40,30)], "Willowshade Pond", 700),
    "Blackwater River": WaterBody([pygame.Rect(495, 170, 25, 90)], "Blackwater River", 850),
    "Stoneflow Creek": WaterBody([pygame.Rect(560, 270, 60,10)], "Stoneflow Creek", 1000),
    "Deepwood Stream": WaterBody([pygame.Rect(505, 375, 60,20)], "Deepwood Stream", 1500),
    "Ebon Depths": WaterBody([pygame.Rect(200, 480, 60,60)], "Ebon Depths", 1650),
    "Ghostwater Reef": WaterBody([pygame.Rect(750, 155, 50,70)], "Ghostwater Reef", 1900),
    "Blackfin Gulf": WaterBody([pygame.Rect(280, 370, 60,35)], "Blackfin Gulf", 2000),
    "Driftwood Bay": WaterBody([pygame.Rect(220, 185, 50,65)], "Driftwood Bay", 2500),
    "Coralmoon Bay": WaterBody([pygame.Rect(620, 510, 60,35)], "Coralmoon Bay", 3500),
    "Serpent's Delta": WaterBody([pygame.Rect(420, 340, 60,50)], "Serpent's Delta", 5000),
    "Moonwillow Lake": WaterBody([pygame.Rect(360, 415, 55,45)], "Moonwillow Lake", 8000),
    "Lilyveil Pond": WaterBody([pygame.Rect(535, 425, 35,35)], "Lilyveil Pond", 12000),
    "Owlsong Pond": WaterBody([pygame.Rect(675, 405, 50,35)], "Owlsong Pond", 20000),
    "Shadefen Lake": WaterBody([pygame.Rect(605, 325, 70,50)], "Shadefen Lake", 30000),
}



for body in GameData.watersUnlocked:
    waterbodies[body].locked = False

