import pygame
from dunwoody_disaster import ASSETS
from dunwoody_disaster.animations.idle import IdleAnimation


class Battle:
    def __init__(self):
        pygame.init()
        self.setup_screen()
        self.load_resources()
        self.clock = pygame.time.Clock()
        self.running = True
        self.FPS = 60
        self.player_health = 100
        self.enemy_health = 100
        self.player_turn = True

    def load_resources(self):
        try:
            self.background_img = pygame.image.load(ASSETS["background"]).convert()
            user_animation_path = "path_to_idle_animation_user"
            enemy_animation_path = "path_to_idle_animation_enemy"
            self.sprite_animation_user = IdleAnimation(user_animation_path, 8)
            self.sprite_animation_enemy = IdleAnimation(enemy_animation_path, 8)
        except Exception as e:
            print(f"Failed to load resources: {e}")
            self.running = False

    def setup_screen(self):
        self.screen = pygame.display.set_mode((800, 600), pygame.RESIZABLE)
        pygame.display.set_caption("Pokémon Battle Simulator")

    def process_attack(self):
        if self.player_turn:
            self.enemy_health = max(self.enemy_health - 20, 0)
            print("Player attacked")
        else:
            self.player_health = max(self.player_health - 20, 0)
            print("Enemy Attacked")
        # Ensure that the player turn toggles
        self.player_turn = not self.player_turn

    def update_animations(self):
        self.sprite_animation_user.next_frame()
        self.sprite_animation_enemy.next_frame()

    def draw_battle(self):
        self.screen.blit(
            pygame.transform.scale(self.background_img, self.screen.get_size()), (0, 0)
        )
        self.sprite_animation_user.draw(
            self.screen,
            (int(self.screen.get_width() * 0.23), int(self.screen.get_height() * 0.60)),
            (80, 100),
        )
        self.sprite_animation_enemy.draw(
            self.screen,
            (int(self.screen.get_width() * 0.70), int(self.screen.get_height() * 0.25)),
            (100, 100),
        )
        self.draw_health_bars()
        pygame.display.flip()

    def draw_health_bars(self):
        # Draw player's health bar
        player_health_bar_width = int(
            self.screen.get_width() * 0.2
        )  # 20% of screen width
        player_health_bar_height = 20
        player_health_bar_x = (
            self.screen.get_width() - player_health_bar_width - 10
        )  # 10 pixels from the right edge
        player_health_bar_y = (
            self.screen.get_height() - player_health_bar_height - 10
        )  # 10 pixels from the bottom

        # Draw the full health background (Red)
        pygame.draw.rect(
            self.screen,
            (255, 0, 0),
            (
                player_health_bar_x,
                player_health_bar_y,
                player_health_bar_width,
                player_health_bar_height,
            ),
        )
        # Draw the current health (Green)
        pygame.draw.rect(
            self.screen,
            (0, 255, 0),
            (
                player_health_bar_x,
                player_health_bar_y,
                player_health_bar_width * (self.player_health / 100),
                player_health_bar_height,
            ),
        )

        # Draw enemy's health bar
        enemy_health_bar_width = int(
            self.screen.get_width() * 0.2
        )  # 20% of screen width
        enemy_health_bar_height = 20
        enemy_health_bar_x = 10  # 10 pixels from the left edge
        enemy_health_bar_y = 10  # 10 pixels from the top

        # Draw the full health background (Red)
        pygame.draw.rect(
            self.screen,
            (255, 0, 0),
            (
                enemy_health_bar_x,
                enemy_health_bar_y,
                enemy_health_bar_width,
                enemy_health_bar_height,
            ),
        )
        # Draw the current health (Green)
        pygame.draw.rect(
            self.screen,
            (0, 255, 0),
            (
                enemy_health_bar_x,
                enemy_health_bar_y,
                enemy_health_bar_width * (self.enemy_health / 100),
                enemy_health_bar_height,
            ),
        )

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.process_attack()
                elif event.key == pygame.K_ESCAPE:
                    self.running = False

        # Exit the game when one of the players has no health left
        if self.player_health == 0 or self.enemy_health == 0:
            self.running = False

    def run(self):
        print("Starting game loop")
        while self.running:
            print("Handling events")
            self.handle_events()
            print("Updating animations")
            self.update_animations()
            print("Drawing battle")
            self.draw_battle()
            print("Ticking clock")
            self.clock.tick(self.FPS)
        print("Exited game loop")


if __name__ == "__main__":
    game = Battle()
    game.run()
    pygame.quit()
