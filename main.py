import pygame
import sys
from state import *

pygame.init()
fpsClock = pygame.time.Clock()
screen = pygame.display.set_mode([WIDTH, HEIGHT], pygame.RESIZABLE)
pygame.display.set_caption("Fish & Flow")
pygame.display.set_icon(pygame.transform.scale_by(pygame.image.load("images/uiElements/logo.png"), 2))

stateManager.push(IntroMenuState())
stateManager.push(BoatState())
# stateManager.push(BoatMenu())



'''
TODO: 
needa make fish type dependent on upgrades n shit


needa make the shop items work

needa make a class for the casting line stuff to stop making such a mess
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
            width = screen.get_width()
            if width < 1000:
                width = 1000
            height = width * .7
            screen = pygame.display.set_mode([width, height], pygame.RESIZABLE)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                stateManager.push(BoatMenuState())

    WIDTH, HEIGHT = screen.get_size()
    GameData.scaleFactor = WIDTH/1000
    
    stateManager.run(screen, events)
    pygame.display.flip() 
    delta = fpsClock.tick(60)/1000
