import pygame
import sys
from state import *

pygame.init()
fpsClock = pygame.time.Clock()
screen = pygame.display.set_mode([WIDTH, HEIGHT], pygame.RESIZABLE)
display = pygame.Surface((WIDTH,HEIGHT))
pygame.display.set_caption("Fish & Flow")
pygame.display.set_icon(pygame.transform.scale_by(pygame.image.load("images/uiElements/logo.png"), 2))

stateManager.push(IntroMenuState())
stateManager.push(BoatState())
# stateManager.push(BoatMenu())

'''
TODO: 
needa make fish type dependent on upgrades n shit
make holding pen
make holding pen upgrades
differentiate between fresh, salt, and brackish fish


needa make the shop items work

'''


running = True
while running:
    events = pygame.event.get() 
    for event in events:
        if event.type == pygame.QUIT:
            saveGame()
            running = False
            pygame.quit()
            sys.exit()
        if event.type == pygame.VIDEORESIZE:
            print("is resized")
            width = screen.get_width()
            if width < 1000:
                width = 1000
            height = width * .7
            screen = pygame.display.set_mode([width, height], pygame.RESIZABLE)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                stateManager.push(BoatMenuState())

    # WIDTH, HEIGHT = pygame.display.get_window_size()
    WIDTH, HEIGHT = screen.get_size()

    if WIDTH/HEIGHT == 10/7:
        GameData.scaleFactor = WIDTH/1000
        GameDataisFullscreen = False
        GameData.fullscreenOffset = 0

    elif WIDTH/HEIGHT != 10/7:
        print("is fullscreen")
        GameData.isFullscreen = True
        GameData.scaleFactor = HEIGHT/700
        GameData.fullscreenOffset = screen.get_width()/2-(display.get_width()*GameData.scaleFactor)/2

    
    stateManager.run(display, events)
    # screen.fill((255,0,0))
    screen.fill((0,255,255))
    if GameData.isFullscreen:
        # screen.blit(display, (GameData.fullscreenOffset,0))
        screen.blit(pygame.transform.scale_by(display, GameData.scaleFactor), (GameData.fullscreenOffset,0))
    else:
        screen.blit(pygame.transform.scale_by(display, GameData.scaleFactor), (0,0))
    pygame.display.flip() 
    delta = fpsClock.tick(60)/1000
