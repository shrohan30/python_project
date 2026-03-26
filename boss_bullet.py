import pygame

class BossBullet:
    def __init__(self, x, y):
        self.image = pygame.Surface((12, 20))
        self.image.fill((255, 0, 0))  # red bullet
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 5

    def move(self):
        self.rect.y += self.speed

    def draw(self, screen):
        screen.blit(self.image, self.rect)