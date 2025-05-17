from items import *

class StateManager:
    def __init__(self) -> None:
        self.queue = []

    def push(self, page):
        self.queue.append(page)
        # page.onEnter()

    def pop(self):
        self.queue[len(self.queue)-1].onExit()
        self.queue.pop(len(self.queue)-1)

    def run(self, surface, events):
        self.queue[len(self.queue)-1].update()
        for state in self.queue:
            state.render(surface)
        self.queue[len(self.queue)-1].handleInput(events)

stateManager = StateManager()

class State:
    def __init__(self) -> None:
        pass

    def onEnter(self):
        pass

    def onExit(self):
        pass

    def render(self, screen):
        pass

    def update(self):
        pass

    def handleInput(self, events):
        pass

# Boat section states

class BoatState(State):
    def __init__(self):
        super().__init__()
        self.castingBar = CastingBar()
        self.caughtAFish = False
        self.moneyBox = pygame.transform.scale_by(pygame.image.load("images/uiElements/money_box.png"), 6)
        self.menuButton = Button((900,20), image="pause_button.png")
        self.moneyText = Text("$" + str(GameData.money), 20, (35,45))

        self.lineButtons = []
        for i in range(4):
            if GameData.lines[i]["locked"] == False:
                self.lineButtons.append(LineControlButton(i))


    def render(self, screen):
        super().render(screen)
        screen.blit(sky, (0,0))
        boat.water.render(screen)
        boat.render(screen)
        self.menuButton.render(screen)

        spacing = 20
        margin = (1000 - (len(self.lineButtons) * (self.lineButtons[0].rect.w + spacing)))/2

        for i, button in enumerate(self.lineButtons):
            button.render(screen, (margin+i*(button.rect.w+spacing), 600))

        screen.blit(self.moneyBox, (20,20))
        self.moneyText.render(screen)

        if boat.casting:
            self.castingBar.render(screen)

        


    def update(self):
        super().update()
        boat.update()
        boat.water.update()

        # print(GameData.inventoryCapacity)

        GameData.money = round(GameData.money, 2)
        self.moneyText = Text("$" + str(GameData.money), 20, (35,45))

        if boat.casting:
            self.castingBar.update()

        for button in self.lineButtons:
            button.update()

        num = 0
        for i in range(4):
            if GameData.lines[i]["locked"] == False:
                num += 1
        
        if num != len(self.lineButtons):
            self.lineButtons = []
            for i in range(4):
                if GameData.lines[i]["locked"] == False:
                    self.lineButtons.append(LineControlButton(i))

            


    def handleInput(self, events):
        super().handleInput(events)
        boat.handleInput(events)
        boat.water.handleInput(events)
        for event in events:
            if event.type == pygame.MOUSEBUTTONUP:
                mousePos = pygame.mouse.get_pos()
                if boat.checkClickedOn(mousePos):
                    stateManager.push(BoatInventoryState())
                elif self.menuButton.checkMouseOver(mousePos):
                    stateManager.push(MainMenuState())
                
                for i, button in enumerate(self.lineButtons):
                    if button.checkMouseOver():
                        if boat.lines[i].casting and boat.lines[i].playingAnimation:
                            boat.catchAFish(i)
                        button.casting = not button.casting
                        boat.lines[i].casting = button.casting


            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    if boat.casting:
                        if self.castingBar.updating == True:
                            self.castingBar.updating = False
                            if self.castingBar.checkInTarget():
                                boat.catchAFish()
                            self.castingBar.reset()
                if event.key == pygame.K_m:
                    stateManager.push(MainMenuState())

