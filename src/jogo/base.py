from config.configuracoes import pygame, os, randint, numpy, choice, uniform, tela
from recursos import dados

class Mob(pygame.sprite.Sprite):
    def __init__(self, caminho, linhas_colunas, dimensoes, inflar, random_x=500, escala=None):
        pygame.sprite.Sprite.__init__(self)
        dados.sprites.add(self)
    
        self.sprite = pygame.image.load(os.path.join(caminho)).convert_alpha()

        self.sprites = [ self.sprite.subsurface((coluna *  dimensoes[0], linha * dimensoes[1]), (dimensoes[0], dimensoes[1])) for linha in range(linhas_colunas[0]) for coluna in range(linhas_colunas[1]) ]
        self.sprites = [pygame.transform.scale(imagem, escala) for imagem in self.sprites] if escala != None else self.sprites
        self.sprite_index = 0

        self.image = self.sprites[self.sprite_index]

        self.rect = self.image.get_rect()
        self.rect = pygame.Rect.inflate(self.rect, inflar[0], inflar[1])

        self.random_x = random_x
        self.linhas = linhas_colunas[0]
        self.colunas = linhas_colunas[1]
        self.contador_ivulnerabilidade = 0
        self.velocidade_x = 0
        self.velocidade_y = 0
    
    def receber_dano(self, dano):
        self.vida -= dano
    
    def conferir_vida(self):
        if self.vida <= 0:
            return True
    
    def contar_vulnerabilidade(self):
        if self.contador_ivulnerabilidade > 0:
            self.contador_ivulnerabilidade -= 1

    def morrer(self):
        self.kill()
    
    def randomizar(self):
        self.rect = self.image.get_rect()
        self.rect.x = randint(-60, dados.dimensoes_janela[0])
        self.rect.bottom = randint(-400, 0)
    
    def mover(self):
        if abs(self.velocidade_x) >= 1:
            self.rect.x += self.velocidade_x
            self.velocidade_x -= int(self.velocidade_x)
        if abs(self.velocidade_y) >= 1:
            self.rect.y += self.velocidade_y
            self.velocidade_y -= int(self.velocidade_y)
    
    def contar_index(self, taxa=0.1):
        if self.sprite_index < ( self.linhas * self.colunas ) - 1:
            self.image = self.sprites[int(self.sprite_index)]
            self.sprite_index += taxa
            return True
        else:
            return False

    def debug(self, cor=(000, 255, 000)): # mostrar o retangul ode colisao
        pygame.draw.rect(tela, cor, self.rect, 2) if self.debug else None
    
    def renderizar_vida(self):
        # barra de vida
        if self.vida < self.vida_max:
            barra = pygame.Rect(self.rect.x, self.rect.y - 10, self.vida * (self.rect.width / self.vida_max), 5)
            pygame.draw.rect(tela, (255, 000, 000), barra)