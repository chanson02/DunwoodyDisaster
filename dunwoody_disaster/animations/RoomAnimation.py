import pygame
from dunwoody_disaster.animations.PygameAnimation import PygameAnimation
from dunwoody_disaster.animations.idle import IdleComponent
from dunwoody_disaster.animations.AnimationComponent import AnimationComponent


class RoomAnimation(PygameAnimation):
    def __init__(self, background: str, player: str, enemy: str):
        super().__init__()
        self.bkg = pygame.transform.scale(
            pygame.image.load(background).convert_alpha(), self.size
        )
        self.components: list[AnimationComponent] = []

        self.player_pos = (int(self.size[0] * 0.15), int(self.size[1] * 0.5))
        self.enemy_pos = (int(self.size[0] * 0.70), int(self.size[1] * 0.5))

        player_size = int(max(self.size) * 0.15)
        player_size = (player_size, player_size)

        idle = IdleComponent(player, self.player_pos, player_size)
        idle.elapsed = 30  # offset so they don't bounce together
        self.components.append(idle)
        self.components.append(IdleComponent(enemy, self.enemy_pos, player_size))

    def run(self) -> None:
        self.clock.tick(20)
        if self.running:
            self.surface.blit(self.bkg, (0, 0))

            for component in self.components:
                component.draw(self.surface)
