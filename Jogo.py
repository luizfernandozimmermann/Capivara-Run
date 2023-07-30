import pygame
from pygame.locals import *

from Capivara import Capivara
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
        velocidade_fundo = 0
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
        vidas_capivara = 3
        pisando = True
        capivara = Capivara(self.altura_tela - 400)
        morte = False

        # animação inicial
        capivara_posição_x = 480
        velocidade_capivara_x = 1
        velocidade_capivara_y = 0
        contagem = 0
        chão = Chão(self.altura_tela)
        onça = Onça(-200, self.altura_tela - 200 - 120)
        velocidade_onça_x = 4
        mostrar_onça = False
        tempo = 0
        abriu_agora = True

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

        # fundo
        fundos = []
        nuvens = []
        for c in range(0, self.largura_tela * 3, self.altura_tela):
            fundo = Fundo(c, self.altura_tela, "tela_de_fundo")
            fundos.append(fundo)

            nuvem = Fundo(c, self.altura_tela, "nuvens")
            nuvens.append(nuvem)

        # terra
        solos = []
        for c in range(0, 10):
            solo = Chão(self.altura_tela)
            solo.posição[0] = 240 * c
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
        dentro2 = False

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

            # animação inicial
            if inicio:
                tempo += 1

                if click and easter_egg.posição[0] <= x_mouse <= easter_egg.posição[0] + 80 and self.altura_tela - 80 <= y_mouse <= self.altura_tela:
                    icone_tela_imagem = pygame.image.load("sprites/icone_tela2.png")
                    icone_tela = pygame.display.set_icon(icone_tela_imagem)
                    tocar_amogus = True
                    nome_da_janela = pygame.display.set_caption("Sus Run")
                    logo.amogus()
                    self.som_amogus.play()

                # carregando as nuvens e o fundo
                for c in range(0, len(nuvens)):
                    if nuvens[c].posição[0] <= -self.altura_tela:
                        if c == 0:
                            nuvens[c].posição[0] = nuvens[-1].posição[0] + self.altura_tela
                        else:
                            nuvens[c].posição[0] = nuvens[c - 1].posição[0] + self.altura_tela
                    nuvens[c].posição[0] -= int(velocidade_fundo * 0.2)

                    self.tela.blit(nuvens[c].image, (nuvens[c].posição[0], nuvens[c].posição[1]))
                
                for c in range(0, len(fundos)):
                    if fundos[c].posição[0] <= -self.altura_tela:
                        if c == 0:
                            fundos[c].posição[0] = fundos[-1].posição[0] + self.altura_tela
                        else:
                            fundos[c].posição[0] = fundos[c - 1].posição[0] + self.altura_tela
                    fundos[c].posição[0] -= int(velocidade_fundo * 0.5)

                    self.tela.blit(fundos[c].image, (fundos[c].posição[0], fundos[c].posição[1]))
                
                # carregando o solo
                for c in range(0, len(solos)):
                    # recicla os objetos
                    if solos[c].posição[0] <= -240:
                        if c == 0:
                            solos[c].posição[0] = solos[-1].posição[0] + 240
                        else:
                            solos[c].posição[0] = solos[c-1].posição[0] + 240
                    # movimenta os objetos e atualiza
                    solos[c].posição[0] -= velocidade_fundo
                    self.tela.blit(solos[c].image, (solos[c].posição[0], solos[c].posição[1]))

                # carrega a capivara
                if capivara_posição_x == 610 and contagem == 0:
                    capivara.image = pygame.transform.flip(capivara.image, True, False)
                    velocidade_capivara_x = -velocidade_capivara_x

                if capivara_posição_x == 360 or contagem > 0:
                    contagem += 1
                    if contagem == 240:
                        capivara.image = pygame.transform.flip(capivara.image, True, False)
                        capivara.aceleracao_y = -25
                        velocidade_fundo = 8
                        velocidade_capivara_x = -6
                    elif contagem < 240:
                        velocidade_capivara_x = -velocidade_capivara_x * 1.001
                
                if contagem == 110:
                    self.som_onça_chegando.play()
                if contagem == 130:
                    mostrar_onça = True

                if mostrar_onça:
                    if onça.posição[0] < 0 and contagem < 240:
                        onça.posição[0] += velocidade_onça_x
                    if contagem >= 240:
                        onça.posição[0] -= velocidade_fundo
                    self.tela.blit(onça.image, (onça.posição[0], onça.posição[1]))

                if contagem > 240:
                    capivara.aceleracao_y += 0.5
                
                # fim da animação
                if capivara.rect.y > self.altura_tela - 120 -180 and contagem > 260 and capivara.aceleracao_y > 0:
                    capivara.aceleracao_y = 0
                    capivara.rect.y = self.altura_tela - 120 - 180
                    inicio = False
                    velocidade_fundo = 5.5
                    if tocar_amogus:       
                        if abriu_agora:
                            pygame.mixer.music.set_volume(0.05)
                            musica_de_fundo = pygame.mixer.music.load("audios/musica_amogus.mp3")
                            pygame.mixer.music.play(-1)
                        capivara.transgformar_amogus()
                    else:                
                        if abriu_agora:
                            pygame.mixer.music.set_volume(0.05)
                            musica_de_fundo = pygame.mixer.music.load("audios/musica_de_fundo.mp3")
                            pygame.mixer.music.play(-1)  
                
                if capivara.aceleracao_y != 0:
                    capivara.mover = True
                    capivara.update()

                capivara.rect.y += capivara.aceleracao_y
                if capivara_posição_x > 200:
                    capivara_posição_x += velocidade_capivara_x
                elif capivara_posição_x > 200:
                    velocidade_capivara_x = 0
                    capivara_posição_x = 200
                self.tela.blit(capivara.image, (capivara_posição_x, capivara.rect.y))

                # carrega as aguas
                for c in range(0, len(aguas)):
                    if aguas[c].posição[0] + 240 >= 0:
                        aguas[c].posição[0] -= velocidade_fundo
                    self.tela.blit(aguas[c].image, (aguas[c].posição[0], aguas[c].posição[1]))

                easter_egg.posição[0] -= velocidade_fundo
                self.tela.blit(easter_egg.image, (easter_egg.posição[0], easter_egg.posição[1]))
                
            if botão_pausar.posição[0] <= x_mouse <= botão_pausar.posição[0] + botão_pausar.tamanho and botão_pausar.posição[1] <= y_mouse <= botão_pausar.posição[1] + botão_pausar.tamanho and not pausado and not inicio:
                if click:
                    pausado = True
                if not dentro2 and not pausado:
                    dentro2 = True
                    self.som_botao.play()

            else:
                dentro2 = False

            # O JOGO TA AQUI XDD
            if not pausado and not inicio and not morte:
                abriu_agora = False
                # movimentação da tela de fundo e nuvens
                for c in range(0, len(nuvens)):
                    if nuvens[c].posição[0] <= -self.altura_tela:
                        if c == 0:
                            nuvens[c].posição[0] = nuvens[-1].posição[0] + self.altura_tela
                        else:
                            nuvens[c].posição[0] = nuvens[c - 1].posição[0] + self.altura_tela
                    nuvens[c].posição[0] -= int(velocidade_fundo * 0.2)

                    self.tela.blit(nuvens[c].image, (nuvens[c].posição[0], nuvens[c].posição[1]))
                
                for c in range(0, len(fundos)):
                    if fundos[c].posição[0] <= -self.altura_tela:
                        if c == 0:
                            fundos[c].posição[0] = fundos[-1].posição[0] + self.altura_tela
                        else:
                            fundos[c].posição[0] = fundos[c - 1].posição[0] + self.altura_tela
                    fundos[c].posição[0] -= int(velocidade_fundo * 0.5)

                    self.tela.blit(fundos[c].image, (fundos[c].posição[0], fundos[c].posição[1]))

                # movimentação do solo
                for c in range(0, len(solos)):
                    # recicla os objetos
                    if solos[c].posição[0] <= -240:
                        if c == 0:
                            solos[c].posição[0] = solos[-1].posição[0] + 240
                        else:
                            solos[c].posição[0] = solos[c-1].posição[0] + 240
                    # movimenta os objetos e atualiza
                    solos[c].posição[0] -= velocidade_fundo
                    self.tela.blit(solos[c].image, (solos[c].posição[0], solos[c].posição[1]))

                # carregamento dos cajuzinho
                for c in range(0, vidas_capivara):
                    self.tela.blit(cajuzinho.image, (c * 100 + 20, 20))
                
                
                # deletando cactos que ja foram
                try:
                    for c in range(0, len(cactos_colocados_em_campo)):
                        if cactos_colocados_em_campo[c].posição[0] + cactos_colocados_em_campo[c].tamanho[0] < 0:
                            del cactos_colocados_em_campo[c]
                        cactos_colocados_em_campo[c].posição[0] -=velocidade_fundo
                        self.tela.blit(cactos_colocados_em_campo[c].image, (cactos_colocados_em_campo[c].posição[0], cactos_colocados_em_campo[c].posição[1]))          
                except:
                    pass

                # gravidade
                if capivara.rect.y + capivara.rect.height < self.altura_tela - 120:
                    capivara.pulando = True
                    capivara.cair()
                else:
                    capivara.zerar_gravidade()

                # pulo
                pular = pygame.key.get_pressed()[K_w] or pygame.key.get_pressed()[K_SPACE] or \
                    pygame.key.get_pressed()[K_UP] or pygame.mouse.get_pressed()[0]
                if not capivara.pulando and pular:
                    capivara.pular()
                    
                

                # define a altura da capivara, mantendo ela em cima da terra
                capivara.rect.y += int(capivara.aceleracao_y)
                if capivara.rect.y + 180 > solos[0].posição[1]:
                    capivara.rect.y = solos[0].posição[1] - 180
                    capivara.aceleracao_y = 0


                # cactos
                numero_aleatorio = ""
                if velocidade_fundo != 0:
                    numero_aleatorio = randint(0, 80 // (velocidade_fundo // 5 ))
                
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
                            elif cacto_escolhido == 2 and velocidade_fundo > 5.5:
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
                        if cactos_colocados_em_campo[c].posição[0] <= 160 + capivara.tamanho[0] <= cactos_colocados_em_campo[c].posição[0] + cactos_colocados_em_campo[c].tamanho[0] and cactos_colocados_em_campo[c].posição[1] <= capivara.rect.y + capivara.tamanho[1] <= cactos_colocados_em_campo[c].posição[1] + cactos_colocados_em_campo[c].tamanho[1] and not colisão_com_cacto:
                            colisão_com_cacto = True
                            vidas_capivara -= 1
                        elif capivara.rect.y + capivara.tamanho[1] - 60 >= cactos_colocados_em_campo[c].posição[1] and not colisão_com_cacto:
                            if 260 <= cactos_colocados_em_campo[c].posição[0] <= 140 + capivara.tamanho[0] or 260 <= cactos_colocados_em_campo[c].posição[0] + cactos_colocados_em_campo[c].tamanho[0] <= 140 + capivara.tamanho[0]:
                                colisão_com_cacto = True
                                vidas_capivara -= 1

                # reset
                if vidas_capivara == 0:
                    self.som_morte.play()
                    morte = True
                
                if colisão_com_cacto:
                    temporizador += 1
                    if temporizador == 1 and vidas_capivara != 0 and not reinicio_agora:
                        self.som_colisão_cacto.play()
                    if 20 > temporizador > 0 and not reinicio_agora:
                        capivara.image = imagem_vazio
                    else:
                        capivara.image = capivara.animações[int(capivara.atual)]
                        capivara.mover = True
                        capivara.update()
                    if temporizador == 60:
                        colisão_com_cacto = False
                    elif temporizador > 60:
                        temporizador = 0

                # cajuzinho extra
                numero_aleatorio_cajuzinho = randint(0, 1000)
                if numero_aleatorio_cajuzinho == 0 and vidas_capivara < 3 and not cajuzinho_extra_na_tela:
                    cajuzinho_extra_na_tela = True

                # verifica se ta em cima de algum cacto
                if cajuzinho_extra_na_tela:
                    cajuzinho_extra.posição[0] -= velocidade_fundo
                    self.tela.blit(cajuzinho_extra.image, (cajuzinho_extra.posição[0], cajuzinho_extra.posição[1]))

                if 200 <= cajuzinho_extra.posição[0] <= 380 and capivara.rect.y <= cajuzinho_extra.posição[1] <= capivara.rect.y + 180:
                    cajuzinho_extra.posição[0] = self.largura_tela
                    vidas_capivara += 1
                    cajuzinho_extra_na_tela = False
                    self.som_cajuzinho_extra.play()

                if cajuzinho_extra.posição[0] + 80 < 0:
                    cajuzinho_extra.posição[0] = self.largura_tela
                    cajuzinho_extra_na_tela = False


                # aumento de velocidade
                if 0 < velocidade_fundo < 10:
                    velocidade_fundo += 0.001
                
                # aumento da pontuação e atualização delas
                if velocidade_fundo > 0:
                    pontuação += int(velocidade_fundo)

                if not colisão_com_cacto and velocidade_fundo > 0:
                    capivara.update()

                if velocidade_fundo == 0:
                    capivara.image = capivara.animações[0]
                
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
                        velocidade_fundo = 0
                        temporizador = 0
                        reinicio_agora = True
                        vidas_capivara = 3
                        cactos_colocados_em_campo = []
                        cacto_tipo1 = Cacto(1, 100, self.largura_tela, self.altura_tela, 1, 1)
                        cacto_tipo2 = Cacto(2, 100, self.largura_tela, self.altura_tela, 2, 1)
                        cacto_tipo3 = Cacto(3, 100, self.largura_tela, self.altura_tela, 1, 2)
                        cactos_colocados_em_campo.append(cacto_tipo1)
                        fundos = []
                        nuvens = []
                        for c in range(0, self.largura_tela * 3, self.altura_tela):
                            fundo = Fundo(c, self.altura_tela, "tela_de_fundo")
                            fundos.append(fundo)
                            nuvem = Fundo(c, self.altura_tela, "nuvens")
                            nuvens.append(nuvem)
                        pausado = False
                        cajuzinho_extra.posição[0] = self.largura_tela
                        cajuzinho_extra_na_tela = False

                        inicio = True
                        capivara_posição_x = 480
                        capivara.rect.y = self.altura_tela - 220
                        velocidade_capivara_x = 1
                        velocidade_capivara_y = 0
                        contagem = 0
                        chão = Chão(self.altura_tela)
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