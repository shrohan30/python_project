import pygame

class BossBullet:
    def __init__(self, x, y):
        self.image = pygame.image.load("assets/boss_bullet.png")
        self.image = pygame.transform.scale(self.image, (30, 40))  # adjust size
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 6

    def move(self):
        self.rect.y += self.speed

    def draw(self, screen):
        screen.blit(self.image, self.rect)