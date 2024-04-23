import pygame
from dunwoody_disaster import ASSETS


class Game:
    def __init__(self):
        # self.test = test
        self.should_render = False
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
        self.background_img = pygame.image.load(ASSETS["background"]).convert()
        self.sprite_image_user = pygame.image.load(
            ASSETS["CooperModel"]
        ).convert_alpha()
        self.sprite_image_enemy = pygame.image.load(ASSETS["RyanRengo"]).convert_alpha()

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

    def draw_battle(self):
        # Scale the background image to fit the current size of the screen.
        scaled_bg = pygame.transform.scale(
            self.background_img, (self.screen.get_width(), self.screen.get_height())
        )
        # Blit (copy) the scaled background image onto the screen at position (0, 0).
        self.screen.blit(scaled_bg, (0, 0))

        # Calculate positions for user and enemy sprites as a percentage of screen size.
        UserSprite_pos = (
            int(self.screen.get_width() * 0.23),
            int(self.screen.get_height() * 0.60),
        )
        EnemySprite_pos = (
            int(self.screen.get_width() * 0.70),
            int(self.screen.get_height() * 0.25),
        )

        # Scale the user sprite image to a fixed size of (80, 100) pixels.
        user_sprite_scaled = pygame.transform.scale(self.sprite_image_user, (80, 100))
        # Scale the enemy sprite image to a fixed size of (100, 100) pixels.
        enemy_sprite_scaled = pygame.transform.scale(
            self.sprite_image_enemy, (100, 100)
        )

        # Blit the scaled user sprite to the calculated position on the screen.
        self.screen.blit(user_sprite_scaled, UserSprite_pos)
        # Blit the scaled enemy sprite to the calculated position on the screen.
        self.screen.blit(enemy_sprite_scaled, EnemySprite_pos)

        self.draw_health_bars()
        pygame.display.flip()

    def update(self):
        for event in pygame.event.get():
            self.handle_events(event)
        self.draw_battle()

    def to_bytes(self):
        return pygame.image.tobytes(self.screen, "RGB")

    def quit(self):
        pygame.quit()

    # def run(self):
    #     while self.running:
    #         for event in pygame.event.get():
    #             if event.type == pygame.QUIT:
    #                 self.running = False
    #             elif event.type == pygame.VIDEORESIZE:
    #                 self.screen = pygame.display.set_mode(
    #                     (event.w, event.h), pygame.RESIZABLE
    #                 )
    #             self.handle_events(event)
    #         self.draw_battle()
    #         # pygame.image.save(self.screen, '/home/chanson/Desktop/test.png')
    #         # img_bytes = pygame.image.tobytes(self.screen, 'P')
    #         if self.should_render:
    #             img_bytes = pygame.image.tobytes(self.screen, 'RGB')
    #             #img_bytes = pygame.image.tobytes(self.screen, 'ARGB')
    #             #img_bytes = pygame.image.tobytes(self.screen, 'RGBA')
    #             #img_bytes = pygame.image.tostring(self.screen, 'RGB')
    #             self.test.test_update_pyside(img_bytes)
    #
    #         self.clock.tick(self.FPS)
    #     pygame.quit()
    #     #sys.exit()

    def handle_events(self, event):
        self.should_render = False
        # Check if the event is a key press.
        if event.type == pygame.KEYDOWN:
            # If the spacebar is pressed, process an attack.
            if self.player_turn:
                self.enemy_health = max(self.enemy_health - 20, 0)
                print("Player attacked")
                self.should_render = True
            else:
                self.player_health = max(self.player_health - 20, 0)
                print("Enemy Attacked")
                self.should_render = True
            self.player_turn = not self.player_turn


if __name__ == "__main__":
    game = Game()
    game.run()
