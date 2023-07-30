from random import randint
import pygame
from pygame.locals import *
from sys import exit

pygame.init()

class Capivara(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.animações = []
        for c in range(0, 5):
            imagem = pygame.image.load("sprites/capivarinha_" + str(c) + ".png").convert_alpha()
            imagem = pygame.transform.scale(imagem, (180, 180))
            self.animações.append(imagem)
        self.atual = 0
        self.image = self.animações[self.atual]
        self.image = pygame.transform.scale(self.image, (180, 180))
        self.mover = False
        self.tamanho = [180, 180]
        self.rect = self.image.get_rect()
        self.rect.topleft = (0, 0)

    def amogus(self):
        self.animações = []
        for c in range(0, 5):
            imagem = pygame.image.load("sprites/amogus_" + str(c) + ".png").convert_alpha()
            imagem = pygame.transform.scale(imagem, (180, 180))
            self.animações.append(imagem)

    def update(self):
        if self.mover:
            self.atual += 0.1
            if self.atual >= 4:
                self.atual = 0
            self.image = self.animações[int(self.atual)]
            self.image = pygame.transform.scale(self.image, (180, 180))

class Fundo(pygame.sprite.Sprite):
    def __init__(self, x, altura_tela, imagem):
        pygame.sprite.Sprite.__init__(self)

        self.altura = altura_tela

        self.image = pygame.image.load("sprites/" + str(imagem) + ".png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.altura, self.altura))
        if imagem == "tela_de_fundo":
            self.posição = [x, -120]
        else:
            self.posição = [x, 0]

class Chão(pygame.sprite.Sprite):
    def __init__(self, altura_tela):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load("sprites/terra.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (240, 120))
        self.posição = [0, altura_tela - 120]
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.posição[0], self.posição[1])

class Cacto(pygame.sprite.Sprite):
    def __init__(self, imagem, tamanho, largura_tela, altura_tela, proporção_altura=1, proporção_largura=1):
        pygame.sprite.Sprite.__init__(self)

        self.proporção = proporção_altura
        self.largura = proporção_largura
        self.tamanho = [tamanho * proporção_largura, tamanho * proporção_altura]
        self.image = pygame.image.load("sprites/cacto_" + str(imagem) + ".png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.tamanho[0], self.tamanho[1]))
        self.posição = [largura_tela, altura_tela - self.tamanho[0] - 110 - tamanho * (proporção_altura - 1)]
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.posição[0], self.posição[1])

class Botão(pygame.sprite.Sprite):
    def __init__(self, imagem, x, y, tamanho):
        pygame.sprite.Sprite.__init__(self)

        self.tamanho = tamanho
        self.posição = [x, y]
        self.image = pygame.image.load("sprites/botão_" + str(imagem) + ".png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (tamanho, tamanho))

class Cajuzinho(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load("sprites/cajuzinho.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (100, 100))

def texto(texto):
    fonte = pygame.font.SysFont("Emulogic Regular", 60, True, False)
    texto_formatado = fonte.render(texto, True, (0, 0, 0))
    return texto_formatado

class Cajuzinho_extra(pygame.sprite.Sprite):
    def __init__(self, posição_x, posição_y):
        pygame.sprite.Sprite.__init__(self)

        self.posição = [posição_x, posição_y]
        self.image = pygame.image.load("sprites/cajuzinho.png").convert_alpha()
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
        self.image = pygame.image.load("sprites/logo.png").convert_alpha()
        self.tamanho = tamanho
        self.image = pygame.transform.scale(self.image, (tamanho, tamanho))

    def amogus(self):
        self.image = pygame.image.load("sprites/logo_sus.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.tamanho, self.tamanho))

info = pygame.display.Info()
largura_tela = info.current_w
altura_tela = info.current_h
janela = pygame.display.set_mode((largura_tela, altura_tela))
nome_da_janela = pygame.display.set_caption("Capivara Run")
icone_tela_imagem = pygame.image.load("sprites/icone_tela.png").convert_alpha()
icone_tela = pygame.display.set_icon(icone_tela_imagem)
relogio = pygame.time.Clock()
fps = 120

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
easter_egg = Easter_egg(0, altura_tela - 80)
tocar_amogus = False
som_amogus = pygame.mixer.Sound("áudios/amogus.wav")
som_amogus.set_volume(0.05)

som_colisão_cacto = pygame.mixer.Sound("áudios/dano_cacto.wav")
som_colisão_cacto.set_volume(0.2)

som_cajuzinho_extra = pygame.mixer.Sound("áudios/cajuzinho_extra.wav")
som_cajuzinho_extra.set_volume(1)

som_morte = pygame.mixer.Sound("áudios/morte.wav")
som_morte.set_volume(0.1)

som_pulo = pygame.mixer.Sound("áudios/pulo.wav")
som_pulo.set_volume(0.8)

som_onça_chegando = pygame.mixer.Sound("áudios/onça_chegando.wav")
som_onça_chegando.set_volume(0.1)

som_botão = pygame.mixer.Sound("áudios/botões_audio.wav")
som_botão.set_volume(0.6)

# capivara
imagem_vazio = pygame.image.load("sprites/vazio.png").convert_alpha()
colisão_com_cacto = False
vidas_capivara = 3
pisando = True
capivara = Capivara()
altura_capivara = altura_tela - 400
aceleração_capivara_y = 0
capivara_pisou_na_terra = 3
morte = False

# animação inicial
capivara_posição_x = 480
altura_capivara = altura_tela - 220
velocidade_capivara_x = 1
velocidade_capivara_y = 0
contagem = 0
chão = Chão(altura_tela)
onça = Onça(-200, altura_tela - 200 - 120)
velocidade_onça_x = 4
mostrar_onça = False
tempo = 0
abriu_agora = True

aguas = []
agua_entrada = Agua("agua_entrada", 0, altura_tela - 120)
aguas.append(agua_entrada)
agua_meio1 = Agua("agua_meio", 240, altura_tela - 120)
aguas.append(agua_meio1)
agua_meio2 = Agua("agua_meio", 480, altura_tela - 120)
aguas.append(agua_meio2)
agua_saida = Agua("agua_saida", 480 + 240, altura_tela - 120)
aguas.append(agua_saida)

# cajuzinho
cajuzinho = Cajuzinho()
cajuzinho_extra = Cajuzinho_extra(largura_tela, altura_tela - 120 - 80 - 30)
cajuzinho_extra_na_tela = False

# fundo
fundos = []
nuvens = []
for c in range(0, largura_tela * 3, altura_tela):
    fundo = Fundo(c, altura_tela, "tela_de_fundo")
    fundos.append(fundo)

    nuvem = Fundo(c, altura_tela, "nuvens")
    nuvens.append(nuvem)

# terra
solos = []
for c in range(0, 10):
    solo = Chão(altura_tela)
    solo.posição[0] = 240 * c
    solos.append(solo)

# cactos
cactos_colocados_em_campo = []

cacto_tipo1 = Cacto(1, 100, largura_tela, altura_tela, 1, 1)
cactos_colocados_em_campo.append(cacto_tipo1)

cacto_tipo2 = Cacto(2, 100, largura_tela, altura_tela, 2, 1)
cacto_tipo3 = Cacto(3, 100, largura_tela, altura_tela, 1, 2)

# botões quando pausado e pausar
tamanho_botões = 160
botão_continuar = Botão("continuar", 100, (altura_tela - tamanho_botões) // 2, tamanho_botões)
botão_reiniciar =Botão("restart", largura_tela // 2 - tamanho_botões // 2, (altura_tela - tamanho_botões) // 2, tamanho_botões)
botão_sair = Botão("sair", largura_tela - 100 - tamanho_botões, (altura_tela - tamanho_botões) // 2, tamanho_botões)
botão_pausar = Botão("pause", largura_tela - tamanho_botões + 40 - 20, 20, tamanho_botões - 40)
dentro = False
dentro2 = False

# logo
logo = Logo(altura_tela // 3 * 2)

while True:
    janela.fill((50, 50, 50))
    relogio.tick(fps)
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

        if click and easter_egg.posição[0] <= x_mouse <= easter_egg.posição[0] + 80 and altura_tela - 80 <= y_mouse <= altura_tela:
            icone_tela_imagem = pygame.image.load("sprites/icone_tela2.png")
            icone_tela = pygame.display.set_icon(icone_tela_imagem)
            tocar_amogus = True
            nome_da_janela = pygame.display.set_caption("Sus Run")
            logo.amogus()
            som_amogus.play()

        # carregando as nuvens e o fundo
        for c in range(0, len(nuvens)):
            if nuvens[c].posição[0] <= -altura_tela:
                if c == 0:
                    nuvens[c].posição[0] = nuvens[-1].posição[0] + altura_tela
                else:
                    nuvens[c].posição[0] = nuvens[c - 1].posição[0] + altura_tela
            nuvens[c].posição[0] -= int(velocidade_fundo * 0.2)

            janela.blit(nuvens[c].image, (nuvens[c].posição[0], nuvens[c].posição[1]))
        
        for c in range(0, len(fundos)):
            if fundos[c].posição[0] <= -altura_tela:
                if c == 0:
                    fundos[c].posição[0] = fundos[-1].posição[0] + altura_tela
                else:
                    fundos[c].posição[0] = fundos[c - 1].posição[0] + altura_tela
            fundos[c].posição[0] -= int(velocidade_fundo * 0.5)

            janela.blit(fundos[c].image, (fundos[c].posição[0], fundos[c].posição[1]))
        
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
            janela.blit(solos[c].image, (solos[c].posição[0], solos[c].posição[1]))

        # carrega a capivara
        if capivara_posição_x == 610 and contagem == 0:
            capivara.image = pygame.transform.flip(capivara.image, True, False)
            velocidade_capivara_x = -velocidade_capivara_x

        if capivara_posição_x == 360 or contagem > 0:
            contagem += 1
            if contagem == 240:
                capivara.image = pygame.transform.flip(capivara.image, True, False)
                aceleração_capivara_y = -25
                velocidade_fundo = 8
                velocidade_capivara_x = -6
            elif contagem < 240:
                velocidade_capivara_x = -velocidade_capivara_x * 1.001
        
        if contagem == 110:
            som_onça_chegando.play()
        if contagem == 130:
            mostrar_onça = True

        if mostrar_onça:
            if onça.posição[0] < 0 and contagem < 240:
                onça.posição[0] += velocidade_onça_x
            if contagem >= 240:
                onça.posição[0] -= velocidade_fundo
            janela.blit(onça.image, (onça.posição[0], onça.posição[1]))

        if contagem > 240:
            aceleração_capivara_y += 0.5
        
        # fim da animação
        if altura_capivara > altura_tela - 120 -180 and contagem > 260 and aceleração_capivara_y > 0:
            aceleração_capivara_y = 0
            altura_capivara = altura_tela - 120 - 180
            inicio = False
            velocidade_fundo = 5.5
            if tocar_amogus:       
                if abriu_agora:
                    pygame.mixer.music.set_volume(0.05)
                    musica_de_fundo = pygame.mixer.music.load("áudios/musica_amogus.mp3")
                    pygame.mixer.music.play(-1)
                capivara.amogus()
            else:                
                if abriu_agora:
                    pygame.mixer.music.set_volume(0.05)
                    musica_de_fundo = pygame.mixer.music.load("áudios/musica_de_fundo.mp3")
                    pygame.mixer.music.play(-1)  
        
        if aceleração_capivara_y != 0:
            capivara.mover = True
            capivara.update()

        altura_capivara += aceleração_capivara_y
        if capivara_posição_x > 200:
            capivara_posição_x += velocidade_capivara_x
        elif capivara_posição_x > 200:
            velocidade_capivara_x = 0
            capivara_posição_x = 200
        janela.blit(capivara.image, (capivara_posição_x, altura_capivara))

        # carrega as aguas
        for c in range(0, len(aguas)):
            if aguas[c].posição[0] + 240 >= 0:
                aguas[c].posição[0] -= velocidade_fundo
            janela.blit(aguas[c].image, (aguas[c].posição[0], aguas[c].posição[1]))

        easter_egg.posição[0] -= velocidade_fundo
        janela.blit(easter_egg.image, (easter_egg.posição[0], easter_egg.posição[1]))
        
    if botão_pausar.posição[0] <= x_mouse <= botão_pausar.posição[0] + botão_pausar.tamanho and botão_pausar.posição[1] <= y_mouse <= botão_pausar.posição[1] + botão_pausar.tamanho and not pausado and not inicio:
        if click:
            pausado = True
        if not dentro2 and not pausado:
            dentro2 = True
            som_botão.play()

    else:
        dentro2 = False

    if not pausado and not inicio and not morte:
        abriu_agora = False
        # movimentação da tela de fundo e nuvens
        for c in range(0, len(nuvens)):
            if nuvens[c].posição[0] <= -altura_tela:
                if c == 0:
                    nuvens[c].posição[0] = nuvens[-1].posição[0] + altura_tela
                else:
                    nuvens[c].posição[0] = nuvens[c - 1].posição[0] + altura_tela
            nuvens[c].posição[0] -= int(velocidade_fundo * 0.2)

            janela.blit(nuvens[c].image, (nuvens[c].posição[0], nuvens[c].posição[1]))
        
        for c in range(0, len(fundos)):
            if fundos[c].posição[0] <= -altura_tela:
                if c == 0:
                    fundos[c].posição[0] = fundos[-1].posição[0] + altura_tela
                else:
                    fundos[c].posição[0] = fundos[c - 1].posição[0] + altura_tela
            fundos[c].posição[0] -= int(velocidade_fundo * 0.5)

            janela.blit(fundos[c].image, (fundos[c].posição[0], fundos[c].posição[1]))

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
            janela.blit(solos[c].image, (solos[c].posição[0], solos[c].posição[1]))

        # carregamento dos cajuzinho
        for c in range(0, vidas_capivara):
            janela.blit(cajuzinho.image, (c * 100 + 20, 20))
        
        
        # deletando cactos que ja foram
        try:
            for c in range(0, len(cactos_colocados_em_campo)):
                if cactos_colocados_em_campo[c].posição[0] + cactos_colocados_em_campo[c].tamanho[0] < 0:
                    del cactos_colocados_em_campo[c]
                cactos_colocados_em_campo[c].posição[0] -=velocidade_fundo
                janela.blit(cactos_colocados_em_campo[c].image, (cactos_colocados_em_campo[c].posição[0], cactos_colocados_em_campo[c].posição[1]))          
        except:
            pass

        # gravidade
        pisando = False
        for c in range(0, len(solos)):
            if solos[c].posição[0] <= 100 <= solos[c].posição[0] + 240 and solos[c].posição[1] <= altura_capivara + 180:
                pisando = True
                capivara_pisou_na_terra = c
                break
        
        if not pisando:
            aceleração_capivara_y += 0.5

        # pulo
        if not reinicio_agora and pygame.key.get_pressed()[K_w] or pygame.key.get_pressed()[K_SPACE] or pygame.key.get_pressed()[K_UP] or pygame.mouse.get_pressed()[0]:
            if pisando:
                aceleração_capivara_y = -19
                som_pulo.play()

            # começo do jogo
            if velocidade_fundo == 0:
                velocidade_fundo = 5.5
                capivara.mover = True

        # define a altura da capivara, mantendo ela em cima da terra
        altura_capivara += int(aceleração_capivara_y)
        if altura_capivara + 180 > solos[0].posição[1]:
            altura_capivara = solos[0].posição[1] - 180
            aceleração_capivara_y = 0


        # cactos
        numero_aleatorio = ""
        if velocidade_fundo != 0:
            numero_aleatorio = randint(0, 80 // (velocidade_fundo // 5 ))
        
        ultimo_item_da_lista_distancia = 0
        if len(cactos_colocados_em_campo) > 0:
            ultimo_item_da_lista_distancia = largura_tela - cactos_colocados_em_campo[-1].posição[0]

        if numero_aleatorio == 0 and ultimo_item_da_lista_distancia > 600 or len(cactos_colocados_em_campo) == 0:
            try:
                if largura_tela - cactos_colocados_em_campo[-1].posição[0] > 400:
                    cacto_escolhido = randint(0, 2)
                    if cacto_escolhido == 0 or cactos_colocados_em_campo[-1].proporção != 1 or cactos_colocados_em_campo[-1].largura == 2:
                        cacto_tipo1 = Cacto(1, 100, largura_tela, altura_tela, 1, 1)
                        cactos_colocados_em_campo.append(cacto_tipo1)
                    elif cacto_escolhido == 1:
                        cacto_tipo2 = Cacto(2, 100, largura_tela, altura_tela, 2, 1)
                        cactos_colocados_em_campo.append(cacto_tipo2)
                    elif cacto_escolhido == 2 and velocidade_fundo > 5.5:
                        cacto_tipo3 = cacto_tipo3 = Cacto(3, 100, largura_tela, altura_tela, 1, 2)
                        cacto_tipo3.posição[1] += 100
                        cactos_colocados_em_campo.append(cacto_tipo3)
            except:
                cacto_escolhido = randint(0, 2)
                if cacto_escolhido == 0:
                    cacto_tipo1 = Cacto(1, 100, largura_tela, altura_tela, 1, 1)
                    cactos_colocados_em_campo.append(cacto_tipo1)
                elif cacto_escolhido == 2:
                    cacto_tipo2 = Cacto(2, 100, largura_tela, altura_tela, 2, 1)
                    cactos_colocados_em_campo.append(cacto_tipo2)
                elif cacto_escolhido == 3:
                    cacto_tipo3 = cacto_tipo3 = Cacto(3, 100, largura_tela, altura_tela, 1, 2)
                    cacto_tipo3.posição[1] += 100
                    cactos_colocados_em_campo.append(cacto_tipo3)
    
        
        # colisão com cacto
        if len(cactos_colocados_em_campo) > 0:
            for c in range(0, len(cactos_colocados_em_campo)):
                if cactos_colocados_em_campo[c].posição[0] <= 160 + capivara.tamanho[0] <= cactos_colocados_em_campo[c].posição[0] + cactos_colocados_em_campo[c].tamanho[0] and cactos_colocados_em_campo[c].posição[1] <= altura_capivara + capivara.tamanho[1] <= cactos_colocados_em_campo[c].posição[1] + cactos_colocados_em_campo[c].tamanho[1] and not colisão_com_cacto:
                    colisão_com_cacto = True
                    vidas_capivara -= 1
                elif altura_capivara + capivara.tamanho[1] - 60 >= cactos_colocados_em_campo[c].posição[1] and not colisão_com_cacto:
                    if 260 <= cactos_colocados_em_campo[c].posição[0] <= 140 + capivara.tamanho[0] or 260 <= cactos_colocados_em_campo[c].posição[0] + cactos_colocados_em_campo[c].tamanho[0] <= 140 + capivara.tamanho[0]:
                        colisão_com_cacto = True
                        vidas_capivara -= 1

        # reset
        if vidas_capivara == 0:
            som_morte.play()
            morte = True
        
        if colisão_com_cacto:
            temporizador += 1
            if temporizador == 1 and vidas_capivara != 0 and not reinicio_agora:
                som_colisão_cacto.play()
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
            janela.blit(cajuzinho_extra.image, (cajuzinho_extra.posição[0], cajuzinho_extra.posição[1]))

        if 200 <= cajuzinho_extra.posição[0] <= 380 and altura_capivara <= cajuzinho_extra.posição[1] <= altura_capivara + 180:
            cajuzinho_extra.posição[0] = largura_tela
            vidas_capivara += 1
            cajuzinho_extra_na_tela = False
            som_cajuzinho_extra.play()

        if cajuzinho_extra.posição[0] + 80 < 0:
            cajuzinho_extra.posição[0] = largura_tela
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

        janela.blit(botão_pausar.image, (botão_pausar.posição[0], botão_pausar.posição[1]))
        janela.blit(pontuação_texto, (20, altura_tela - 60))
        janela.blit(pontuação_maxima_texto, (largura_tela // 2, altura_tela - 60))
        capivara.rect.topleft = (200, altura_capivara)
        janela.blit(capivara.image, (200, altura_capivara))

    elif pausado and not inicio or morte:
        janela.blit(logo.image, (largura_tela // 2 - logo.tamanho // 2, -logo.tamanho // 5))

        if morte:
            pontuação_texto = texto(f"Pontuação feita: {str(pontuação)}")
            janela.blit(pontuação_texto, (0, altura_tela - 60))
        else:
            janela.blit(botão_continuar.image, (botão_continuar.posição[0], botão_continuar.posição[1]))

            # clicar em continuar ^
        if botão_continuar.posição[0] <= x_mouse <= botão_continuar.posição[0] + botão_continuar.tamanho and botão_continuar.posição[1] <= y_mouse <= botão_continuar.posição[1] + botão_continuar.tamanho:
            if click and not morte:
                pausado = False
            if not dentro:
                dentro = True
                som_botão.play()

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
                cacto_tipo1 = Cacto(1, 100, largura_tela, altura_tela, 1, 1)
                cacto_tipo2 = Cacto(2, 100, largura_tela, altura_tela, 2, 1)
                cacto_tipo3 = Cacto(3, 100, largura_tela, altura_tela, 1, 2)
                cactos_colocados_em_campo.append(cacto_tipo1)
                fundos = []
                nuvens = []
                for c in range(0, largura_tela * 3, altura_tela):
                    fundo = Fundo(c, altura_tela, "tela_de_fundo")
                    fundos.append(fundo)
                    nuvem = Fundo(c, altura_tela, "nuvens")
                    nuvens.append(nuvem)
                pausado = False
                cajuzinho_extra.posição[0] = largura_tela
                cajuzinho_extra_na_tela = False

                inicio = True
                capivara_posição_x = 480
                altura_capivara = altura_tela - 220
                velocidade_capivara_x = 1
                velocidade_capivara_y = 0
                contagem = 0
                chão = Chão(altura_tela)
                onça = Onça(-200, altura_tela - 200 - 120)
                velocidade_onça_x = 4
                mostrar_onça = False
                tempo = 0
                capivara.atual = 0
                capivara.update()

                aguas = []
                agua_entrada = Agua("agua_entrada", 0, altura_tela - 120)
                aguas.append(agua_entrada)
                agua_meio1 = Agua("agua_meio", 240, altura_tela - 120)
                aguas.append(agua_meio1)
                agua_meio2 = Agua("agua_meio", 480, altura_tela - 120)
                aguas.append(agua_meio2)
                agua_saida = Agua("agua_saida", 480 + 240, altura_tela - 120)
                aguas.append(agua_saida)

            if not dentro:
                dentro = True
                som_botão.play()
        
        # clicar em sair
        elif botão_sair.posição[0] <= x_mouse <= botão_sair.posição[0] + botão_sair.tamanho and botão_sair.posição[1] <= y_mouse <= botão_sair.posição[1] + botão_sair.tamanho:
            if click:
                pygame.quit()
                exit()
            if not dentro:
                dentro = True
                som_botão.play()
        else:
            dentro = False

        janela.blit(botão_reiniciar.image, (botão_reiniciar.posição[0], botão_reiniciar.posição[1]))
        janela.blit(botão_sair.image, (botão_sair.posição[0], botão_sair.posição[1]))        

    click = False
    pygame.display.update()