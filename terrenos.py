import pygame
from classes import Objeto_movel


class FundoTerreno(pygame.sprite.Sprite, Objeto_movel):
    def __init__(self, x, altura_tela):
        pygame.sprite.Sprite.__init__(self)

        self.constante = 0.5
        self.image = pygame.image.load("sprites/terrenos/tela_de_fundo.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (altura_tela, altura_tela))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = -120  # para não ficar atrás do chão
        

class FundoNuvem(pygame.sprite.Sprite, Objeto_movel):
    def __init__(self, x, altura_tela):
        pygame.sprite.Sprite.__init__(self)

        self.constante = 0.2
        self.image = pygame.image.load("sprites/terrenos/nuvens.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (altura_tela, altura_tela))
        self.rect = self.image.get_rect()
        self.rect.x = x


class Chao(pygame.sprite.Sprite, Objeto_movel):
    def __init__(self, x, altura_tela):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load("sprites/terrenos/terra.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (240, 120))
        self.rect = self.image.get_rect()
        self.rect.x = 240 * x
        self.rect.y = altura_tela - 120