class MainMenuState(State):
    def __init__(self):
        super().__init__()
        self.surface = pygame.transform.scale_by(pygame.image.load("images/uiElements/main_menu.png"), 5)
        self.xButton = Button((150,100), image="x_button.png")
        self.aquariumButton = Button((300,300), "Aquarium")
        self.mapButton = Button((500,300), "Map")
        self.inventoryButton = Button((300,400), "Inventory",)
        self.shopButton = Button((500,400), "Shop")

        self.moneyBox = pygame.transform.scale_by(pygame.image.load("images/uiElements/money_box.png"), 6)
        self.moneyText = Text("$" + str(GameData.money), 20, (35,45))

        self.lockedImage = pygame.transform.scale_by(pygame.image.load("images/uiElements/lock.png"), 6)

        self.buttons = [self.aquariumButton, self.mapButton, self.xButton, self.inventoryButton, self.shopButton]
        self.titleText = Text("Main Menu", 40, (500,200), True, shadow=True)
        self.backgroundCoords = (500 - self.surface.get_width()/2, 350-self.surface.get_height()/2)

    def render(self, screen):
        super().render(screen)
        screen.blit(self.surface, (self.backgroundCoords[0], self.backgroundCoords[1]))
        self.titleText.render(screen)

        screen.blit(self.moneyBox, (20, 20))
        self.moneyText.render(screen)

        for button in self.buttons:
            button.render(screen)

        if GameData.aquariumLocked:
            screen.blit(self.lockedImage, (365, 305))


    def update(self):
        super().update()
        self.moneyText = Text("$" + str(GameData.money), 20, (35,45))
        
    def handleInput(self, events):
        super().handleInput(events)
        for event in events:
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_q:
                    stateManager.pop()

            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                if self.aquariumButton.checkMouseOver(pos):
                    if GameData.aquariumLocked:
                        if GameData.money > GameData.unlockAquariumCost:
                            GameData.money -= GameData.unlockAquariumCost
                            GameData.aquariumLocked = False
                    else:
                        pass
                
                if self.mapButton.checkMouseOver(pos):
                    stateManager.push(MapMenuState())
                if self.xButton.checkMouseOver(pos):
                    stateManager.pop()
                if self.inventoryButton.checkMouseOver(pos):
                    stateManager.push(BoatInventoryState())
                if self.shopButton.checkMouseOver(pos):
                    stateManager.push(ShopState())

class FishMenuState(State):
    def __init__(self, fish):
        super().__init__()
        self.xButton = Button((280,40), image="x_button.png")
        self.background = pygame.transform.scale_by(pygame.image.load("images/uiElements/fish_menu.png"), 5)
        self.fish = fish
        self.value = fish.value
        self.titles = []
        self.fishName = self.fish.fishType
        if len(self.fishName) >= 10:
            self.fishName = self.fishName.split(" ")
            for i in range(len(self.fishName)):
                self.titles.append(Text(self.fishName[i], 30, (500,145 + i*55), True, shadow=True))
        else:
            self.titles.append(Text(self.fish.fishType, 30, (500,160), True, shadow=True))

        self.rarityText = Text("Rarity: " + fish.rarity, 15, (350,260), shadow=True)
        self.weightText = Text("Size: " + str(fish.weight) + " lbs", 15, (350,295), shadow=True)
        self.valueText = Text("Value: $" + str(fish.value), 15, (350,330), shadow=True)
        self.backgroundCoords = (500-self.background.get_width()/2, 350-self.background.get_height()/2)

        self.texts = [self.rarityText, self.weightText, self.valueText]
        self.sellButton = Button((410,400), "Sell")
        self.keepButton = Button((410,480), "Keep")

    def render(self, screen):
        screen.blit(self.background, (self.backgroundCoords[0], self.backgroundCoords[1]))
        
        for text in self.titles:
            text.render(screen) 
        
        for text in self.texts:
            text.render(screen)
        
        self.xButton.render(screen)
        self.sellButton.render(screen)
        self.keepButton.render(screen)

    def update(self):
        GameData.money = round(GameData.money, 2)

    def handleInput(self, events):
        super().handleInput(events)
        for event in events:
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                if self.xButton.checkMouseOver(pos):
                    stateManager.pop()
                
                if self.sellButton.checkMouseOver(pos):
                    GameData.money += self.value
                    boat.inventory.remove(self.fish)
                    stateManager.pop()

                if self.keepButton.checkMouseOver(pos):
                    boat.inventory.remove(self.fish)
                    GameData.holdingCellInventory.append(self.fish.convertToDict())
                    stateManager.pop()

