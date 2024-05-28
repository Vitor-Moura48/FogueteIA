from .base import Mob
from config.configuracoes import randint, pygame, tela, dimensoes_janela
from recursos import dados

class Navio(Mob):
    def __init__(self):
        Mob.__init__(self, 'recursos/imagens/ship.png', (1, 1), (550, 80), (10, 10))

        self.rect.center = (dimensoes_janela[0] // 2, dimensoes_janela[1] * 0.85)
        
    def update(self):
        self.debug()

barco = Navio()