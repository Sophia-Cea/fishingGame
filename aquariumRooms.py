

class AquariumRoom:
    def __init__(self):
        pass

    def render(self, screen):
        pass

    def update(self):
        pass

    def handleInput(self, events):
        pass


class AquariumRoom1(AquariumRoom):
    def __init__(self):
        super().__init__()
        self.unlockableAquariums = [
            Aquarium((170,60)), 
            Aquarium((340,60)), 
            Aquarium((510,60)), 
            Aquarium((680,60)), 
            
            Aquarium((170,180)), 
            Aquarium((340,180)), 
            Aquarium((510,180)), 
            Aquarium((680,180)), 

            Aquarium((170,300)), 
            Aquarium((340,300)), 
            Aquarium((510,300)), 
            Aquarium((680,300)), 
        ]


class Aquarium:
    def __init__(self, pos):
        self.fish = []
        self.decor = []
        self.background = pygame.Surface((WIDTH, HEIGHT))
        self.waterType = "fresh"
        self.rect = pygame.Rect(pos[0], pos[1], 150,100)
        self.thumbnailImage = pygame.Surface(self.rect.size)
        self.thumbnailImage.fill((0, 18, 25))
        pygame.draw.rect(self.thumbnailImage, (38, 70, 83), (4,4,142,92))

    def render(self, screen):
        screen.blit(self.background, (0,0))
        for decor in self.decor:
            decor.render(screen)

        for fish in self.fish:
            fish.render(screen)
    
    def renderThumbnail(self, screen):
        screen.blit(self.thumbnailImage, self.rect.topleft)

    def update(self):
        for decor in self.decor:
            decor.update()

        for fish in self.fish:
            fish.update()
