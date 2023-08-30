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

        self.jogar()

    def carregar_audios(self):
        self.som_colisao_cacto = pygame.mixer.Sound("audios/dano_cacto.wav")
        self.som_colisao_cacto.set_volume(0.2)

        self.som_morte = pygame.mixer.Sound("audios/morte.wav")
        self.som_morte.set_volume(0.1)
        
        pygame.mixer.music.set_volume(0.05)
        self.musica_de_fundo = pygame.mixer.music.load("audios/musica_de_fundo.mp3")
        pygame.mixer.music.play(-1)  

    def carregar_fundos_e_obstaculos(self):
        # Terrenos
        self.fundos : list[FundoTerreno] = []
        self.nuvens : list[FundoNuvem] = []
        quantidade_imagens_fundo = math.ceil(self.largura_tela / self.altura_tela) + 1
        for i in range(0, quantidade_imagens_fundo):
            posicao_x = i * self.altura_tela
            fundo = FundoTerreno(posicao_x, self.altura_tela)
            self.fundos.append(fundo)

            nuvem = FundoNuvem(posicao_x, self.altura_tela)
            self.nuvens.append(nuvem)

        self.solos : list[Chao] = []
        quantidade_solo = math.ceil(self.largura_tela / 240) + 2
        for i in range(0, quantidade_solo):
            solo = Chao(i, self.altura_tela)
            self.solos.append(solo)

        # cactos
        self.cactos : list[Obstaculo] = []

    def jogar(self):
        # caracteristicas do jogo
        self.pontuacao = 0
        
        # botao
        botao_pausar = Botao("pause", self.largura_tela - 128, 0, 128, self.pausar)

        # self.capivara
        self.capivara = Capivara(self.altura_tela - 301)

        #Terrenos
        self.carregar_fundos_e_obstaculos()
        tempo_ultimo_cacto = datetime.now()

        while True:
            self.tela.fill((50, 50, 50))
            self.relogio.tick(self.fps)
            x_mouse, y_mouse = pygame.mouse.get_pos()

            if botao_pausar.rect.collidepoint(x_mouse, y_mouse) and pygame.mouse.get_pressed()[0]:
                botao_pausar.click()
                
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
            for pos, nuvem in enumerate(self.nuvens):
                nuvem.mover(self.nuvens[pos - 1].rect.right)
                self.tela.blit(nuvem.image, nuvem.rect.topleft)
            
            for pos, fundo in enumerate(self.fundos):
                fundo.mover(self.fundos[pos - 1].rect.right)
                self.tela.blit(fundo.image, fundo.rect.topleft)

            for pos, solo in enumerate(self.solos):
                solo.mover(self.solos[pos - 1].rect.right)
                self.tela.blit(solo.image, solo.rect.topleft)

            # carregamento das vidas
            for c in range(0, self.capivara.vidas):
                self.tela.blit(self.capivara.vida_imagem, (c * 100 + 20, 20))
            
            # update da self.capivara
            self.capivara.update(self.altura_tela)
            
            # pulo
            pular = pygame.key.get_pressed()[K_w] or pygame.key.get_pressed()[K_SPACE] or \
                pygame.key.get_pressed()[K_UP] or \
                (pygame.mouse.get_pressed()[0] and not botao_pausar.rect.collidepoint(x_mouse, y_mouse))
            if not self.capivara.pulando and pular:
                self.capivara.pular()
                
            # geração e carregamento dos cactos
            tempo_agora = datetime.now()
            if tempo_agora - tempo_ultimo_cacto > timedelta(0, 3 - Objeto_movel.velocidade / 11.25):
                self.cactos.append(Obstaculo(self.altura_tela, self.largura_tela))
                tempo_ultimo_cacto = tempo_agora
                
            for cacto in self.cactos:
                cacto.mover()
                self.tela.blit(cacto.image, cacto.rect.topleft)
                if self.capivara.colidiu(cacto) and not cacto.ja_colidiu:
                    self.som_colisao_cacto.play()
                    self.capivara.vidas -= 1
                    self.capivara.tempo_invisivel += 1
                    cacto.ja_colidiu = True
                    if self.capivara.vidas == 0:
                        self.morte()
                        
            for cacto in self.cactos:
                if cacto.rect.right < 0:
                    self.cactos.remove(cacto)
                
            pontuacao_texto = texto(f"Pontuação: {str(self.pontuacao)}")
            pontuacao_maxima_texto = texto(f"Recorde: {str(self.pontuacao_maxima)}")
            
            self.tela.blit(pontuacao_texto, (20, self.altura_tela - 60))
            self.tela.blit(pontuacao_maxima_texto, (self.largura_tela // 2, self.altura_tela - 60))
            self.tela.blit(self.capivara.image, self.capivara.rect.topleft)
            self.tela.blit(botao_pausar.image, botao_pausar.rect)

            pygame.display.update()
            
    def finalizar_jogo(self):
        if self.pontuacao == self.pontuacao_maxima:
            self.pontuacao_maxima = self.pontuacao
            conteudo = carregar()
            conteudo["pontuacao_maxima"] = self.pontuacao
            salvar(conteudo)

    def morte(self):
        self.som_morte.play()
        
        botao_restart   = Botao("restart", 
                                (self.largura_tela - (128 * 2 + 50 * 1)) // 2 + (128 + 50) * 0, 
                                (self.altura_tela - 128) // 2, 128, self.resetar)
        botao_sair      = Botao("sair", 
                                (self.largura_tela - (128 * 2 + 50 * 1)) // 2 + (128 + 50) * 1, 
                                (self.altura_tela - 128) // 2, 128, exit)
        
        botoes : pygame.sprite.Group[Botao] = pygame.sprite.Group(
            botao_restart,
            botao_sair
        )
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
                    
            if pygame.mouse.get_pressed()[0]:                
                if botao_restart.rect.collidepoint(x_mouse, y_mouse):
                    botao_restart.click()
                    return
                
                if botao_sair.rect.collidepoint(x_mouse, y_mouse):
                    botao_sair.click()
                    
            for botao in botoes:
                self.tela.blit(botao.image, botao.rect.topleft)

            pygame.display.update()
    
    def pausar(self):
        botao_continuar = Botao("continuar", 
                                (self.largura_tela - (128 * 3 + 50 * 2)) // 2 + (128 + 50) * 0, 
                                (self.altura_tela - 128) // 2, 128)
        botao_restart   = Botao("restart", 
                                (self.largura_tela - (128 * 3 + 50 * 2)) // 2 + (128 + 50) * 1, 
                                (self.altura_tela - 128) // 2, 128, self.resetar)
        botao_sair      = Botao("sair", 
                                (self.largura_tela - (128 * 3 + 50 * 2)) // 2 + (128 + 50) * 2, 
                                (self.altura_tela - 128) // 2, 128, exit)
        
        botoes : pygame.sprite.Group[Botao] = pygame.sprite.Group(
            botao_continuar,
            botao_restart,
            botao_sair
        )

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
                    
            if pygame.mouse.get_pressed()[0]:
                if botao_continuar.rect.collidepoint(x_mouse, y_mouse):
                    botao_continuar.click()
                    return
                
                if botao_restart.rect.collidepoint(x_mouse, y_mouse):
                    botao_restart.click()
                    return
                
                if botao_sair.rect.collidepoint(x_mouse, y_mouse):
                    botao_sair.click()
                    
            for botao in botoes:
                self.tela.blit(botao.image, botao.rect.topleft)
                
            pygame.display.update()
            
    def resetar(self):
        self.capivara.resetar_atributos()
        self.finalizar_jogo()
        self.pontuacao = 0
        Objeto_movel.velocidade = 11
        self.carregar_fundos_e_obstaculos()
            