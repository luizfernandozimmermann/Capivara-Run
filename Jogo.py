from datetime import datetime, timedelta
import math
import pygame
from pygame.locals import *

from capivara import Capivara
from terrenos import *
from obstaculo import Obstaculo
from botao import Botao

from save_and_load import *
from classes import *
from random import randint
from sys import exit


class Jogo():
    pontuacao = 0
    def __init__(self, tela : pygame.Surface):
        self.tela = tela
        self.largura_tela = self.tela.get_width()
        self.altura_tela = self.tela.get_height()

        self.relogio = pygame.time.Clock()
        self.fps = 60

        self.pontuacao_maxima = carregar()["pontuacao_maxima"]
        
        self.carregar_audios()

        while True:
            # TODO: self.carregar_menu()
            self.carregar_jogo()

    def carregar_audios(self):
        self.som_amogus = pygame.mixer.Sound("audios/amogus.wav")
        self.som_amogus.set_volume(0.05)

        self.som_colisao_cacto = pygame.mixer.Sound("audios/dano_cacto.wav")
        self.som_colisao_cacto.set_volume(0.2)

        self.som_cajuzinho_extra = pygame.mixer.Sound("audios/cajuzinho_extra.wav")
        self.som_cajuzinho_extra.set_volume(1)

        self.som_morte = pygame.mixer.Sound("audios/morte.wav")
        self.som_morte.set_volume(0.1)

        

        self.som_onça_chegando = pygame.mixer.Sound("audios/onça_chegando.wav")
        self.som_onça_chegando.set_volume(0.1)

        self.som_botao = pygame.mixer.Sound("audios/botões_audio.wav")
        self.som_botao.set_volume(0.6)

    def carregar_jogo(self):
        # caracteristicas do jogo
        self.pontuacao = 0
        
        # botao
        botao_pausar = Botao("pause", self.largura_tela - 128, 0, 128)

        # capivara
        capivara = Capivara(self.altura_tela - 301)

        # Terrenos
        fundos : list[FundoTerreno] = []
        nuvens : list[FundoNuvem] = []
        quantidade_imagens_fundo = math.ceil(self.largura_tela / self.altura_tela) + 1
        for i in range(0, quantidade_imagens_fundo):
            posicao_x = i * self.altura_tela
            fundo = FundoTerreno(posicao_x, self.altura_tela)
            fundos.append(fundo)

            nuvem = FundoNuvem(posicao_x, self.altura_tela)
            nuvens.append(nuvem)

        solos : list[Chao] = []
        quantidade_solo = math.ceil(self.largura_tela / 240) + 2
        for i in range(0, quantidade_solo):
            solo = Chao(i, self.altura_tela)
            solos.append(solo)

        # cactos
        cactos : list[Obstaculo] = []
        tempo_ultimo_cacto = datetime.now()

        while True:
            self.tela.fill((50, 50, 50))
            self.relogio.tick(self.fps)
            x_mouse, y_mouse = pygame.mouse.get_pos()

            if botao_pausar.rect.collidepoint(x_mouse, y_mouse) and pygame.mouse.get_pressed()[0]:
                self.pausar()
                
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    exit()
                
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        self.pausar()
            
            if Objeto_movel.velocidade < 22.5:
                Objeto_movel.velocidade += 0.005
                
            self.pontuacao += int(Objeto_movel.velocidade)
            if self.pontuacao > self.pontuacao_maxima:
                self.pontuacao_maxima = self.pontuacao

            # movimentação da tela de fundo, nuvens e solos
            for pos, nuvem in enumerate(nuvens):
                nuvem.mover(nuvens[pos - 1].rect.right)
                self.tela.blit(nuvem.image, nuvem.rect.topleft)
            
            for pos, fundo in enumerate(fundos):
                fundo.mover(fundos[pos - 1].rect.right)
                self.tela.blit(fundo.image, fundo.rect.topleft)

            for pos, solo in enumerate(solos):
                solo.mover(solos[pos - 1].rect.right)
                self.tela.blit(solo.image, solo.rect.topleft)

            # carregamento das vidas
            for c in range(0, capivara.vidas):
                self.tela.blit(capivara.vida_imagem, (c * 100 + 20, 20))
            
            # update da capivara
            capivara.update(self.altura_tela)
            
            # pulo
            pular = pygame.key.get_pressed()[K_w] or pygame.key.get_pressed()[K_SPACE] or \
                pygame.key.get_pressed()[K_UP] or \
                (pygame.mouse.get_pressed()[0] and not botao_pausar.rect.collidepoint(x_mouse, y_mouse))
            if not capivara.pulando and pular:
                capivara.pular()
                
            # geração e carregamento dos cactos
            tempo_agora = datetime.now()
            if tempo_agora - tempo_ultimo_cacto > timedelta(0, 3 - Objeto_movel.velocidade / 11.25):
                cactos.append(Obstaculo(self.altura_tela, self.largura_tela))
                tempo_ultimo_cacto = tempo_agora
                
            for cacto in cactos:
                cacto.mover()
                self.tela.blit(cacto.image, cacto.rect.topleft)
                if capivara.colidiu(cacto) and not cacto.ja_colidiu:
                    self.som_colisao_cacto.play()
                    capivara.vidas -= 1
                    capivara.tempo_invisivel += 1
                    cacto.ja_colidiu = True
                    if capivara.vidas == 0:
                        self.finalizar_jogo()
                        return
                if cacto.rect.right < 0:
                    cactos.remove(cacto)
                
            pontuacao_texto = texto(f"Pontuação: {str(self.pontuacao)}")
            pontuacao_maxima_texto = texto(f"Recorde: {str(self.pontuacao_maxima)}")
            
            self.tela.blit(pontuacao_texto, (20, self.altura_tela - 60))
            self.tela.blit(pontuacao_maxima_texto, (self.largura_tela // 2, self.altura_tela - 60))
            self.tela.blit(capivara.image, capivara.rect.topleft)
            self.tela.blit(botao_pausar.image, botao_pausar.rect)

            pygame.display.update()
            
    def finalizar_jogo(self):
        if self.pontuacao == self.pontuacao_maxima:
            self.pontuacao_maxima = self.pontuacao
            conteudo = carregar()
            conteudo["pontuacao_maxima"] = self.pontuacao
            salvar(conteudo)

    def pausar(self):
        while True:
            self.tela.fill((50, 50, 50))
            self.relogio.tick(self.fps)
            x_mouse, y_mouse = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    exit()
                    
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        return

            pygame.display.update()
            