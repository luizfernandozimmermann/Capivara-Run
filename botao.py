import pygame


class Botao(pygame.sprite.Sprite):
    def __init__(self, imagem : str, x : int, y : int, tamanho : int):
        pygame.sprite.Sprite.__init__(self)
        
        self.image = pygame.image.load(f"sprites/botoes/botao_{imagem}.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (tamanho, tamanho))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        