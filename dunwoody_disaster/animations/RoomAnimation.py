import pygame
from dunwoody_disaster.animations.PygameAnimation import PygameAnimation
from dunwoody_disaster.animations.idle import IdleComponent
from dunwoody_disaster.animations.AnimationComponent import AnimationComponent


class RoomAnimation(PygameAnimation):
    def __init__(self, background: str, player: str, enemy: str):
        super().__init__()
        self.bkg = pygame.transform.scale(pygame.image.load(background).convert_alpha(), self.size)
        self.components: list[AnimationComponent] = []

        self.player_pos = (100, 200)
        self.enemy_pos = (450, 200)

        idle = IdleComponent(player, self.player_pos)
        idle.elapsed = 30  # offset so they don't bounce together
        self.components.append(idle)
        self.components.append(IdleComponent(enemy, self.enemy_pos))

    def run(self) -> None:
        self.clock.tick(20)
        if self.running:
            self.surface.blit(self.bkg, (7, 0))

            for component in self.components:
                component.draw(self.surface)
