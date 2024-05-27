from config.configuracoes import *
from ..rede_neural import estrategia_evolutiva
from . import player
from recursos import dados

#classe para conferir conliões
class Colisoes:
    
    def verificar_saida(self, objeto):
        if objeto.rect.top > dados.dimensoes_janela[1] or objeto.rect.right < 0 or objeto.rect.left > dados.dimensoes_janela[0]:
            objeto.kill()
            
    # função para chamar as funções de colisão a cada iteração
    def update(self):

        for objeto in dados.sprites:
            self.verificar_saida(objeto)

        try: 
            if pygame.sprite.spritecollideany(player.jogador, dados.sprites_inimigas):
                player.jogador.kill()
                player.jogador = None
        except: pass

