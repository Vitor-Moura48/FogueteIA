from config.configuracoes import pygame, dimensoes_janela
from random import randint

dimensoes_janela = pygame.display.get_surface().get_size()

sprites = pygame.sprite.Group()
sprites_agentes = pygame.sprite.Group()
sprites_alvos = pygame.sprite.Group()

cenario = 0
vento = 0
max_vento = 0.08
sucessos = 0

center_agentes = (randint(int(dimensoes_janela[0] * 0.1), int(dimensoes_janela[0] * 0.9)), randint(int(dimensoes_janela[1] * 0.3), int(dimensoes_janela[1] * 0.6)))