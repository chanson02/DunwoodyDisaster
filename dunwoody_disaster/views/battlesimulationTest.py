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

    def setup_screen(self):
        self.screen = pygame.display.set_mode((800, 600), pygame.RESIZABLE)
        pygame.display.set_caption("Pokémon Battle Simulator")

    def draw_battle(self):
        # Scale the background
        scaled_bg = pygame.transform.scale(
            self.background_img, (self.screen.get_width(), self.screen.get_height())
        )
        self.screen.blit(scaled_bg, (0, 0))

        User_Sprite_x = 0.23
        User_Sprite_y = 0.60

        Enemy_Sprite_x = 0.90
        Enemy_Sprite_y = 0.25

        # Calculate the position of the user sprite on current screen size
        UserSprite_pos_x = int(self.screen.get_width() * User_Sprite_x)
        UserSprite_pos_y = int(self.screen.get_height() * User_Sprite_y)

        # Calculate the position of the enemy sprite on current screen size
        EnemySprite_pos_x = int(self.screen.get_height() * Enemy_Sprite_x)
        EnemySprite_pos_y = int(self.screen.get_height() * Enemy_Sprite_y)

        # User Sprite Loadout
        sprite_image_user = pygame.image.load(
            "Class/DunwoodyDisaster/dunwoody_disaster/assets/CooperModel.png"
        ).convert_alpha()
        sprite_image_user = pygame.transform.scale(
            sprite_image_user, (100, 100)
        )  # Scaling sprite to a fixed size, adjust as needed

        # Draw the sprite at the calculated position
        self.screen.blit(sprite_image_user, (UserSprite_pos_x, UserSprite_pos_y))

        # Enemy Sprite Loadout
        sprite_image_enemy = pygame.image.load(
            "Class/DunwoodyDisaster/dunwoody_disaster/assets/RyanRengo.jpg"
        ).convert_alpha()
        sprite_image_enemy = pygame.transform.scale(
            sprite_image_enemy, (100, 100)
        )  # Scaling sprite to a fixed size, adjust as needed

        # Draw enemy sprite at calculated location
        self.screen.blit(sprite_image_enemy, (EnemySprite_pos_x, EnemySprite_pos_y))

        # Update the display
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
            # pygame.image.save(self.screen, '/home/chanson/Desktop/test.png')
            print('saved')
            self.clock.tick(self.FPS)
        pygame.quit()
        sys.exit()

    def handle_events(self, event):
        # Handle keypresses and other events
        pass


class Battle(Game):
    def __init__(self):
        super().__init__()
        self.player_health = 100
        self.enemy_health = 100
        self.player_turn = True

    def draw_battle(self):
        # Draw the background
        self.screen.blit(self.background_img, (0, 0))

        # Draw the player's health bar
        player_health_bar_width = int(self.screen.get_width() * 0.2)
        player_health_bar_height = 20
        player_health_bar_x = self.screen.get_width() - player_health_bar_width - 10
        player_health_bar_y = self.screen.get_height() - player_health_bar_height - 10
        pygame.draw.rect(
            self.screen,
            (0, 255, 0),
            (
                player_health_bar_x,
                player_health_bar_y,
                player_health_bar_width,
                player_health_bar_height,
            ),
        )
        pygame.draw.rect(
            self.screen,
            (255, 0, 0),
            (
                player_health_bar_x,
                player_health_bar_y,
                player_health_bar_width * (self.player_health / 100),
                player_health_bar_height,
            ),
        )

        # Draw the enemy's health bar
        enemy_health_bar_width = int(self.screen.get_width() * 0.2)
        enemy_health_bar_height = 20
        enemy_health_bar_x = 10
        enemy_health_bar_y = self.screen.get_height() - enemy_health_bar_height - 10
        pygame.draw.rect(
            self.screen,
            (0, 255, 0),
            (
                enemy_health_bar_x,
                enemy_health_bar_y,
                enemy_health_bar_width,
                enemy_health_bar_height,
            ),
        )
        pygame.draw.rect(
            self.screen,
            (255, 0, 0),
            (
                enemy_health_bar_x,
                enemy_health_bar_y,
                enemy_health_bar_width * (self.enemy_health / 100),
                enemy_health_bar_height,
            ),
        )

        # Draw the player's and


if __name__ == "__main__":
    game = Game()
    game.run()
