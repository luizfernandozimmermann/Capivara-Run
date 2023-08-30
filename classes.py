import pygame


class Objeto_movel:
    velocidade = 11
    constante = 1
    def mover(self : pygame.Surface, pos_final : int):
        if self.rect.right < 0:
            self.rect.x = pos_final
        self.rect.x -= int(self.velocidade * self.constante)


def texto(texto):
    fonte = pygame.font.SysFont("Emulogic Regular", 60, True, False)
    texto_formatado = fonte.render(texto, True, (0, 0, 0))
    return texto_formatado
