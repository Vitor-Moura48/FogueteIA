from config.configuracoes import pygame, os, randint, numpy, choice, uniform, tela
from recursos import dados

class Mob(pygame.sprite.Sprite):
    def __init__(self, caminho, linhas_colunas, dimensoes, inflar, escala=None):
        pygame.sprite.Sprite.__init__(self)
        dados.sprites.add(self)
    
        self.sprite = pygame.image.load(os.path.join(caminho)).convert_alpha()

        self.sprites = [ self.sprite.subsurface((coluna *  dimensoes[0], linha * dimensoes[1]), (dimensoes[0], dimensoes[1])) for linha in range(linhas_colunas[0]) for coluna in range(linhas_colunas[1]) ]
        self.sprites = [pygame.transform.scale(imagem, escala) for imagem in self.sprites] if escala != None else self.sprites
        self.sprite_index = 0

        self.image = self.sprites[self.sprite_index]

        self.rect = self.image.get_rect()
        self.rect = pygame.Rect.inflate(self.rect, inflar[0], inflar[1])

        self.linhas = linhas_colunas[0]
        self.colunas = linhas_colunas[1]
 
    
    def contar_index(self, taxa=0.1):
        if self.sprite_index < ( self.linhas * self.colunas ) - 1:
            self.image = self.sprites[int(self.sprite_index)]
            self.sprite_index += taxa
            return True
        else:
            return False

    def debug(self, cor=(000, 255, 000)): # mostrar o retangulo de colisao
        pygame.draw.rect(tela, cor, self.rect, 2) if self.debug else None
    
