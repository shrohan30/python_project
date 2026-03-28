import pygame

class PowerUp:

    def __init__(self,x,y):
        
        self.image = pygame.image.load("assets/powerup.png")
        self.rect = self.image.get_rect(center=(x,y))
        self.speed = 3

    def move(self):
        self.rect.y += self.speed

    def draw(self,screen):
        screen.blit(self.image,self.rect)