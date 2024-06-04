from config.configuracoes import *
from ..rede_neural import estrategia_evolutiva
from . import player
from .navio import barco
from recursos import dados

#classe para conferir conliões
class Colisoes:

    # função para conferir as colisões com o player
    def verificar_colisao(self, objeto):
        for ponto in objeto.pontos:
            ponto = (ponto[0].item(), ponto[1].item())
            if ponto[0] < 0 or ponto[0] > tela.get_width():
                objeto.rede_neural.recompensa += objeto.combustivel
                estrategia_evolutiva.gerenciador.desativar_agente(objeto)
                objeto.kill()
                break
            elif ponto[1] < 0 or ponto[1] > (tela.get_height() - 60):
                objeto.rede_neural.recompensa += objeto.combustivel
                estrategia_evolutiva.gerenciador.desativar_agente(objeto)
                objeto.kill()
                break
            
            for alvo in dados.sprites_alvos:
                if alvo.rect.collidepoint(ponto) and alvo.indice == objeto.index_alvo:
                    objeto.index_alvo += 1
                    objeto.rede_neural.recompensa += 2000
    
    def conferir_pouso(self, objeto):

        for ponto in objeto.pontos[1:]:
            if (ponto[0] > barco.bloco_colisao.left and ponto[0] < barco.bloco_colisao.right) and ponto[1] >= barco.bloco_colisao.top:
                if objeto.angulo_foquete < 100 and objeto.angulo_foquete > 80 and objeto.velocidade_y < 3:
                    if not objeto.pousado:
                        objeto.velocidade_x = 0
                        objeto.velocidade_y = 0
                        objeto.angulo_foquete = 90
                        return True

                else:
                    objeto.rede_neural.recompensa += objeto.combustivel
                    estrategia_evolutiva.gerenciador.desativar_agente(objeto)
                    objeto.kill()
                    break
        return False
       
    def verificar_saida(self, objeto):
        if objeto.rect.top > dados.dimensoes_janela[1] or objeto.rect.right < 0 or objeto.rect.left > dados.dimensoes_janela[0]:
            objeto.rede_neural.recompensa += objeto.combustivel
            estrategia_evolutiva.gerenciador.desativar_agente(objeto)
            objeto.kill()
            
    # função para chamar as funções de colisão a cada iteração
    def update(self):
        if len(estrategia_evolutiva.gerenciador.agentes) > 0:
            for agente in estrategia_evolutiva.gerenciador.agentes[:]:
                self.verificar_colisao(agente)
            for agente in estrategia_evolutiva.gerenciador.agentes[:]:
                self.verificar_saida(agente)
            for agente in estrategia_evolutiva.gerenciador.agentes[:]:
                agente.pousado = True if self.conferir_pouso(agente) else False

        try:      
            for ponto in player.jogador.pontos:
                ponto = (ponto[0].item(), ponto[1].item())
                if ponto[0] < 0 or ponto[0] > tela.get_width():
                    player.jogador.kill()
                    player.jogador = None
                    break
                elif ponto[1] < 0 or ponto[1] > (tela.get_height() - 60):
                    player.jogador.kill()
                    player.jogador = None
                    break
            
            for ponto in player.jogador.pontos[1:]:
                if (ponto[0] > barco.bloco_colisao.left and ponto[0] < barco.bloco_colisao.right) and ponto[1] >= barco.bloco_colisao.top:
                    if player.jogador.angulo_foquete < 100 and player.jogador.angulo_foquete > 80 and player.jogador.velocidade_y < 3:
                        if not player.jogador.pousado:
                            player.jogador.velocidade_x = 0
                            player.jogador.velocidade_y = 0
                            player.jogador.angulo_foquete = 90
                            return True
                        else:
                            player.jogador.frames_parado += 1
                    else:
                        player.jogador.kill()
                        player.jogador = None
                        break
            player.jogador.frames_parado = 0
        except Exception as e: pass
