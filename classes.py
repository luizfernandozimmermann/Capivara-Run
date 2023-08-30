import pygame


class Objeto_movel:
    velocidade = 11
    constante = 1
    def mover(self : pygame.Surface, pos_final : int):
        if self.rect.right < 0:
            self.rect.x = pos_final
        self.rect.x -= int(self.velocidade * self.constante)


class Cajuzinho(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load("sprites/objetos/cajuzinho.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (100, 100))


def texto(texto):
    fonte = pygame.font.SysFont("Emulogic Regular", 60, True, False)
    texto_formatado = fonte.render(texto, True, (0, 0, 0))
    return texto_formatado


class Cajuzinho_extra(pygame.sprite.Sprite):
    def __init__(self, posição_x, posição_y):
        pygame.sprite.Sprite.__init__(self)

        self.posição = [posição_x, posição_y]
        self.image = pygame.image.load("sprites/objetos/cajuzinho.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (80, 80))


class Onça(pygame.sprite.Sprite):
    def __init__(self, posição_x, posição_y):
        pygame.sprite.Sprite.__init__(self)
        self.posição = [posição_x, posição_y]
        self.image = pygame.image.load("imagens_animação/onça_pintada.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (200, 200))


class Agua(pygame.sprite.Sprite):
    def __init__(self, imagem, posição_x, posição_y):
        pygame.sprite.Sprite.__init__(self)

        self.posição = [posição_x, posição_y]
        self.image = pygame.image.load("imagens_animação/" + str(imagem) + ".png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (240, 120))


class Easter_egg(pygame.sprite.Sprite):
    def __init__(self, posição_x, posição_y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("imagens_animação/easter_egg.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (80, 80))
        self.posição = [posição_x, posição_y]


class Logo(pygame.sprite.Sprite):
    def __init__(self, tamanho):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("sprites/extras/logo.png").convert_alpha()
        self.tamanho = tamanho
        self.image = pygame.transform.scale(self.image, (tamanho, tamanho))

    def amogus(self):
        self.image = pygame.image.load("sprites/extras/logo_sus.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.tamanho, self.tamanho))
        