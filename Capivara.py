import pygame
from obstaculo import Obstaculo


class Capivara(pygame.sprite.Sprite):
    def __init__(self, altura_inicial):
        pygame.sprite.Sprite.__init__(self)
        
        self.aceleracao_y = 0
        self.morta = False
        self.pulando = False
        self.vidas = 3
        self.atual = 0
        self.tempo_invisivel = 0
        
        self.som_pulo = pygame.mixer.Sound("audios/pulo.wav")
        self.som_pulo.set_volume(0.8)
        
        self.imagens_animacoes : list[pygame.Surface] = []
        imagem0 = pygame.image.load("sprites/capivara/capivarinha_0.png").convert_alpha()
        self.imagens_animacoes.append(imagem0)

        imagem1 = pygame.image.load("sprites/capivara/capivarinha_1.png").convert_alpha()
        self.imagens_animacoes.append(imagem1)
        self.imagens_animacoes.append(imagem0)

        imagem1 = pygame.image.load("sprites/capivara/capivarinha_2.png").convert_alpha()
        self.imagens_animacoes.append(imagem1)
        self.imagens_animacoes.append(imagem0)

        for pos, imagem in enumerate(self.imagens_animacoes):
            self.imagens_animacoes[pos] = pygame.transform.scale(imagem, (180, 180))

        self.image = self.imagens_animacoes[self.atual]
        self.rect = self.image.get_rect()
        self.altura_inicial = altura_inicial
        self.rect.y = altura_inicial
        self.rect.x = 200

        self.vida_imagem = pygame.image.load("sprites/objetos/cajuzinho.png").convert_alpha()
        self.vida_imagem = pygame.transform.scale(self.vida_imagem, (100, 100))
        self.mask = pygame.mask.from_surface(self.image)

    def resetar_atributos(self):
        self.zerar_gravidade()
        self.morta = False
        self.vidas = 3
        self.rect.x = 200
        self.rect.y = self.altura_inicial
        self.tempo_invisivel = 0

    def zerar_gravidade(self):
        self.pulando = False
        self.aceleracao_y = 0

    def pular(self):
        self.som_pulo.play()
        self.pulando = True
        # TODO: verificar se a gravidade está boa
        self.aceleracao_y = -26
        self.cair()

    def cair(self):
        self.aceleracao_y += 1
        self.rect.y += self.aceleracao_y

    def update(self, altura_tela):
        if self.tempo_invisivel == 0:
            self.atual += 0.2
            if self.atual >= 4:
                self.atual = 0
            self.image = self.imagens_animacoes[int(self.atual)]
            self.image = pygame.transform.scale(self.image, (180, 180))
        else:
            self.image = pygame.Surface((0, 0))
            self.tempo_invisivel += 1
            if self.tempo_invisivel == 15:
                self.tempo_invisivel = 0
        
        # gravidade
        if self.rect.bottom < altura_tela - 120:
            self.cair()
            if self.rect.bottom > altura_tela - 120:
                self.rect.bottom = altura_tela - 120
        else:
            self.zerar_gravidade()
        
    def colidiu(self, obstaculo : Obstaculo) -> bool:
        return pygame.sprite.collide_mask(self, obstaculo) != None
        