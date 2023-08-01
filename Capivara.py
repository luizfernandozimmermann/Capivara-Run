import pygame

class Capivara(pygame.sprite.Sprite):
    aceleracao_y = 0
    velocidade_y = 0
    morta = False
    pulando = False

    def __init__(self, altura_inicial):
        pygame.sprite.Sprite.__init__(self)
        self.som_pulo = pygame.mixer.Sound("audios/pulo.wav")
        self.som_pulo.set_volume(0.8)
        
        self.imagens_animacoes = []
        for c in range(0, 5):
            imagem = pygame.image.load("sprites/capivarinha_" + str(c) + ".png").convert_alpha()
            imagem = pygame.transform.scale(imagem, (180, 180))
            self.imagens_animacoes.append(imagem)

        self.atual = 0
        self.image = self.imagens_animacoes[self.atual]
        self.image = pygame.transform.scale(self.image, (180, 180))
        self.movendo = False
        self.tamanho = self.image.get_size()
        self.rect = self.image.get_rect()
        self.rect.y = altura_inicial

    def transformar_amogus(self):
        self.imagens_animacoes = []
        for c in range(0, 5):
            imagem = pygame.image.load("sprites/amogus_" + str(c) + ".png").convert_alpha()
            imagem = pygame.transform.scale(imagem, (180, 180))
            self.imagens_animacoes.append(imagem)

    def zerar_gravidade(self):
        self.pulando = False
        self.aceleracao_y = 0
        self.velocidade_y = 0

    def pular(self):
        self.som_pulo.play()
        # TODO: verificar se a gravidade está boa
        self.aceleracao_y = -25

    def cair(self):
        self.aceleracao_y += 1
        self.velocidade_y += self.aceleracao_y
        self.rect.y += self.velocidade_y

    def update(self):
        if self.movendo:
            self.atual += 0.2
            if self.atual >= 4:
                self.atual = 0
            self.image = self.imagens_animacoes[int(self.atual)]
            self.image = pygame.transform.scale(self.image, (180, 180))