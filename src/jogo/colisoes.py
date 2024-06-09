from config.configuracoes import *
from ..rede_neural import estrategia_evolutiva
from . import player
from .navio import barco
from recursos import dados

#classe para conferir conliões
class Colisoes:

    # função para conferir as colisões com o player
    def verificar_colisao(self, objeto):
        if objeto.rect.bottom > (tela.get_height() - 40):
            #objeto.rede_neural.recompensa += objeto.combustivel
            estrategia_evolutiva.gerenciador.desativar_agente(objeto)
            objeto.kill()
            return 1
            
        for ponto in objeto.pontos:
            ponto = (ponto[0].item(), ponto[1].item())
            for alvo in dados.sprites_alvos:
                if alvo.rect.collidepoint(ponto) and alvo.indice == objeto.index_alvo:
                    if objeto.index_alvo < 6:
                        objeto.index_alvo += 1
                        #objeto.rede_neural.recompensa += 300 * objeto.index_alvo
    
    def conferir_pouso(self, objeto):

        for ponto in objeto.pontos[1:]:
            if (ponto[0] > barco.bloco_colisao.left and ponto[0] < barco.bloco_colisao.right) and ponto[1] >= barco.bloco_colisao.top:
                if objeto.angulo_foquete < 100 and objeto.angulo_foquete > 80 and objeto.aceleracao_y < 3:
                    if objeto.index_alvo == 6:
                        objeto.aceleracao_x = 0
                        objeto.aceleracao_y = 0
                        objeto.velocidade_x = 0
                        objeto.velocidade_y = 0
                        objeto.angulo_foquete = 90
                        objeto.rede_neural.recompensa += objeto.combustivel ** 1.7
                        estrategia_evolutiva.gerenciador.desativar_agente(objeto)
                        objeto.kill()
                        dados.sucessos += 1
                        return True

                else:
                    #objeto.rede_neural.recompensa += objeto.combustivel
                    estrategia_evolutiva.gerenciador.desativar_agente(objeto)
                    objeto.kill()
                    break
        return False
       
    # função para chamar as funções de colisão a cada iteração
    def update(self):
        if len(estrategia_evolutiva.gerenciador.agentes) > 0:
             for agente in estrategia_evolutiva.gerenciador.agentes[:]:
                 self.verificar_colisao(agente)
             for agente in estrategia_evolutiva.gerenciador.agentes[:]:
                 self.conferir_pouso(agente)
             for agente in estrategia_evolutiva.gerenciador.agentes[:]:
                 if agente.frames_fora > 60:
                     #agente.rede_neural.recompensa += agente.combustivel
                     estrategia_evolutiva.gerenciador.desativar_agente(agente)
                     agente.kill()

        try:
            if player.jogador.rect.bottom > (tela.get_height() - 40):
                player.jogador.kill()
                player.jogador = None
            else:

                for ponto in player.jogador.pontos:
                    ponto = (ponto[0].item(), ponto[1].item())

                    if ponto[1] > (tela.get_height() - 60):
                        player.jogador.kill()
                        player.jogador = None
                        break
                
                for ponto in player.jogador.pontos[1:]:
                    if (ponto[0] > barco.bloco_colisao.left and ponto[0] < barco.bloco_colisao.right) and ponto[1] >= barco.bloco_colisao.top:
                        if player.jogador.angulo_foquete < 100 and player.jogador.angulo_foquete > 80 and player.jogador.aceleracao_y < 3:
                            if not player.jogador.pousado:
                                player.jogador.aceleracao_x = 0
                                player.jogador.aceleracao_y = 0
                                player.jogador.velocidade_x = 0
                                player.jogador.velocidade_y = 0
                                player.jogador.angulo_foquete = 90
                                return True
                        else:
                            player.jogador.kill()
                            player.jogador = None
                            break
        except Exception as e: pass
