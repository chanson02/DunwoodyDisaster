import pygame
from dunwoody_disaster.animations import animation

class AnimationClass:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        self.clock = pygame.time.Clock()
        self.fps = 60
        self.running = True
        self.animation = animation.Animation(r"C:/Users/vuejohw/OneDrive - Dunwoody College of Technology/Documents/Data Structures/Class/DunwoodyDisaster/dunwoody_disaster/animations/Animation_Assets/idle", 8)

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.animation.update()
            self.screen.fill((0, 0, 0))
            self.animation.draw(self.screen, 350, 250)
            pygame.display.flip()
            self.clock.tick(self.fps)