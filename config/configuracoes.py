import pygame
import numpy, math, time
import os
from random import randint, uniform, choice
from functools import cache

pygame.init()

fps = 600
clock = pygame.time.Clock()

largura = 1000
altura = 600

tela = pygame.display.set_mode((largura, altura), pygame.RESIZABLE)

dimensoes_janela = tela.get_size()

plano_de_fundo = pygame.image.load("recursos/imagens/bg.png")

musica = False
if musica:
    musica_de_fundo = pygame.mixer.Sound("recursos/sons/fundo.wav")
    musica_de_fundo.set_volume(0.5)
    musica_de_fundo.play(-1)

pygame.display.set_caption("Neural Pilot")