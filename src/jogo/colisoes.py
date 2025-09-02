from config.configuracoes import *
from . import player
from .navio import barco
from recursos import dados

#classe para conferir conliões
class Colisoes:

    # função para conferir as colisões com o player
    def verificar_colisao(self) -> list[player.Player]:
        agents_to_remove = []

        for agent in dados.sprites_agentes:
            agent: player.Player

            if agent.rect.bottom > (tela.get_height() - 40):
                agents_to_remove.append(agent)
                continue
                
            for ponto in agent.pontos:
                ponto = (ponto[0].item(), ponto[1].item())
                for alvo in dados.sprites_alvos:
                    if alvo.rect.collidepoint(ponto) and alvo.indice == agent.index_alvo:
                        if agent.index_alvo < 6:
                            agent.index_alvo += 1
        
            for ponto in agent.pontos[1:]:
                if (ponto[0] > barco.bloco_colisao.left and ponto[0] < barco.bloco_colisao.right) and ponto[1] >= barco.bloco_colisao.top:
                    if agent.angulo_foquete < 100 and agent.angulo_foquete > 80 and agent.aceleracao_y < 3:
                        if agent.index_alvo == 6:
                            agent.aceleracao_x = 0
                            agent.aceleracao_y = 0
                            agent.velocidade_x = 0
                            agent.velocidade_y = 0
                            agent.angulo_foquete = 90
                            agent.rede_neural.increment_reward(agent.combustivel ** 1.7)

                            agents_to_remove.append(agent)

                            dados.sucessos += 1
                            continue

                    else:

                        agents_to_remove.append(agent)

                        continue

            if agent.frames_fora > 50:

                agents_to_remove.append(agent)
                continue

        return agents_to_remove