from .base import Mob
from config.configuracoes import randint, pygame, tela, dimensoes_janela
from recursos import dados

class Navio(Mob):
    def __init__(self):
        Mob.__init__(self, 'recursos/imagens/ship.png', (1, 1), (550, 80), (1, 100))

        self.rect.center = (dimensoes_janela[0] // 2, dimensoes_janela[1] * 0.85)
     
        colisao_width = 550  
        colisao_height = 80  
        self.bloco_colisao = pygame.Rect(dimensoes_janela[0] // 2, dimensoes_janela[1] * 0.85, colisao_width, colisao_height)
        self.atualizar_bloco_colisao()
        
    def atualizar_bloco_colisao(self):
        
        #pygame.draw.rect(tela, (255, 0, 0), self.bloco_colisao, 2)
        self.bloco_colisao.center = self.rect.center

    def update(self):
        self.atualizar_bloco_colisao()

barco = Navio()