class BoatInventoryState(State):
    def __init__(self):
        super().__init__()
        self.marginX = 260
        self.marginY = 290
        self.spacing = 60
        self.spacingY = 90
        self.numPerLine = 7

        self.leftButton = Button((200,300), image="arrow_left.png")
        self.rightButton = Button((750,300), image="arrow_right.png")
        self.currentPage = 0
        self.numFishPerPage = 14
        self.numPages = len(boat.inventory)//self.numFishPerPage

        self.xButton = Button((150,100), image="x_button.png")
        self.titleText = Text("Inventory", 40, (500,200), True, shadow=True)
        self.moneyBox = pygame.transform.scale_by(pygame.image.load("images/uiElements/money_box.png"), 6)
        self.moneyText = Text("$" + str(GameData.money), 20, (35,45))
        self.background = pygame.transform.scale_by(pygame.image.load("images/uiElements/main_menu.png"), 5)
        self.backgroundCoords = (500-self.background.get_width()/2, 350-self.background.get_height()/2)

    def render(self, screen):
        super().render(screen)
        screen.blit(self.background, (self.backgroundCoords[0], self.backgroundCoords[1]))
        self.titleText.render(screen)
        self.xButton.render(screen)
        for i, fish in enumerate(boat.inventory[self.currentPage*self.numFishPerPage:(self.currentPage+1)*self.numFishPerPage]):
            fish.render(screen, (self.marginX + i%self.numPerLine * self.spacing, self.marginY + i//self.numPerLine * self.spacingY))

        screen.blit(self.moneyBox, (20,20))
        self.moneyText.render(screen)

        if self.currentPage > 0:
            self.leftButton.render(screen)
        
        if self.currentPage < self.numPages:
            self.rightButton.render(screen)
            

    def update(self):
        super().update()
        GameData.money = round(GameData.money, 2)
        self.moneyText = Text("$" + str(GameData.money), 20, (35,45))
        self.numPages = len(boat.inventory)//self.numFishPerPage
    

    def handleInput(self, events):
        super().handleInput(events)
        pos = pygame.mouse.get_pos()
        for event in events:
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_q:
                    stateManager.pop()
            if event.type == pygame.MOUSEBUTTONUP:
                if self.xButton.checkMouseOver(pygame.mouse.get_pos()):
                    stateManager.pop()
                
                for i, fish in enumerate(boat.inventory[self.currentPage*self.numFishPerPage:(self.currentPage+1)*self.numFishPerPage]):
                    if pygame.Rect((self.marginX + i%self.numPerLine * self.spacing)*GameData.scaleFactor+GameData.fullscreenOffset, (self.marginY + i//self.numPerLine * self.spacingY)*GameData.scaleFactor, (fish.image.get_width())*GameData.scaleFactor, (fish.image.get_height())*GameData.scaleFactor).collidepoint(pygame.mouse.get_pos()):
                        stateManager.push(FishMenuState(fish))
                
                if self.currentPage > 0:
                    if self.leftButton.checkMouseOver(pos):
                        self.currentPage -= 1
        
                if self.currentPage < self.numPages:
                    if self.rightButton.checkMouseOver(pos):
                        self.currentPage += 1

class MapMenuState(State):
    def __init__(self):
        super().__init__()
        self.surface = pygame.transform.scale_by(pygame.image.load("images/uiElements/main_menu.png"), 5)
        self.map = pygame.transform.scale_by(pygame.image.load("images/map.png"), 5)
        self.xButton = Button((150,100), image="x_button.png")
        self.titleText = Text("Map", 40, (500,200), True, shadow=True)
        self.moneyBox = pygame.transform.scale_by(pygame.image.load("images/uiElements/money_box.png"), 6)
        self.moneyText = Text("$" + str(GameData.money), 20, (35,45))
        self.backgroundCoords = (500 - self.surface.get_width()/2, 350-self.surface.get_height()/2)
        self.mapCoords = (500 - self.map.get_width()/2, 350-self.map.get_height()/2)

    def render(self, screen):
        super().render(screen)
        screen.blit(self.moneyBox, (20,20))
        self.moneyText.render(screen)
        screen.blit(self.surface, (self.backgroundCoords[0], self.backgroundCoords[1]))
        screen.blit(self.map, (self.mapCoords[0], self.mapCoords[1]))
        self.xButton.render(screen)

        for key, value in waterbodies.items():
            value.render(screen)


    def update(self):
        super().update()
        self.moneyText = Text("$" + str(GameData.money), 20, (35,45))
        for key, value in waterbodies.items():
            value.update()
    
    def handleInput(self, events):
        super().handleInput(events)
        for event in events:
            pos = pygame.mouse.get_pos()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_q:
                    stateManager.pop()

            if event.type == pygame.MOUSEBUTTONUP:
                if self.xButton.checkMouseOver(pos):
                    stateManager.pop()
                
                for key, value in waterbodies.items():
                    if value.checkMouseOver():
                        if value.locked:
                            if GameData.money >= value.price:
                                stateManager.push(PopUpQuestionState(value.price, value.name))
                            else:
                                stateManager.push(NotEnoughMoneyState())
                        else: 
                            boat.water = waterObjects[key]
                            stateManager.pop()
                            stateManager.pop()

class NotEnoughMoneyState(State):
    def __init__(self):
        super().__init__()
        self.background = pygame.transform.scale_by(pygame.image.load("images/uiElements/popup_menu.png"), 4)
        self.text = Text("Not enough funds", 25, (500, 300), True, shadow=True)
        self.okButton = Button((450,350), "Okay")
        self.backgroundCoords = (500-self.background.get_width()/2, 350-self.background.get_height()/2)

    def render(self, screen):
        super().render(screen)
        screen.blit(self.background, (self.backgroundCoords[0], self.backgroundCoords[1]))
        self.text.render(screen)
        self.okButton.render(screen)
    
    def handleInput(self, events):
        super().handleInput(events)
        for event in events: 
            if event.type == pygame.MOUSEBUTTONUP:
                if self.okButton.checkMouseOver(pygame.mouse.get_pos()):
                    stateManager.pop()

class PopupStateBase(State):
    def __init__(self, price, name, adjective="unlock"):
        super().__init__()
        self.name = name
        self.background = pygame.transform.scale_by(pygame.image.load("images/uiElements/popup_menu.png"), 4)
        self.price = price
        self.texts = [
            Text("Would you like", 20, (500, 260), True, shadow=True),
            Text("to " + adjective, 20, (500, 285), True, shadow=True),
        ]
        self.nameOffset = 0
        if type(self.name) == list:
            self.name.reverse()
            for i in range(len(self.name)-1,0,-1):
                if len(self.name[i] + self.name[i-1]) < 15:
                    self.name[i-1] = self.name[i] + " " + self.name[i-1]
                    self.name.pop(i)
            self.name.reverse()

            for text in self.name:
                self.texts.append(Text(str(text), 20, (500, 310 + self.nameOffset), True, shadow=True))
                self.nameOffset += 25
            self.nameOffset -= 25
        else:
            self.texts.append(Text(str(self.name), 20, (500, 310), True, shadow=True))

        self.texts.append(Text("for $" + str(price) + "?", 20, (500, 335+self.nameOffset), True, shadow=True))
        
        self.yesButton = Button((350, 400), "Yes", "small_button.png")
        self.noButton = Button((510, 400), "No", "small_button.png")
        self.backgroundCoords = (500-self.background.get_width()/2, 350-self.background.get_height()/2)

    def render(self, screen):
        super().render(screen)
        screen.blit(self.background, (self.backgroundCoords[0], self.backgroundCoords[1]))
        for text in self.texts:
            text.render(screen)

        self.yesButton.render(screen)
        self.noButton.render(screen)
    
    def handleInput(self, events):
        super().handleInput(events)
        mouse = pygame.mouse.get_pos()
        for event in events:
            if event.type == pygame.MOUSEBUTTONUP:
                if self.yesButton.checkMouseOver(mouse):
                    stateManager.pop()
                    GameData.money -= self.price
                    stateManager.queue[-1].bought = True

                elif self.noButton.checkMouseOver(mouse):
                    stateManager.pop()


class PopUpQuestionState(PopupStateBase):
    def __init__(self, price, lake):
        super().__init__(price, lake)
        self.name = lake
        self.lake = lake

    def render(self, screen):
        super().render(screen)
        screen.blit(self.background, (self.backgroundCoords[0], self.backgroundCoords[1]))
        for text in self.texts:
            text.render(screen)

        self.yesButton.render(screen)
        self.noButton.render(screen)
    
    
    def handleInput(self, events):
        mouse = pygame.mouse.get_pos()
        for event in events:
            if event.type == pygame.MOUSEBUTTONUP:
                if self.yesButton.checkMouseOver(mouse):
                    stateManager.pop()
                    GameData.money -= self.price
                    waterbodies[self.lake].locked = False
                    GameData.watersUnlocked.append(self.lake)
                elif self.noButton.checkMouseOver(mouse):
                    stateManager.pop()


class ShopStateBase(State):
    def __init__(self, title):
        super().__init__()
        self.surface = pygame.transform.scale_by(pygame.image.load("images/uiElements/main_menu.png"), 5)
        self.xButton = Button((150,100), image="x_button.png")
        self.titleText = Text(title, 40, (500,200), True, shadow=True)
        self.backgroundCoords = (500 - self.surface.get_width()/2, 350-self.surface.get_height()/2)
        self.moneyBox = pygame.transform.scale_by(pygame.image.load("images/uiElements/money_box.png"), 6)
        self.moneyText = Text("$" + str(GameData.money), 20, (35,45))

        self.maxItemsPerPage = 8
        self.leftButton = Button((215,350), image="arrow_left.png")
        self.rightButton = Button((750,350), image="arrow_right.png")
        self.currentPage = 0
        self.numPages = len(self.shopItems)//self.maxItemsPerPage

    def renderBackground(self, screen):
        super().render(screen)
        screen.blit(self.surface, (self.backgroundCoords[0], self.backgroundCoords[1]))
        self.titleText.render(screen)
        self.xButton.render(screen)
        screen.blit(self.moneyBox, (20, 20))
        self.moneyText.render(screen)

    def renderItems(self, screen):
        for i, item in enumerate(self.shopItems[self.currentPage*8:(self.currentPage+1)*8]):
            item.render(screen, (260+(i%4)*120, 270+(i//4)*130))

        if self.currentPage > 0:
            self.leftButton.render(screen)
        
        if self.currentPage < self.numPages:
            self.rightButton.render(screen)
    
    def update(self):
        super().update()
        self.moneyText = Text("$" + str(GameData.money), 20, (35,45))
    
    def handleInput(self, events):
        super().handleInput(events)
        for event in events:
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                if self.xButton.checkMouseOver(pos):
                    stateManager.pop()

                if self.currentPage > 0:
                    if self.leftButton.checkMouseOver(pos):
                        self.currentPage -= 1
        
                if self.currentPage < self.numPages:
                    if self.rightButton.checkMouseOver(pos):
                        self.currentPage += 1

class ShopState(ShopStateBase):
    def __init__(self):
        self.shopItems = [
            ShopLabelButton("Unlock", (285, 300), "radar1.png"),
            ShopLabelButton("Upgrade", (430, 300), "line.png"),
            ShopLabelButton("Acquire", (575, 300), "worm.png")
        ]
        super().__init__("Shop")

    def render(self, screen):
        super().renderBackground(screen)
        for item in self.shopItems:
            item.render(screen)
    
    def update(self):
        super().update()
    
    def handleInput(self, events):
        super().handleInput(events)
        for event in events:
            if event.type == pygame.MOUSEBUTTONUP:
                for i, item in enumerate(self.shopItems):
                    if item.checkMouseOver():
                        if i == 0:
                            stateManager.push(ShopUnlockablesState())
                        elif i == 1:
                            stateManager.push(ShopUpgradablesState())
                        elif i == 2:
                            stateManager.push(ShopItemsState())

class ShopUnlockablesState(ShopStateBase):
    def __init__(self):
        self.shopItems = []
        for i, item in enumerate(GameData.upgradeData["unlockables"]):
            self.shopItems.append(UnlockableItem(i))
        self.selectedItemIndex = None
        self.selectedItem = None
        self.bought = False
        super().__init__("Unlockables")

    def render(self, screen):
        super().renderBackground(screen)
        super().renderItems(screen)
    
    def update(self):
        super().update()
        if self.selectedItem != None and self.bought:
            if self.selectedItem.name == "Line 2":
                if self.selectedItem.unlocked == False:
                    self.selectedItem.unlocked = True
                    GameData.upgradeData["unlockables"][self.selectedItemIndex]["unlocked"] = True
                    GameData.lines[1]["locked"] = False
                else:
                    GameData.upgradeData["unlockables"][self.selectedItemIndex]["level"] += 1
            if self.selectedItem.name == "Line 3":
                if self.selectedItem.unlocked == False:
                    self.selectedItem.unlocked = True
                    GameData.upgradeData["unlockables"][self.selectedItemIndex]["unlocked"] = True
                    GameData.lines[2]["locked"] = False
                else:
                    GameData.upgradeData["unlockables"][self.selectedItemIndex]["level"] += 1
            if self.selectedItem.name == "Line 4":
                if self.selectedItem.unlocked == False:
                    self.selectedItem.unlocked = True
                    GameData.upgradeData["unlockables"][self.selectedItemIndex]["unlocked"] = True
                    GameData.lines[3]["locked"] = False
                else:
                    GameData.upgradeData["unlockables"][self.selectedItemIndex]["level"] += 1
            
            self.shopItems[self.selectedItemIndex] = UnlockableItem(GameData.upgradeData["unlockables"][self.selectedItemIndex])
            self.selectedItem = None 
            self.selectedItemIndex = None
            self.bought = False
    
    def handleInput(self, events):
        super().handleInput(events)
        for event in events:
            if event.type == pygame.MOUSEBUTTONUP:
                for i, item in enumerate(self.shopItems):
                    if item.checkMouseOver():
                        self.selectedItemIndex = i
                        self.selectedItem = item
                        if not item.unlocked:
                            stateManager.push(PopupStateBase(item.cost, item.name))
                        else:
                            stateManager.push(PopupStateBase(item.cost, item.name, "upgrade"))

class ShopUpgradablesState(ShopStateBase):
    def __init__(self):
        self.shopItems = []
        for item in GameData.upgradeData["upgradables"]:
            self.shopItems.append(UpgradableItem(item))
        self.selectedItem = None
        self.selectedItemIndex = None
        self.bought = False
        super().__init__("Upgradables")

    def render(self, screen):
        super().renderBackground(screen)
        super().renderItems(screen)
    
    def update(self):
        super().update()
        if self.selectedItemIndex != None and self.selectedItem != None and self.bought:
            self.selectedItem.upgradeItem()
            self.selectedItemIndex = None
            self.selectedItem = None
            self.bought = False
    
    def handleInput(self, events):
        super().handleInput(events)
        for event in events:
            if event.type == pygame.MOUSEBUTTONUP:
                for i, item in enumerate(self.shopItems):
                    if item.checkMouseOver():
                        self.selectedItem = item
                        self.selectedItemIndex = i
                        stateManager.push(PopupStateBase(item.cost, item.name, "upgrade"))


class ShopItemsState(ShopStateBase): # fix this class
    def __init__(self):
        self.shopItems = []
        for item in GameData.upgradeData["items"]:
            self.shopItems.append(BuyableItem(item))
        self.bought = False
        self.selectedItem = None
        super().__init__("Bait n Hooks")

    def render(self, screen):
        super().renderBackground(screen)
        super().renderItems(screen)
    
    def update(self):
        super().update()
        if self.bought and self.selectedItem != None:
            if "hook" in self.selectedItem:
                GameData.itemsBought["hooks"].append(self.selectedItem[5:-4])
            else:
                GameData.itemsBought["bait"].append(self.selectedItem)
            self.selectedItem = None
            self.bought = False
        elif self.selectedItem != None and self.bought == False:
            self.selectedItem = None

    
    def handleInput(self, events):
        super().handleInput(events)
        for event in events:
            if event.type == pygame.MOUSEBUTTONUP:
                for item in self.shopItems:
                    if item.checkMouseOver():
                        self.selectedItem = item.image
                        stateManager.push(PopupStateBase(item.cost, item.name, "purchase"))




class BoatMenuState(State):
    def __init__(self):
        super().__init__()
        self.background = pygame.transform.scale_by(pygame.image.load("images/uiElements/boat_menu.png"), 5)
        self.pos = (450,110)
        self.xButton = Button((445,100), image="x_button2.png")
        self.lineTiles = []
        for i in range(4):
            self.lineTiles.append(LineMenu((472+i*120, 140), "Line " + str(i+1), GameData.lines[i]["locked"], GameData.lines[i]["bait"], GameData.lines[i]["hook"]))

        # self.netTile = pygame.transform.scale_by(pygame.image.load("images/uiElements/net_window.png"), 5)
        # self.radarTile = pygame.transform.scale_by(pygame.image.load("images/uiElements/radar_window.png"), 5)
        # self.netIcon = pygame.transform.scale_by(pygame.image.load("images/uiElements/net_1.png"), 5)
        # self.radarIcon = pygame.transform.scale_by(pygame.image.load("images/uiElements/radar1.png"), 5)

        # self.netText = Text("Casting Net", 15, (515, 390))
        # self.radarText = Text("Fish Radar", 15, (755, 390))


    def render(self, screen):
        super().render(screen)
        screen.blit(self.background, (self.pos[0], self.pos[1]))

        for tile in self.lineTiles:
            tile.render(screen)

        
        # screen.blit(self.netTile, (490, 370))
        # screen.blit(self.radarTile, (720, 370))

        # screen.blit(self.netIcon, (620,450))
        # screen.blit(self.radarIcon, (800,440))

        
        # screen.blit(self.lockImage, (575,425))
        # screen.blit(self.lockImage, (795,425))

        self.xButton.render(screen)

    
    def update(self):
        super().update()
        # for i, line in enumerate(self.lineTiles):
        #     self.lineTiles[i] = LineMenu((472+i*120, 140), "Line " + str(i+1), GameData.lines[i]["locked"], GameData.lines[i]["bait"], GameData.lines[i]["hook"])
        #     pass
    
    def handleInput(self, events):
        super().handleInput(events)
        pos = pygame.mouse.get_pos()
        for event in events:
            if event.type == pygame.MOUSEBUTTONUP:
                for i, tile in enumerate(self.lineTiles):
                    if not tile.locked and tile.checkMouseOver():
                        stateManager.push(LineCustomizeMenuState(i))
                if self.xButton.checkMouseOver(pos):
                    stateManager.pop()
                
                for i, line in enumerate(self.lineTiles):
                    self.lineTiles[i] = LineMenu((472+i*120, 140), "Line " + str(i+1), GameData.lines[i]["locked"], GameData.lines[i]["bait"], GameData.lines[i]["hook"])
            
                
# This is the class for the little menu on the left where you can change the bait and hooks on each line.
# This class is a disgusting mess at least i only have to make it once and never touch it again.
class LineCustomizeMenuState(State):
    def __init__(self, line):
        super().__init__()
        self.line = line
        self.lineData = GameData.lines[line]
        self.background = pygame.transform.scale_by(pygame.image.load("images/uiElements/line_menu.png"), 5)
        self.bgCoords = (20, 170)
        self.xButton = Button((15,160), image="x_button2.png")
        self.leftArrow = pygame.transform.scale_by(pygame.image.load("images/uiElements/arrow_left.png"), 3)
        self.rightArrow = pygame.transform.scale_by(pygame.image.load("images/uiElements/arrow_right.png"), 3)
        self.leftArrowRect = pygame.Rect(30,440,20,40)
        self.rightArrowRect = pygame.Rect(415, 440, 20,40)
        self.titleText = Text("Line 1", 25, (235,195), centered=True, shadow=True)
        self.baitText = Text("Bait", 15, (145, 250), True)
        self.hookText = Text("Hook", 15, (320, 250), True)
        self.tabs = pygame.transform.scale_by(pygame.image.load("images/uiElements/tabs1.png"), 5)
        self.lineItem = pygame.transform.scale_by(pygame.image.load("images/uiElements/line_window2.png"), 5)

        self.baitBox = pygame.Rect(80,235, 135,125)
        self.hookBox = pygame.Rect(250,235, 135,125)

        self.baitTabRect = pygame.Rect(35,365, 52, 35)
        self.hookTabRect = pygame.Rect(87,365, 53, 35)

        self.inventoryRect = pygame.Rect(20,400, 425,120)

        self.bait = self.lineData["bait"]
        if self.bait != None:
            self.bait = BaitItem(self.bait, self.baitBox.center)
        self.hook = self.lineData["hook"]
        if self.hook != None:
            self.hook = HookItem(self.hook, self.hookBox.center)

        self.currentTab = "bait"
        self.numItemsPerPage = 4
        self.currentPage = 0

        self.inventoryBait = []
        for item in GameData.itemsBought["bait"]:
            self.inventoryBait.append(BaitItem(item, (0,0)))
        
        self.inventoryHooks = []
        for item in GameData.itemsBought["hooks"]:
            self.inventoryHooks.append(HookItem(item, (0,0)))

        self.numPages = len(self.inventoryBait)//self.numItemsPerPage


    def render(self, screen):
        super().render(screen)
        screen.blit(self.background, (self.bgCoords[0], self.bgCoords[1]))
        self.xButton.render(screen)
        
        if self.currentPage > 0:
            screen.blit(self.leftArrow, (30,440))
        if self.currentPage < self.numPages:
            screen.blit(self.rightArrow, (415,440))

        screen.blit(self.lineItem, (80,235))
        screen.blit(self.lineItem, (250,235))


        self.titleText.render(screen)
        self.baitText.render(screen)
        self.hookText.render(screen)

        if self.bait != None:
            self.bait.render(screen)
        
        if self.hook != None:
            self.hook.render(screen)

        screen.blit(self.tabs, (35, 365))

        if self.currentTab == "bait":
            for i, item in enumerate(self.inventoryBait[self.currentPage*self.numItemsPerPage:(self.currentPage+1)*self.numItemsPerPage]):
                item.render(screen, (75+i*80,435))

        elif self.currentTab == "hooks":
            for i, item in enumerate(self.inventoryHooks[self.currentPage*self.numItemsPerPage:(self.currentPage+1)*self.numItemsPerPage]):
                item.render(screen, (75+i*80,435))

    
    def update(self):
        super().update()
        if self.bait != None:
            self.bait.update()
        if self.hook != None:
            self.hook.update()

        if self.currentTab == "bait":
            for i, item in enumerate(self.inventoryBait[self.currentPage*self.numItemsPerPage:(self.currentPage+1)*self.numItemsPerPage]):
                item.update()

        elif self.currentTab == "hooks":
            for i, item in enumerate(self.inventoryHooks[self.currentPage*self.numItemsPerPage:(self.currentPage+1)*self.numItemsPerPage]):
                item.update()

    def handleInput(self, events):
        super().handleInput(events)
        pos = pygame.mouse.get_pos()
        if self.bait != None:
            self.bait.handleInput(events)
        if self.hook != None:
            self.hook.handleInput(events)

        if self.currentTab == "bait":
            for i, item in enumerate(self.inventoryBait[self.currentPage*self.numItemsPerPage:(self.currentPage+1)*self.numItemsPerPage]):
                item.handleInput(events)
                
        elif self.currentTab == "hooks":
            for i, item in enumerate(self.inventoryHooks[self.currentPage*self.numItemsPerPage:(self.currentPage+1)*self.numItemsPerPage]):
                item.handleInput(events)

        for event in events: 
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.xButton.checkMouseOver(pos):
                    stateManager.pop()
            if event.type == pygame.MOUSEBUTTONUP:

                if self.baitTabRect.collidepoint(pos):
                    self.currentTab = "bait"
                    self.currentPage = 0
                    self.numPages = len(self.inventoryBait)//self.numItemsPerPage
                if self.hookTabRect.collidepoint(pos):
                    self.currentTab = "hooks"
                    self.currentPage = 0
                    self.numPages = len(self.inventoryHooks)//self.numItemsPerPage
                
                if self.leftArrowRect.collidepoint(pos) and self.currentPage > 0:
                    self.currentPage -= 1
                if self.rightArrowRect.collidepoint(pos) and self.currentPage < self.numPages:
                    self.currentPage += 1
                
                if self.currentTab == "bait":
                    for i, item in enumerate(self.inventoryBait[self.currentPage*self.numItemsPerPage:(self.currentPage+1)*self.numItemsPerPage]):
                        if item.dragging:
                            item.dragging = False
                            if pygame.Rect(pos[0]-item.draggingOffset[0], pos[1]-item.draggingOffset[1], item.rect.w, item.rect.h).colliderect(self.baitBox):
                                if self.bait != None:
                                    GameData.itemsBought["bait"].append(self.bait.imageName) # adds the replaced item to the GameData class
                                    self.inventoryBait.append(BaitItem(self.bait.imageName, (0,0))) # adds the same item to the current loaded inventory
                                GameData.itemsBought["bait"].remove(item.imageName)
                                self.inventoryBait.remove(item)
                                self.bait = BaitItem(item.imageName, self.baitBox.center)
                                GameData.lines[self.line]["bait"] = self.bait.imageName
                                break
                
                elif self.currentTab == "hooks":
                    for i, item in enumerate(self.inventoryHooks[self.currentPage*self.numItemsPerPage:(self.currentPage+1)*self.numItemsPerPage]):
                        if item.dragging:
                            item.dragging = False
                            if pygame.Rect(pos[0]-item.draggingOffset[0], pos[1]-item.draggingOffset[1], item.rect.w, item.rect.h).colliderect(self.hookBox):
                                if self.hook != None:
                                    GameData.itemsBought["hooks"].append(self.hook.imageName) # adds the replaced item to the GameData class
                                    self.inventoryHooks.append(HookItem(self.hook.imageName, (0,0))) # adds the same item to the current loaded inventory
                                GameData.itemsBought["hooks"].remove(item.imageName)
                                self.inventoryHooks.remove(item)
                                self.hook = HookItem(item.imageName, self.hookBox.center)
                                GameData.lines[self.line]["hook"] = self.hook.imageName
                                break









class HoldingCellState(State):
    def __init__(self):
        super().__init__()

    def render(self, screen):
        super().render(screen)

    def update(self):
        super().update()
    
    def handleInput(self, events):
        super().handleInput(events)









# Might delete

class IntroMenuState(State):
    def __init__(self):
        super().__init__()

    def render(self, screen):
        super().render(screen)
        screen.fill((150,200,180))

    def update(self):
        super().update()
    
    def handleInput(self, events):
        super().handleInput(events)

class TutorialState(State):
    def __init__(self):
        super().__init__()

    def render(self, screen):
        super().render(screen)

    def update(self):
        super().update()
    
    def handleInput(self, events):
        super().handleInput(events)

