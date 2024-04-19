import pygame


class Fighter:
    def __init__(self, x, y):
        self.rect = pygame.Rect((x, y, 80, 180))
        self.vel_y = 0
        self.jump = False
        self.attacking = False
        self.attack_type = 0
        self.health = 100

    # movement method
    def move(self, Screen_Width, Screen_Height, surface, target):
        SPEED = 10
        GRAVITY = 2
        dx = 0
        dy = 0

        # get keypresses
        key = pygame.key.get_pressed()

        # can only perform other actions if not currently attacking
        if self.attacking == False:
            # movement
            if key[pygame.K_a]:
                dx = -SPEED
            if key[pygame.K_d]:
                dx = SPEED

            # jump movement
            if key[pygame.K_w] and self.jump == False:
                self.vel_y = -30
                self.jump = True

            # attack moves
            if key[pygame.K_r] or key[pygame.K_t]:
                self.attack(surface, target)

                # determine which attack type was used
                if key[pygame.K_r]:
                    self.attack_type = 1
                if key[pygame.K_t]:
                    self.attack_type = 2

        # apply gravity
        self.vel_y += GRAVITY
        dy += self.vel_y

        # Screen Limitation
        if self.rect.left + dx < 0:
            dx = -self.rect.left

        if self.rect.right + dx > Screen_Width:
            dx = Screen_Width - self.rect.right

        if self.rect.bottom + dy > Screen_Height - 110:
            self.vel_y = 0
            dy = Screen_Height - 110 - self.rect.bottom
            self.jump = False
        # update player position
        self.rect.x += dx
        self.rect.y += dy

    def attack(self, surface, target):
        self.attacking = True
        attacking_rect = pygame.Rect(
            self.rect.centerx, self.rect.y, 2 * self.rect.width, self.rect.height
        )
        if attacking_rect.colliderect(target.rect):
            print("hit")
            target.health -= 10

        pygame.draw.rect(surface, (0, 255, 0), attacking_rect)

    def draw(self, surface):
        pygame.draw.rect(surface, (255, 0, 0), self.rect)
