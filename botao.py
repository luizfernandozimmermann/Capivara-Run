from typing import Callable
import pygame


class Botao(pygame.sprite.Sprite):
    def __init__(self, imagem : str, x : int, y : int, tamanho : int, funcao : Callable = None):
        pygame.sprite.Sprite.__init__(self)
        
        self.som_botao = pygame.mixer.Sound("audios/botao_audio.wav")
        self.som_botao.set_volume(0.6)
        self.image = pygame.image.load(f"sprites/botoes/botao_{imagem}.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (tamanho, tamanho))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.funcao = funcao
        
    def click(self):
        self.som_botao.play()
        if self.funcao is not None:
            self.funcao()
        