from config.configuracoes import pygame

dimensoes_janela = pygame.display.get_surface().get_size()

sprites = pygame.sprite.Group()
sprites_agentes = pygame.sprite.Group()

cenario = 0