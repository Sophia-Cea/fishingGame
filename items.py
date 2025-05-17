from waters import *

class Boat:
    def __init__(self):
        self.boats = [
            pygame.transform.scale_by(pygame.image.load("images/boat.png"), 4),
        ]
        self.image = self.boats[0]
        self.rect = pygame.Rect(10,180, self.image.get_width()*.6, self.image.get_height()*.8)
        self.casting = False
        self.water = waterObjects["Crystal Glade Lake"]
        self.inventory = []
        if len(GameData.boatInventory) > 0:
            for fish in GameData.boatInventory:
                self.inventory.append(Fish(None, fish))

        self.angle = 0
        self.oscillationMarker = 0
        self.probabilityOfIdleCatch = 100

        self.boatWater = pygame.Surface((400, 60))
        if time == "Day":
            self.boatWater.fill(self.water.waterColorDay)
        else:
            self.boatWater.fill(self.water.waterColorNight)
        
        self.bubbleColor = self.water.currentSplashColor

        self.bubbles = []
        for i in range(200):
            self.bubbles.append(Bubble(self.bubbleColor))

        self.reelpath = [
            (440, 339), 
            (441, 341), 
            (441, 342), 
            (441, 343), 
            (441, 344), 
            (441, 344), 
            (441, 344), 
            (441, 345), 
            (441, 347), 
            (441, 348), 
            (441, 349), 
            (441, 349), 
            (441, 350), 
            (441, 351), 
            (441, 352), 
            (441, 352), 
            (441, 352), 
            (441, 352), 
            (441, 352), 
            (441, 351), 
            (440, 349), 
            (440, 348), 
            (440, 348), 
            (439, 348), 
            (439, 348), 
            (439, 348), 
            (438, 347), 
            (438, 346), 
            (437, 346), 
            (436, 345), 
            (434, 344), 
            (432, 342), 
            (432, 342), 
            (432, 342), 
            (432, 342), 
            (432, 341), 
            (431, 339), 
            (431, 337), 
            (431, 336), 
            (430, 334), 
            (429, 332), 
            (428, 331), 
            (427, 329), 
            (427, 329), 
            (427, 329), 
            (427, 329), 
            (427, 329), 
            (427, 328), 
            (428, 328), 
            (428, 327), 
            (429, 327), 
            (429, 326), 
            (430, 326), 
            (430, 326), 
            (431, 326), 
            (431, 325), 
            (431, 325), 
            (432, 324), 
            (432, 323), 
            (433, 322), 
            (433, 321), 
            (433, 321), 
            (433, 321), 
            (433, 321), 
            (434, 320), 
            (434, 320), 
            (434, 319), 
            (434, 319), 
            (434, 319), 
            (434, 319), 
            (434, 319), 
            (434, 319), 
            (434, 318), 
            (434, 318), 
            (435, 317), 
            (435, 317), 
            (435, 317), 
            (435, 317), 
            (435, 318), 
            (435, 319), 
            (435, 319), 
            (435, 319), 
            (435, 319), 
            (435, 319), 
            (435, 319), 
            (435, 319), 
            (435, 320), 
            (435, 321), 
            (435, 322), 
            (435, 322), 
            (435, 323), 
            (435, 323), 
            (435, 324), 
            (435, 326), 
            (435, 328), 
            (435, 330), 
            (436, 332), 
            (436, 334), 
            (437, 337), 
            (438, 338),
            (440, 339)
        ]

        self.reelLocation = self.reelpath[0]

        self.lines = [
            CastingLineFull(self.reelLocation, (750,420), 350, self.bubbleColor,0), 
            CastingLineFull(self.reelLocation, (690,470), 320, self.bubbleColor,1),
            CastingLineFull(self.reelLocation, (660,370),240, self.bubbleColor,2),
            CastingLineFull(self.reelLocation, (630,520),310, self.bubbleColor,3),
        ]


    def render(self, screen):
        screen.blit(pygame.transform.rotate(self.image, self.angle), (self.rect.x, self.rect.y))

        screen.blit(self.boatWater, (40,465))
        for bubble in self.bubbles:
            bubble.render(screen)
        
        for i, line in enumerate(GameData.lines):
            if line["locked"] == False:
                self.lines[i].render(screen)
            

    def update(self):
        GameData.inventoryCapacity = GameData.upgradeData["upgradables"]["inventory capacity"]["current value"]
        GameData.freshPenCapacity = GameData.upgradeData["upgradables"]["holding pen capacity fresh"]["current value"]
        GameData.brackishPenCapacity = GameData.upgradeData["upgradables"]["holding pen capacity brackish"]["current value"]
        GameData.saltPenCapacity = GameData.upgradeData["upgradables"]["holding pen capacity salt"]["current value"]
        self.inventoryCapacity = GameData.inventoryCapacity
        self.rect.y = 180 + 8*math.sin(self.oscillationMarker/80)
        self.rect.x = 10 + 4*math.cos(self.oscillationMarker/80)
        self.angle = 2.5 * -math.sin(self.oscillationMarker/80 + math.pi/4)

        self.oscillationMarker += 1
        self.oscillationMarker = self.oscillationMarker%503

        self.reelLocation = self.reelpath[int(self.oscillationMarker//(503//(len(self.reelpath)-5)))]


        for bubble in self.bubbles:
            bubble.update()

        for i in range(len(GameData.lines)):
            self.lines[i].update(self.reelLocation)

        willCatch = random.randint(1,100)
        if willCatch == 1:
            i = random.randint(0,3)
            if GameData.lines[i]["locked"] == False and self.lines[i].casting:
                if GameData.lines[i]["bait"] != None and GameData.lines[i]["hook"] != None:
                    self.lines[i].splash()
                    baitGotEaten = random.randint(1,50)
                    if baitGotEaten == 1:
                        self.lines[i].bait = None
                        GameData.lines[i]["bait"] = None


    def handleInput(self, events):
        pass

    def checkClickedOn(self, pos):
        tempRect = pygame.Rect(self.rect.x*GameData.scaleFactor+GameData.fullscreenOffset, self.rect.y*GameData.scaleFactor, self.rect.w*GameData.scaleFactor, self.rect.h*GameData.scaleFactor)
        return tempRect.collidepoint(pos)
    
    def catchAFish(self, lineIndex):
        if len(self.inventory) < self.inventoryCapacity:
            self.inventory.append(Fish(random.choices(self.water.fish, weights=self.water.fishWeights, k=1)[0]))
            GameData.boatInventory.append(self.inventory[-1].convertToDict())
        
class CastingLineFull:
    def __init__(self, startPt, endPt, stringLen, bubbleColor, index):
        self.index = index
        self.line = CastingLine(startPt, endPt, stringLen)
        self.bubbleColor = bubbleColor
        self.animation = None
        self.animationLocation = endPt
        self.playingAnimation = False
        self.casting = True
        self.bait = GameData.lines[index]["bait"]
        self.hook = GameData.lines[index]["hook"]

    def render(self, screen):
        if self.playingAnimation:
            self.animation.render(screen)

        if self.casting:
            self.line.render(screen)

    def update(self, reelLocation):
        if self.casting:
            self.line.update(reelLocation)
        if self.playingAnimation:
            self.animation.update()
            if self.animation.isFinished:
                self.playingAnimation = False
                self.animation = None

    def handleInput(self, events):
        pass

    
    def splash(self):
        self.playingAnimation = True
        self.animation = SplashAnimation(self.animationLocation, self.bubbleColor)



class Bubble:
    def __init__(self, color):
        self.color = color
        self.startY = 465
        self.pos = [random.randint(100,380), self.startY]
        self.radius = 1
        self.speed = random.randint(-10,10)/7
        self.amplitude = random.randint(2,5)
        self.radSpeed = random.randint(1,10)/20
        self.oscillationCounter = 0

    def render(self, screen):
        pygame.draw.circle(screen, self.color, (self.pos[0], self.pos[1]), int(self.radius))

    def update(self):
        self.pos[0] += self.speed
        self.pos[1] = self.startY + self.amplitude * math.sin(self.oscillationCounter)
        self.radius += self.radSpeed
        
        self.oscillationCounter += .1
        self.oscillationCounter = self.oscillationCounter % math.pi*2

        if self.radius >= 6:
            self.__init__(self.color)

class CastingBar:
    def __init__(self):
        self.castingBar = pygame.transform.scale_by(pygame.image.load("images/uiElements/casting_bar.png"), 5)
        self.rect = pygame.Rect(500-self.castingBar.get_width()/2, 620, self.castingBar.get_width(), self.castingBar.get_height())
        self.positionPercent = 0
        self.position = 0
        self.positionWidth = 5
        self.increasing = False
        self.updating = True
        self.speed = .5
        self.target = 0 
        self.difficulty = 50
        self.targetPercent = random.randint(0,100-int(self.difficulty/3))

    def reset(self):
        self.updating = True
        self.positionPercent = 0
        self.targetPercent = random.randint(0,100-int(self.difficulty/3))

    def checkInTarget(self):
        isInTarget = (self.position >= self.target and self.position <= self.target+self.difficulty-self.positionWidth)
        return isInTarget

    def render(self, screen):
        pygame.draw.rect(screen, (158,217,201), ((self.rect.x+10), (self.rect.y+10), (self.rect.w-10), (self.rect.h-20)))
        pygame.draw.rect(screen, (34,116,119), (self.target, self.rect.y, self.difficulty, self.rect.h))
        pygame.draw.rect(screen, (12,55,72), (self.position, self.rect.y, self.positionWidth, self.rect.h))
        screen.blit(self.castingBar, (self.rect.x, self.rect.y))

    def update(self):
        self.position = self.rect.x + self.rect.w/100 * self.positionPercent
        self.target = self.rect.x + self.rect.w/100 * self.targetPercent

        if self.updating:
            if self.increasing:
                self.positionPercent += self.speed
                if self.positionPercent >= 98:
                    self.increasing = False
            else:
                self.positionPercent -= self.speed
                if self.positionPercent <= 2:
                    self.increasing = True

    def handleInput(self, events):
        pass

class SplashAnimation:
    def __init__(self, startPos, color):
        self.color = color
        self.startPos = startPos
        self.particles = []
        self.particles2 = []
        self.isFinished = False
        self.delayCounter = 5

        self.splashwaves = []
        self.splashwavesCounter = 0

        for i in range(150):
            self.particles.append(SplashParticle(self.startPos, self.color))
            self.particles2.append(SplashParticle(self.startPos, self.color))

    def render(self, screen):
        for particle in self.particles:
            particle.render(screen)

        for particle in self.particles2:
            particle.render(screen)

        for wave in self.splashwaves:
            wave.render(screen)

    def update(self):
        for particle in self.particles:
            particle.update()
            if particle.isFinished:
                self.particles.remove(particle)
        
        if self.delayCounter <= 0:
            for particle in self.particles2:
                particle.update()
                if particle.isFinished:
                    self.particles2.remove(particle)

        if len(self.particles2) == 0 and len(self.particles) == 0 and len(self.splashwaves) == 0:
            self.isFinished = True
        
        if self.delayCounter > 0:
            self.delayCounter -= 1

        if self.splashwavesCounter <= 20:
            if self.splashwavesCounter % 10 == 0:
                self.splashwaves.append(SplashWave(self.color, self.startPos))

        self.splashwavesCounter += 1

        for wave in self.splashwaves:
            wave.update()

        for wave in self.splashwaves:
            if wave.finished:
                self.splashwaves.remove(wave)

class SplashParticle:
    def __init__(self, startPos, color):
        self.color = color
        self.pos = [startPos[0], startPos[1]]
        self.endY = random.randint(startPos[1]+10, startPos[1]+40)
        self.size = random.randint(1,3)
        self.xSpeed = random.randint(-40,40)/10
        self.ySpeed = random.randint(10,50)/5
        self.gravity = -0.5
        self.isFinished = False

    def render(self, screen):
        pygame.draw.circle(screen, self.color, (self.pos[0], self.pos[1]), int(self.size))

    def update(self):
        self.pos[0] += self.xSpeed
        self.pos[1] -= self.ySpeed

        self.ySpeed += self.gravity

        if self.pos[1] > self.endY:
            self.isFinished = True

class SplashWave:
    def __init__(self, color, pos):
        self.rect = pygame.Rect(pos[0], pos[1], 4, 1)
        self.center = pos
        self.color = color
        self.speed = 4
        self.proportion = 4
        self.lineThickness = 1
        self.maxWidth = 150
        self.finished = False

    def render(self, screen):
        pygame.draw.ellipse(screen, self.color, (self.rect.x, self.rect.y, self.rect.w, self.rect.h), int(self.lineThickness))

    def update(self):
        self.rect.w += self.speed
        self.speed -= .05
        self.rect.h = self.rect.w/self.proportion
        self.rect.centerx = self.center[0]
        self.rect.centery = self.center[1]
        self.lineThickness += .1

        if self.rect.w >= self.maxWidth:
            self.finished = True

class CastingLine:
    def __init__(self, startPoint, endPoint, stringLength):
        self.startPoint = startPoint
        self.endPoint = endPoint
        self.numLines = 10
        self.lines = []
        self.refpts = [self.startPoint, self.startPoint, self.endPoint]
        self.bezPts = []
        self.color = (160,165,151)
        self.stringLen = stringLength

    def calculateCurvePoints(self):
        straightDistance = math.sqrt((self.startPoint[0]-self.endPoint[0])**2 + (self.startPoint[1]-self.endPoint[1])**2)
        midpoint = [self.startPoint[0] + (self.endPoint[0] - self.startPoint[0])/2, self.startPoint[1] + (self.endPoint[1] - self.startPoint[1])/2]
        sideLen = self.stringLen/2
        theta = math.acos((2*(sideLen)**2-straightDistance**2)/(2*(sideLen**2)))
        alpha = (math.pi - theta)/2
        ht = math.sqrt((sideLen)**2-(straightDistance/2)**2)

        ang = (math.tan((self.endPoint[1]-self.startPoint[1])/(self.endPoint[0]-self.startPoint[0]))) + math.pi/2
        point = [midpoint[0] + ht*math.cos(ang), midpoint[1] + ht*math.sin(ang)]
        self.refpts[1] = point

    def render(self, screen):
        tempArr = []
        for pt in self.bezPts:
            tempArr.append((pt[0], pt[1]))
        pygame.draw.lines(screen, self.color, False, tempArr, 2)


    def update(self, startPoint):
        self.startPoint = startPoint
        self.refpts[0] = startPoint
        self.calculateCurvePoints()
        self.make_bezier_curve()

    def quadratic_bezier(self, p0, p1, p2, t):
        x = (1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t ** 2 * p2[0]
        y = (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t ** 2 * p2[1]
        return (int(x), int(y))

    def make_bezier_curve(self):
        p0 = self.refpts[0]
        p1 = self.refpts[1]
        p2 = self.refpts[2]
        num_points = 50
        self.bezPts = [self.quadratic_bezier(p0, p1, p2, t / num_points) for t in range(num_points + 1)]


class ShopItem:
    def __init__(self):
        self.background = pygame.transform.scale_by(pygame.image.load("images/uiElements/shop_item.png"), 4)
        self.rect = pygame.Rect(0,0, self.background.get_width(), self.background.get_height())

    def render(self, screen, pos):
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        screen.blit(self.background, (pos[0], pos[1]))

    def checkMouseOver(self):
        pos = pygame.mouse.get_pos()
        return pygame.Rect(self.rect.x*GameData.scaleFactor+GameData.fullscreenOffset, self.rect.y*GameData.scaleFactor, self.rect.w*GameData.scaleFactor, self.rect.h*GameData.scaleFactor).collidepoint(pos)

class UnlockableItem(ShopItem):
    def __init__(self, index):
        super().__init__()
        self.infoDict = GameData.upgradeData["unlockables"][index]
        self.index = index
        self.upgradeTree = self.infoDict["upgrade tree"]
        self.name = self.infoDict["name"]
        self.unlocked = self.infoDict["unlocked"]
        self.level = self.infoDict["level"]
        self.maxedOut = self.level == self.infoDict["max level"]
        if not self.unlocked:
            self.cost = self.infoDict["cost"]
        elif not self.maxedOut:
            self.cost = self.upgradeTree[self.level+1]
        self.image = self.infoDict["image"]
        self.icon = pygame.image.load("images/uiElements/" + self.image)
        self.iconProportion = self.icon.get_width()/self.icon.get_height()
        self.icon = pygame.transform.scale(self.icon, (55*self.iconProportion, 55))
        self.lockIcon = pygame.transform.scale_by(pygame.image.load("images/uiElements/lock.png"), 4)
        self.lockCoords = (self.background.get_width()/2-self.lockIcon.get_width()/2, 20)

        self.nameText = Text(self.name, 10, (self.background.get_width()/2, 75), True, shadow=True)

        if not self.maxedOut:
            self.costText = Text("$" + str(self.cost), 12, (self.background.get_width()/2, 90), True, shadow=True)

        self.background.blit(self.icon, (self.background.get_width()/2-self.icon.get_width()/2, 15))
        self.nameText.render(self.background)
        if not self.maxedOut:
            self.costText.render(self.background)

    def render(self, screen, pos):
        super().render(screen, pos)
        if not self.unlocked:
            screen.blit(self.lockIcon, (pos[0] + self.lockCoords[0], pos[1]+self.lockCoords[1]))
    
    def upgradeItem(self):
        pass

    def resetValsAndText(self):
        pass

class UpgradableItem(ShopItem):
    def __init__(self, infoDict):
        self.dictName = infoDict
        self.resetValuesAndText()
    
    def upgradeItem(self):
        if self.currentLevel < GameData.upgradeData["upgradables"][self.dictName]["max level"]:
            GameData.upgradeData["upgradables"][self.dictName]["current level"] += 1
            GameData.upgradeData["upgradables"][self.dictName]["current value"] = list(self.infoDict["upgrade tree"].values())[self.currentLevel]
            self.resetValuesAndText()

    def resetValuesAndText(self):
        super().__init__()
        self.infoDict = GameData.upgradeData["upgradables"][self.dictName]
        self.name = self.infoDict["name"]
        self.currentValue = self.infoDict["current value"]
        self.currentLevel = self.infoDict["current level"]
        if self.currentLevel < GameData.upgradeData["upgradables"][self.dictName]["max level"]:
            self.cost = list(self.infoDict["upgrade tree"].keys())[self.currentLevel]

        self.nameTexts = []
        if len(self.name) > 10:
            self.name = self.name.split(" ")
            for i, text in enumerate(self.name):
                self.nameTexts.append(Text(text, 11.5, (self.background.get_width()/2, 15+i*15), True, shadow=True))
        else:
            self.nameTexts.append(Text(self.name, 11.5, (self.background.get_width()/2, 25), True, shadow=True))
        
        self.levelText = Text("Level: " + str(self.currentLevel), 10, (self.background.get_width()/2, 70), True, shadow=True)
        if self.currentLevel < GameData.upgradeData["upgradables"][self.dictName]["max level"]:
            self.costText = Text("$" + str(self.cost), 12, (self.background.get_width()/2, 85), True, shadow=True)
        
        for text in self.nameTexts:
            text.render(self.background)
        self.levelText.render(self.background)
        if self.currentLevel < GameData.upgradeData["upgradables"][self.dictName]["max level"]:
            self.costText.render(self.background)

class BuyableItem(ShopItem):
    def __init__(self, infoDict):
        super().__init__()
        self.infoDict = GameData.upgradeData["items"][infoDict]
        self.name = infoDict
        self.numOwned = self.infoDict["num owned"]
        self.cost = self.infoDict["price"]
        self.image = self.infoDict["image"]
        self.icon = pygame.image.load("images/uiElements/" + self.image + ".png")
        self.iconProportion = self.icon.get_width()/self.icon.get_height()
        self.icon = pygame.transform.scale(self.icon, (40*self.iconProportion, 40))
        self.lockIcon = pygame.transform.scale_by(pygame.image.load("images/uiElements/lock.png"), 4)
        self.lockCoords = (self.background.get_width()/2-self.lockIcon.get_width()/2, 20)

        self.nameText = Text(self.name, 12, (self.background.get_width()/2, 60), True, shadow=True)

        self.nameTexts = []
        if len(self.name) > 10:
            self.name = self.name.split(" ")
            if len(self.name) >= 3:
                self.name[0] = self.name[0] + " " + self.name[1]
                self.name.pop(1)
            for i, text in enumerate(self.name):
                self.nameTexts.append(Text(text, 11.5, (self.background.get_width()/2, 50+i*13), True, shadow=True))
        else:
            self.nameTexts.append(Text(self.name, 11.5, (self.background.get_width()/2, 65), True, shadow=True))



        self.numText = Text("Own: " + str(self.numOwned), 10, (self.background.get_width()/2, 81), True, shadow=True)
        self.costText = Text("$" + str(self.cost), 10, (self.background.get_width()/2, 95), True, shadow=True)

        self.background.blit(self.icon, (self.background.get_width()/2-self.icon.get_width()/2, 10))
        for text in self.nameTexts:
            text.render(self.background)
        self.numText.render(self.background)
        self.costText.render(self.background)

    def render(self, screen, pos):
        super().render(screen, pos)
        # if not self.unlocked:
        #     screen.blit(self.lockIcon, (pos[0] + self.lockCoords[0], pos[1]+self.lockCoords[1]))

class ShopLabelButton:
    def __init__(self, name, pos, icon=None):
        self.name = name
        self.icon = pygame.transform.scale_by(pygame.image.load("images/uiElements/" + icon), 5)
        self.background = pygame.transform.scale_by(pygame.image.load("images/uiElements/shop_item.png"), 5)
        self.rect = pygame.Rect(pos[0], pos[1], self.background.get_width(), self.background.get_height())
        self.text = Text(self.name, 16, (self.background.get_width()/2, 95), True, shadow=True)

        self.background.blit(self.icon, (self.background.get_width()/2-self.icon.get_width()/2, 30))
        self.text.render(self.background)

    def render(self, screen):
        screen.blit(self.background, (self.rect.x, self.rect.y))

    def checkMouseOver(self):
        return pygame.Rect(self.rect.x, self.rect.y, self.rect.w, self.rect.h).collidepoint(pygame.mouse.get_pos())


class LineMenu:
    def __init__(self, pos, text, locked, bait=None, hook=None):
        self.locked = locked
        self.image = pygame.transform.scale_by(pygame.image.load("images/uiElements/line_window.png"), 5)
        self.rect = pygame.Rect(pos[0], pos[1], self.image.get_width(), self.image.get_height())
        self.text = Text(text, 15, (self.rect.w/2, 20), centered=True)

        self.bait = pygame.transform.scale_by(pygame.image.load("images/uiElements/corn.png"), 5)
        self.hook = pygame.transform.scale_by(pygame.image.load("images/uiElements/hook_1.png"), 5)

        self.lockImage = pygame.transform.scale_by(pygame.image.load("images/uiElements/lock.png"), 7)

        self.baitBox = pygame.Rect(10, 50, 95,70)
        self.hookBox = pygame.Rect(10, 125,95,70)

        if bait == None:
            self.bait = None
        else:
            self.bait = pygame.transform.scale_by(pygame.image.load("images/uiElements/" + bait + ".png"), 5)

        if hook == None:
            self.hook = None
        else:
            self.hook = pygame.transform.scale_by(pygame.image.load("images/uiElements/hook_" + str(hook) + ".png"), 5)


    def render(self, screen):
        self.text.render(self.image)
        screen.blit(self.image, (self.rect.x, self.rect.y))

        if self.bait != None:
            self.image.blit(self.bait, (self.baitBox.centerx-self.bait.get_width()/2, self.baitBox.centery-self.bait.get_height()/2))

        if self.hook != None:
            self.image.blit(self.hook, (self.hookBox.centerx-self.hook.get_width()/2, self.hookBox.centery-self.hook.get_height()/2))

        if self.locked:
            screen.blit(self.lockImage, (self.rect.centerx-self.lockImage.get_width()/2, self.rect.centery-self.lockImage.get_height()/2))


    def update(self):
        if self.bait != None:
            self.bait.update()

        if self.hook != None:
            self.hook.update()

    def handleInput(self, events):
        if self.bait != None:
            self.bait.handleInput(events)

        if self.hook != None:
            self.hook.handleInput(events)


    def checkMouseOver(self):
        pos = pygame.mouse.get_pos()
        return pygame.Rect(self.rect.x, self.rect.y, self.rect.w, self.rect.h).collidepoint(pos)
    
class DragAndDropItem:
    def __init__(self, image, pos):
        self.imageName = image
        # self.image = pygame.transform.scale_by(pygame.image.load("images/uiElements/" + str(image) + ".png"), 5)
        self.rect = pygame.Rect(pos[0]-self.image.get_width()/2, pos[1]-self.image.get_height()/2, self.image.get_width(), self.image.get_height())
        self.dragging = False
        self.draggingOffset = [0,0]

    def render(self, screen, pos=None):
        if not self.dragging:
            if pos == None:
                screen.blit(self.image, (self.rect.x, self.rect.y))
            else:
                screen.blit(self.image, (pos[0], pos[1]))
                self.rect.x = pos[0]
                self.rect.y = pos[1]
        else:
            mousePos = pygame.mouse.get_pos()
            screen.blit(self.image, (mousePos[0]-self.draggingOffset[0], mousePos[1]-self.draggingOffset[1]))

    def update(self):
        pass

    def handleInput(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if self.checkMouseOver():
                    self.dragging = True
                    self.draggingOffset = [pos[0]-self.rect.x, pos[1]-self.rect.y]

    def checkMouseOver(self):
        pos = pygame.mouse.get_pos()
        return pygame.Rect(self.rect.x, self.rect.y, self.rect.w, self.rect.h).collidepoint(pos)
    
    def checkInRect(self, rect):
        if self.rect.left > rect.left and self.rect.right < rect.right and self.rect.top > rect.top and self.rect.bottom < rect.bottom:
            return True
        return False


class BaitItem(DragAndDropItem):
    def __init__(self, name, pos):
        self.image = pygame.transform.scale_by(pygame.image.load("images/uiElements/" + str(name) + ".png"), 5)
        super().__init__(name, pos)

class HookItem(DragAndDropItem):
    def __init__(self, name, pos):
        self.image = pygame.transform.scale_by(pygame.image.load("images/uiElements/hook_" + str(name) + ".png"), 5)
        super().__init__(name, pos)

class LineControlButton:
    def __init__(self, index):
        self.image = pygame.transform.scale_by(pygame.image.load("images/uiElements/line_panel.png"), 5)
        self.surface = pygame.Surface((self.image.get_width(),self.image.get_height()), pygame.SRCALPHA)
        self.labelText = Text("Line " + str(index+1), 10, (self.image.get_width()/2, 15), True)
        self.statusCastingText = Text("Reel in", 10, (self.image.get_width()/2, 38), True)
        self.statusRestingText = Text("Cast", 10, (self.image.get_width()/2, 38), True)
        self.index = index
        self.casting = True
        self.rect = pygame.Rect(0,0, self.image.get_width(), self.image.get_height())
        self.resetItems()

    def resetItems(self):
        self.baitName = GameData.lines[self.index]["bait"]
        self.hookName = GameData.lines[self.index]["hook"]
        if self.baitName != None:
            self.bait = pygame.image.load("images/uiElements/" + self.baitName + ".png")
            self.bait = pygame.transform.scale_by(self.bait, 20/self.bait.get_width())
        if self.hookName != None:
            self.hook = pygame.image.load("images/uiElements/hook_" + str(self.hookName) + ".png")
            self.hook = pygame.transform.scale_by(self.hook, 20/self.hook.get_width())

    def render(self, screen, pos):
        self.surface.blit(self.image, (0,0))
        self.labelText.render(self.surface)
        if self.casting:
            self.statusCastingText.render(self.surface)
        else:
            self.statusRestingText.render(self.surface)
        
        if self.baitName != None:
            self.surface.blit(self.bait, (43-self.bait.get_width()/2, 73-self.bait.get_height()/2))
        if self.hookName != None:
            self.surface.blit(self.hook, (82-self.hook.get_width()/2, 73-self.hook.get_height()/2))
        
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        screen.blit(self.surface, pos)
    
    def update(self):
        # if self.baitName != GameData.lines[self.index]["bait"]:
        #     self.baitName = GameData.lines[self.index]["bait"]
        #     if self.baitName != None:
        #         self.bait = pygame.transform.scale_by(pygame.image.load("images/uiElements/" + self.baitName + ".png"), 3)
        # if self.hookName != GameData.lines[self.index]["hook"]:
        #     self.hookName = GameData.lines[self.index]["hook"]
        #     if self.hookName != None:
        #         self.hook = pygame.transform.scale_by(pygame.image.load("images/uiElements/hook_" + str(self.hookName) + ".png"), 3)
        if self.baitName != GameData.lines[self.index]["bait"] or self.hookName != GameData.lines[self.index]["hook"]:
            self.resetItems()
       
    
    def checkMouseOver(self):
        pos = pygame.mouse.get_pos()
        return self.rect.collidepoint(pos)






boat = Boat()

