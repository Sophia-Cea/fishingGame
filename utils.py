import pygame
import sys
import os
import math
import random
from datetime import datetime
from data import *
import platform

pygame.init()

info = pygame.display.Info()
screen_width = info.current_w
screen_height = info.current_h
screen_width, screen_height


now = datetime.now()
hours = now.hour
minutes = now.minute
time = float(hours + minutes/60)

WIDTH = 1000
HEIGHT = 700
delta = 1


def get_save_path():
    # Choose a safe folder depending on OS
    if platform.system() == "Windows":
        base = os.environ.get("APPDATA", os.path.expanduser("~"))
    elif platform.system() == "Darwin":  # macOS
        base = os.path.expanduser("~/Library/Application Support")
    else:  # Linux
        base = os.path.expanduser("~")

    folder = os.path.join(base, "fishingGame")  # your game folder
    os.makedirs(folder, exist_ok=True)  # create if it doesn't exist

    return os.path.join(folder, "savegame.json")

GameData.savePath = get_save_path()
print(GameData.savePath)


savedata = {
        "money" : GameData.money,
        "aquariumLocked" : GameData.aquariumLocked,
        "holdingCellInventory" : GameData.holdingCellInventory,
        "aquariumRoomsUnlocked" : GameData.aquariumRoomsUnlocked,
        "upgradesAcquired" : GameData.upgradesAcquired,
        "watersUnlocked" : GameData.watersUnlocked,
        "boatInventory" : GameData.boatInventory
}


try:
    with open(GameData.savePath, "r") as file:
        user_data = json.load(file)
    GameData.money = user_data["money"]
    GameData.aquariumLocked = user_data["aquariumLocked"]
    GameData.holdingCellInventory = user_data["holdingCellInventory"]
    GameData.aquariumRoomsUnlocked = user_data["aquariumRoomsUnlocked"]
    GameData.upgradesAcquired = user_data["upgradesAcquired"]
    GameData.watersUnlocked = user_data["watersUnlocked"]
    GameData.boatInventory = user_data["boatInventory"]
    print("opened file and set values")
except:
    with open(GameData.savePath, 'w', encoding='utf-8') as json_file:
        json.dump(savedata, json_file, indent=4) 
    print("did exception")



#issue where fish dont wanna be fishes in the json file. need to convert them to dicts then convert them back when saving

def saveGame():
    saveData = {
        "money" : GameData.money,
        "aquariumLocked" : GameData.aquariumLocked,
        "holdingCellInventory" : GameData.holdingCellInventory,
        "aquariumRoomsUnlocked" : GameData.aquariumRoomsUnlocked,
        "upgradesAcquired" : GameData.upgradesAcquired,
        "watersUnlocked" : GameData.watersUnlocked,
        "boatInventory" : GameData.boatInventory
    }
    with open(GameData.savePath, 'w', encoding='utf-8') as json_file:
        json.dump(saveData, json_file, indent=4)




def resizeRect(rect, scaleFactor):
    return pygame.Rect(rect.x*scaleFactor, rect.y*scaleFactor, rect.w*scaleFactor, rect.h*scaleFactor)


def resource_path(relative_path):
  if hasattr(sys, '_MEIPASS'):
      return os.path.join(sys._MEIPASS, relative_path)
  return os.path.join(os.path.abspath('.'), relative_path)

class Text:
    texts = []
    def __init__(self, text, size, position, centered=False, color=(237,222,155), shadow=False, shadowColor=(17,54,65)) -> None:
        self.content = str(text)
        self.font = pygame.font.Font(resource_path("font.ttf"), int(size))
        self.color = color
        self.pos = position
        self.centered = centered
        self.text = self.font.render(self.content, True, self.color)
        if shadow:
            self.shadowText = self.font.render(self.content, True, shadowColor)
            increment = self.text.get_height()*.1
            self.surface = pygame.Surface((self.text.get_width() + increment*2, self.text.get_height() + increment*3), pygame.SRCALPHA)
            self.surface.blit(self.shadowText, (0,increment))
            self.surface.blit(self.shadowText, (increment * 2, increment))
            self.surface.blit(self.shadowText, (increment, 0))
            self.surface.blit(self.shadowText, (increment, increment*3))
            self.surface.blit(self.shadowText, (increment, increment*2))
            self.surface.blit(self.text, (increment, increment))
            
            self.text = self.surface
        self.rect = self.rect = pygame.Rect(self.pos[0], self.pos[1], self.text.get_width(), self.text.get_height())
        if self.centered:
            self.rect.x -= self.text.get_width()/2
        
        self.scaledImage = pygame.transform.scale_by(self.text, 1)

    def render(self, surface):
        surface.blit(self.text, (self.rect.x, self.rect.y))
    
    def resize(self, scalefactor):
        self.scaledImage = pygame.transform.scale_by(self.text, 1)


class Button:
    def __init__(self, pos:tuple, text:str = None, image:str = None) -> None:
        self.font = pygame.font.Font(resource_path("font.ttf"), 18)
        self.text = text
        self.scaleFactor = 5
        if image == None:
            self.image: pygame.Surface = pygame.transform.scale_by(pygame.image.load("images/uiElements/button.png"), self.scaleFactor)
        else:
            self.image: pygame.Surface = pygame.transform.scale_by(pygame.image.load("images/uiElements/" + image), self.scaleFactor)
        
        self.rect: pygame.Rect = pygame.Rect(pos[0],pos[1], self.image.get_width(), self.image.get_height())

        if self.text != None:
            self.text = self.font.render(self.text, True, (237,222,155))
            self.image.blit(self.text, (self.image.get_width()/2-self.text.get_width()/2, self.image.get_height()/2-self.text.get_height()/2))

        self.hovering = False

    def render(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))

    def checkMouseOver(self, pos):
        tempRect = pygame.Rect(self.rect.x*GameData.scaleFactor, self.rect.y*GameData.scaleFactor, self.rect.w*GameData.scaleFactor, self.rect.h*GameData.scaleFactor)
        if tempRect.collidepoint(pos):
            return True


timeOfDay = {
    "Morning" : pygame.transform.scale_by(pygame.image.load("images/boat_backgrounds/sunrise.png"),4),
    "Day": pygame.transform.scale_by(pygame.image.load("images/boat_backgrounds/day.png"),4),
    "Evening": pygame.transform.scale_by(pygame.image.load("images/boat_backgrounds/sunset.png"),4),
    "Night": pygame.transform.scale_by(pygame.image.load("images/boat_backgrounds/night.png"),4)
}


# time = 18

if time >= 4.5 and time < 7: # 4:30 am to 7 am
    time = "Morning"

elif time >= 7 and time < 17.5: # 7 am to 5:30 pm
    time = "Day"

elif time >= 17.5 and time < 18.5: # 5:30 pm to 6:30 pm
    time = "Evening"

else: # 6:30 pm to 4:30 am
    time = "Night"

sky = timeOfDay[time]

