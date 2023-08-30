from random import randint
import pygame
from classes import Objeto_movel


class Obstaculo(pygame.sprite.Sprite, Objeto_movel):
    def __init__(self, altura_tela, largura_tela):
        pygame.sprite.Sprite.__init__(self)
        
        self.variante = randint(1, 3)
        self.image = pygame.image.load(f"sprites/objetos/cacto_{self.variante}.png").convert_alpha()
        self.image = pygame.transform.scale(
            self.image, ((self.image.get_width() // 32) * 100, (self.image.get_height() // 32) * 100))
        self.rect = self.image.get_rect()
        self.rect.y = altura_tela - 120 - self.rect.height
        self.rect.x = largura_tela
        self.mask  = pygame.mask.from_surface(self.image)
        
        self.ja_colidiu = False
        
    def mover(self):
        self.rect.x -= int(self.velocidade * self.constante)
