import pygame

class Enemy:

    def __init__(self,x,y):
        
        self.image = pygame.image.load("assets/enemy.png")
        self.rect = self.image.get_rect(topleft=(x,y))
        self.speed = 3

    def move(self):
        self.rect.y += self.speed

    def draw(self,screen):
        screen.blit(self.image,self.rect)