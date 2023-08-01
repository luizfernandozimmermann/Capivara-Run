import pygame





class Cacto(pygame.sprite.Sprite):
    def __init__(self, imagem, tamanho, largura_tela, altura_tela, proporção_altura=1, proporção_largura=1):
        pygame.sprite.Sprite.__init__(self)

        self.proporção = proporção_altura
        self.largura = proporção_largura
        self.tamanho = [tamanho * proporção_largura, tamanho * proporção_altura]
        self.image = pygame.image.load("sprites/objetos/cacto_" + str(imagem) + ".png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.tamanho[0], self.tamanho[1]))
        self.posição = [largura_tela, altura_tela - self.tamanho[0] - 110 - tamanho * (proporção_altura - 1)]
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.posição[0], self.posição[1])


class Botão(pygame.sprite.Sprite):
    def __init__(self, imagem, x, y, tamanho):
        pygame.sprite.Sprite.__init__(self)

        self.tamanho = tamanho
        self.posição = [x, y]
        self.image = pygame.image.load("sprites/botoes/botão_" + str(imagem) + ".png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (tamanho, tamanho))


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