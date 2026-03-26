import pygame

class Boss:
    def __init__(self, x, y, level=1):
        self.level = level
        # Load image based on level
        self.image = pygame.image.load(f"assets/boss{level}.png").convert_alpha()
        self.rect = self.image.get_rect(topleft=(x, y))
        # Set health and speed per level
        self.health = 30 + (level - 1) * 20  # 30, 50, 70
        self.speed = 2 + (level - 1)  # optional: level 1 speed=2, level 2=3, level3=4

    def move(self):
        # Example: horizontal patrol
        self.rect.x += self.speed
        if self.rect.right >= 1000 or self.rect.left <= 0:
            self.speed = -self.speed

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))