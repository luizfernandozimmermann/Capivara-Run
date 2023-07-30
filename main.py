from random import randint
import pygame
from pygame.locals import *
from Jogo import Jogo

pygame.init()

info = pygame.display.Info()
largura_tela = info.current_w
altura_tela = info.current_h

janela = pygame.display.set_mode((largura_tela, altura_tela))

nome_da_janela = pygame.display.set_caption("Capivara Run")
icone_tela_imagem = pygame.image.load("sprites/icone_tela.png").convert_alpha()
icone_tela = pygame.display.set_icon(icone_tela_imagem)


jogo = Jogo(janela)