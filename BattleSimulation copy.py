import pygame
from dunwoody_disaster import ASSETS
from dunwoody_disaster.animations import AnimationClass


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
        self.background_img = pygame.image.load(ASSETS["background"]).convert()
        # Replace static sprites with animations
        user_animation_path = r"C:/Users/vuejohw/OneDrive - Dunwoody College of Technology/Documents/Data Structures/Class/DunwoodyDisaster/dunwoody_disaster/animations/Animation_Assets/idle"
        enemy_animation_path = r"C:/Users/vuejohw/OneDrive - Dunwoody College of Technology/Documents/Data Structures/Class/DunwoodyDisaster/dunwoody_disaster/animations/Animation_Assets/enemy_idle"
        # Replace static sprites with animations
        self.sprite_animation_user = AnimationClass(
            user_animation_path, 8
        )  # Assume 8 frames
        self.sprite_animation_enemy = AnimationClass(
            enemy_animation_path, 8
        )  # Assume 8 frames
        """         self.sprite_animation_user = AnimationClass(ASSETS["CooperModel"], 8)
        self.sprite_animation_enemy = AnimationClass(ASSETS["RyanRengo"], 8) """

    def setup_screen(self):
        self.screen = pygame.display.set_mode((800, 600), pygame.RESIZABLE)
        pygame.display.set_caption("Pokémon Battle Simulator")

    def update(self):
        for event in pygame.event.get():
            self.handle_events(event)
        # Update animations
        self.sprite_animation_user.update()
        self.sprite_animation_enemy.update()
        self.draw_battle()

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
        self.screen.blit(
            pygame.transform.scale(
                self.background_img, (self.screen.get_width(), self.screen.get_height())
            ),
            (0, 0),
        )
        # Draw animations
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
