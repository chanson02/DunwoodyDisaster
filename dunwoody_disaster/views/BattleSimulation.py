import pygame
import sys


class Game:
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
        self.background_img = pygame.image.load(
            "Class/DunwoodyDisaster/dunwoody_disaster/assets/background.jpg"
        ).convert()
        self.sprite_image_user = pygame.image.load(
            "Class/DunwoodyDisaster/dunwoody_disaster/assets/CooperModel.png"
        ).convert_alpha()
        self.sprite_image_enemy = pygame.image.load(
            "Class/DunwoodyDisaster/dunwoody_disaster/assets/RyanRengo.jpg"
        ).convert_alpha()

    def setup_screen(self):
        self.screen = pygame.display.set_mode((800, 600), pygame.RESIZABLE)
        pygame.display.set_caption("Pokémon Battle Simulator")

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

        # Draw the full health background (green)
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
        # Draw the current health (red)
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

        # Draw the full health background (green)
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
        # Draw the current health (red)
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

    def draw_battle(self):
        scaled_bg = pygame.transform.scale(
            self.background_img, (self.screen.get_width(), self.screen.get_height())
        )
        self.screen.blit(scaled_bg, (0, 0))

        UserSprite_pos = (
            int(self.screen.get_width() * 0.23),
            int(self.screen.get_height() * 0.60),
        )
        EnemySprite_pos = (
            int(self.screen.get_width() * 0.70),
            int(self.screen.get_height() * 0.25),
        )

        user_sprite_scaled = pygame.transform.scale(self.sprite_image_user, (80, 100))
        enemy_sprite_scaled = pygame.transform.scale(
            self.sprite_image_enemy, (100, 100)
        )

        self.screen.blit(user_sprite_scaled, UserSprite_pos)
        self.screen.blit(enemy_sprite_scaled, EnemySprite_pos)

        self.draw_health_bars()
        pygame.display.flip()

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.VIDEORESIZE:
                    self.screen = pygame.display.set_mode(
                        (event.w, event.h), pygame.RESIZABLE
                    )
                self.handle_events(event)
            self.draw_battle()
            self.clock.tick(self.FPS)
        pygame.quit()
        sys.exit()

    def handle_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if self.player_turn:
                    self.enemy_health = max(self.enemy_health - 20, 0)
                else:
                    self.player_health = max(self.player_health - 20, 0)
                self.player_turn = not self.player_turn


if __name__ == "__main__":
    game = Game()
    game.run()
