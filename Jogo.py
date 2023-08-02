import math
import pygame
from pygame.locals import *

from Capivara import Capivara
from terrenos import *

from classes import *
from random import randint
from sys import exit


class Jogo():
    def __init__(self, tela):
        self.tela = tela
        self.largura_tela = self.tela.get_width()
        self.altura_tela = self.tela.get_height()

        self.relogio = pygame.time.Clock()
        self.fps = 60
        
        self.carregar_audios()

        self.carregar_jogo()

    def carregar_audios(self):
        self.som_amogus = pygame.mixer.Sound("audios/amogus.wav")
        self.som_amogus.set_volume(0.05)

        self.som_colisão_cacto = pygame.mixer.Sound("audios/dano_cacto.wav")
        self.som_colisão_cacto.set_volume(0.2)

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
        click = False
        pontuação = 0
        pontuação_maxima = 0
        temporizador = 0
        pausado = False
        inicio = True
        reinicio_agora = False

        # sons
        easter_egg = Easter_egg(0, self.altura_tela - 80)
        tocar_amogus = False

        # capivara
        imagem_vazio = pygame.image.load("sprites/vazio.png").convert_alpha()
        colisão_com_cacto = False
        capivara = Capivara(self.altura_tela - 301)
        morte = False

        

        aguas = []
        agua_entrada = Agua("agua_entrada", 0, self.altura_tela - 120)
        aguas.append(agua_entrada)
        agua_meio1 = Agua("agua_meio", 240, self.altura_tela - 120)
        aguas.append(agua_meio1)
        agua_meio2 = Agua("agua_meio", 480, self.altura_tela - 120)
        aguas.append(agua_meio2)
        agua_saida = Agua("agua_saida", 480 + 240, self.altura_tela - 120)
        aguas.append(agua_saida)

        # cajuzinho
        cajuzinho = Cajuzinho()
        cajuzinho_extra = Cajuzinho_extra(self.largura_tela, self.altura_tela - 120 - 80 - 30)
        cajuzinho_extra_na_tela = False

        # Terrenos
        fundos = []
        nuvens = []
        quantidade_imagens_fundo = math.ceil(self.largura_tela / self.altura_tela) + 1
        for i in range(0, quantidade_imagens_fundo):
            posicao_x = i * self.altura_tela
            fundo = FundoTerreno(posicao_x, self.altura_tela)
            fundos.append(fundo)

            nuvem = FundoNuvem(posicao_x, self.altura_tela)
            nuvens.append(nuvem)

        solos = []
        quantidade_solo = math.ceil(self.largura_tela / 240) + 1
        for i in range(0, quantidade_solo):
            solo = Chao(i, self.altura_tela)
            solos.append(solo)

        # cactos
        cactos_colocados_em_campo = []

        cacto_tipo1 = Cacto(1, 100, self.largura_tela, self.altura_tela, 1, 1)
        cactos_colocados_em_campo.append(cacto_tipo1)

        cacto_tipo2 = Cacto(2, 100, self.largura_tela, self.altura_tela, 2, 1)
        cacto_tipo3 = Cacto(3, 100, self.largura_tela, self.altura_tela, 1, 2)

        # botões quando pausado e pausar
        tamanho_botões = 160
        botão_continuar = Botão("continuar", 100, (self.altura_tela - tamanho_botões) // 2, tamanho_botões)
        botão_reiniciar =Botão("restart", self.largura_tela // 2 - tamanho_botões // 2, (self.altura_tela - tamanho_botões) // 2, tamanho_botões)
        botão_sair = Botão("sair", self.largura_tela - 100 - tamanho_botões, (self.altura_tela - tamanho_botões) // 2, tamanho_botões)
        botão_pausar = Botão("pause", self.largura_tela - tamanho_botões + 40 - 20, 20, tamanho_botões - 40)
        dentro = False

        # logo
        logo = Logo(self.altura_tela // 3 * 2)

        while True:
            self.tela.fill((50, 50, 50))
            self.relogio.tick(self.fps)
            x_mouse, y_mouse = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    exit()
                
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE and not inicio:
                        if pausado:
                            pausado = False
                        else:
                            pausado = True
                    
                if event.type == MOUSEBUTTONDOWN:
                    click = True

            # O JOGO TA AQUI XDD
            if not pausado and not morte:
                # movimentação da tela de fundo e nuvens
                for pos, nuvem in enumerate(nuvens):
                    nuvem.mover()
                    if nuvem.rect.right < 0:
                        nuvem.rect.x = nuvens[pos - 1].rect.right - 2
                    
                    self.tela.blit(nuvem.image, nuvem.rect.topleft)
                
                for pos, fundo in enumerate(fundos):
                    fundo.mover()
                    if fundo.rect.right < 0:
                        fundo.rect.x = fundos[pos - 1].rect.right - 5
                    
                    self.tela.blit(fundo.image, fundo.rect.topleft)

                # movimentação do solo
                for pos, solo in enumerate(solos):
                    solo.mover()
                    if solo.rect.right < 0:
                        solo.rect.x = solos[pos - 1].rect.right - 10
                    
                    self.tela.blit(solo.image, solo.rect.topleft)

                # carregamento dos cajuzinho
                for c in range(0, capivara.vidas):
                    self.tela.blit(cajuzinho.image, (c * 100 + 20, 20))
                
                
                # deletando cactos que ja foram
                try:
                    for c in range(0, len(cactos_colocados_em_campo)):
                        if cactos_colocados_em_campo[c].posição[0] + cactos_colocados_em_campo[c].tamanho[0] < 0:
                            del cactos_colocados_em_campo[c]
                        cactos_colocados_em_campo[c].posição[0] -=Terreno.velocidade
                        self.tela.blit(cactos_colocados_em_campo[c].image, (cactos_colocados_em_campo[c].posição[0], cactos_colocados_em_campo[c].posição[1]))          
                except:
                    pass

                # pulo
                pular = pygame.key.get_pressed()[K_w] or pygame.key.get_pressed()[K_SPACE] or \
                    pygame.key.get_pressed()[K_UP] or pygame.mouse.get_pressed()[0]
                if not capivara.pulando and pular:
                    capivara.pular()
                    
                # gravidade
                if capivara.rect.bottom < self.altura_tela - 120:
                    capivara.cair()
                    if capivara.rect.bottom > self.altura_tela - 120:
                        capivara.rect.bottom = self.altura_tela - 120
                else:
                    capivara.zerar_gravidade()

                # cactos
                numero_aleatorio = 0
                if Terreno.velocidade != 0:
                    numero_aleatorio = randint(0, 80 // (Terreno.velocidade // 5 ))
                
                ultimo_item_da_lista_distancia = 0
                if len(cactos_colocados_em_campo) > 0:
                    ultimo_item_da_lista_distancia = self.largura_tela - cactos_colocados_em_campo[-1].posição[0]

                if numero_aleatorio == 0 and ultimo_item_da_lista_distancia > 600 or len(cactos_colocados_em_campo) == 0:
                    try:
                        if self.largura_tela - cactos_colocados_em_campo[-1].posição[0] > 400:
                            cacto_escolhido = randint(0, 2)
                            if cacto_escolhido == 0 or cactos_colocados_em_campo[-1].proporção != 1 or cactos_colocados_em_campo[-1].largura == 2:
                                cacto_tipo1 = Cacto(1, 100, self.largura_tela, self.altura_tela, 1, 1)
                                cactos_colocados_em_campo.append(cacto_tipo1)
                            elif cacto_escolhido == 1:
                                cacto_tipo2 = Cacto(2, 100, self.largura_tela, self.altura_tela, 2, 1)
                                cactos_colocados_em_campo.append(cacto_tipo2)
                            elif cacto_escolhido == 2 and Terreno.velocidade > 5.5:
                                cacto_tipo3 = cacto_tipo3 = Cacto(3, 100, self.largura_tela, self.altura_tela, 1, 2)
                                cacto_tipo3.posição[1] += 100
                                cactos_colocados_em_campo.append(cacto_tipo3)
                    except:
                        cacto_escolhido = randint(0, 2)
                        if cacto_escolhido == 0:
                            cacto_tipo1 = Cacto(1, 100, self.largura_tela, self.altura_tela, 1, 1)
                            cactos_colocados_em_campo.append(cacto_tipo1)
                        elif cacto_escolhido == 2:
                            cacto_tipo2 = Cacto(2, 100, self.largura_tela, self.altura_tela, 2, 1)
                            cactos_colocados_em_campo.append(cacto_tipo2)
                        elif cacto_escolhido == 3:
                            cacto_tipo3 = cacto_tipo3 = Cacto(3, 100, self.largura_tela, self.altura_tela, 1, 2)
                            cacto_tipo3.posição[1] += 100
                            cactos_colocados_em_campo.append(cacto_tipo3)
            
                
                # colisão com cacto
                if len(cactos_colocados_em_campo) > 0:
                    for c in range(0, len(cactos_colocados_em_campo)):
                        if cactos_colocados_em_campo[c].posição[0] <= 160 + capivara.rect.size[0] <= cactos_colocados_em_campo[c].posição[0] + cactos_colocados_em_campo[c].tamanho[0] and cactos_colocados_em_campo[c].posição[1] <= capivara.rect.y + capivara.rect.size[1] <= cactos_colocados_em_campo[c].posição[1] + cactos_colocados_em_campo[c].tamanho[1] and not colisão_com_cacto:
                            colisão_com_cacto = True
                            capivara.vidas -= 1
                        elif capivara.rect.y + capivara.rect.size[1] - 60 >= cactos_colocados_em_campo[c].posição[1] and not colisão_com_cacto:
                            if 260 <= cactos_colocados_em_campo[c].posição[0] <= 140 + capivara.rect.size[0] or 260 <= cactos_colocados_em_campo[c].posição[0] + cactos_colocados_em_campo[c].tamanho[0] <= 140 + capivara.rect.size[0]:
                                colisão_com_cacto = True
                                capivara.vidas -= 1

                # reset
                

                # cajuzinho extra
                numero_aleatorio_cajuzinho = randint(0, 1000)
                if numero_aleatorio_cajuzinho == 0 and capivara.vidas < 3 and not cajuzinho_extra_na_tela:
                    cajuzinho_extra_na_tela = True

                # verifica se ta em cima de algum cacto
                if cajuzinho_extra_na_tela:
                    cajuzinho_extra.posição[0] -= Terreno.velocidade
                    self.tela.blit(cajuzinho_extra.image, (cajuzinho_extra.posição[0], cajuzinho_extra.posição[1]))

                if 200 <= cajuzinho_extra.posição[0] <= 380 and capivara.rect.y <= cajuzinho_extra.posição[1] <= capivara.rect.y + 180:
                    cajuzinho_extra.posição[0] = self.largura_tela
                    capivara.vidas += 1
                    cajuzinho_extra_na_tela = False
                    self.som_cajuzinho_extra.play()

                if cajuzinho_extra.posição[0] + 80 < 0:
                    cajuzinho_extra.posição[0] = self.largura_tela
                    cajuzinho_extra_na_tela = False


                
                # aumento da pontuação e atualização delas
                if Terreno.velocidade > 0:
                    pontuação += int(Terreno.velocidade)

                capivara.update()

                
                
                pontuação_texto = texto(f"Pontuação: {str(pontuação)}")
                pontuação_maxima_texto = texto(f"Recorde: {str(pontuação_maxima)}")
                if pontuação > pontuação_maxima:
                    pontuação_maxima = pontuação
                
                reinicio_agora = False

                self.tela.blit(botão_pausar.image, (botão_pausar.posição[0], botão_pausar.posição[1]))
                self.tela.blit(pontuação_texto, (20, self.altura_tela - 60))
                self.tela.blit(pontuação_maxima_texto, (self.largura_tela // 2, self.altura_tela - 60))
                capivara.rect.topleft = (200, capivara.rect.y)
                self.tela.blit(capivara.image, (200, capivara.rect.y))

            elif pausado and not inicio or morte:
                self.tela.blit(logo.image, (self.largura_tela // 2 - logo.tamanho // 2, -logo.tamanho // 5))

                if morte:
                    pontuação_texto = texto(f"Pontuação feita: {str(pontuação)}")
                    self.tela.blit(pontuação_texto, (0, self.altura_tela - 60))
                else:
                    self.tela.blit(botão_continuar.image, (botão_continuar.posição[0], botão_continuar.posição[1]))

                    # clicar em continuar ^
                if botão_continuar.posição[0] <= x_mouse <= botão_continuar.posição[0] + botão_continuar.tamanho and botão_continuar.posição[1] <= y_mouse <= botão_continuar.posição[1] + botão_continuar.tamanho:
                    if click and not morte:
                        pausado = False
                    if not dentro:
                        dentro = True
                        self.som_botao.play()

                # clicar em reiniciar
                elif botão_reiniciar.posição[0] <= x_mouse <= botão_reiniciar.posição[0] + botão_reiniciar.tamanho and botão_reiniciar.posição[1] <= y_mouse <= botão_reiniciar.posição[1] + botão_reiniciar.tamanho:
                    if click:
                        pontuação = 0
                        morte = False
                        Terreno.velocidade = 0
                        temporizador = 0
                        reinicio_agora = True
                        capivara.vidas = 3
                        cactos_colocados_em_campo = []
                        cacto_tipo1 = Cacto(1, 100, self.largura_tela, self.altura_tela, 1, 1)
                        cacto_tipo2 = Cacto(2, 100, self.largura_tela, self.altura_tela, 2, 1)
                        cacto_tipo3 = Cacto(3, 100, self.largura_tela, self.altura_tela, 1, 2)
                        cactos_colocados_em_campo.append(cacto_tipo1)
                        fundos = []
                        nuvens = []
                        
                        pausado = False
                        cajuzinho_extra.posição[0] = self.largura_tela
                        cajuzinho_extra_na_tela = False

                        inicio = True
                        capivara_posição_x = 480
                        capivara.rect.y = self.altura_tela - 220
                        velocidade_capivara_x = 1
                        velocidade_capivara_y = 0
                        contagem = 0
                        onça = Onça(-200, self.altura_tela - 200 - 120)
                        velocidade_onça_x = 4
                        mostrar_onça = False
                        tempo = 0
                        capivara.atual = 0
                        capivara.update()

                        aguas = []
                        agua_entrada = Agua("agua_entrada", 0, self.altura_tela - 120)
                        aguas.append(agua_entrada)
                        agua_meio1 = Agua("agua_meio", 240, self.altura_tela - 120)
                        aguas.append(agua_meio1)
                        agua_meio2 = Agua("agua_meio", 480, self.altura_tela - 120)
                        aguas.append(agua_meio2)
                        agua_saida = Agua("agua_saida", 480 + 240, self.altura_tela - 120)
                        aguas.append(agua_saida)

                    if not dentro:
                        dentro = True
                        self.som_botao.play()
                
                # clicar em sair
                elif botão_sair.posição[0] <= x_mouse <= botão_sair.posição[0] + botão_sair.tamanho and botão_sair.posição[1] <= y_mouse <= botão_sair.posição[1] + botão_sair.tamanho:
                    if click:
                        pygame.quit()
                        exit()
                    if not dentro:
                        dentro = True
                        self.som_botao.play()
                else:
                    dentro = False

                self.tela.blit(botão_reiniciar.image, (botão_reiniciar.posição[0], botão_reiniciar.posição[1]))
                self.tela.blit(botão_sair.image, (botão_sair.posição[0], botão_sair.posição[1]))        

            click = False
            pygame.display.update()