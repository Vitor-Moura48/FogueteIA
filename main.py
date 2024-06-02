from config.configuracoes import pygame, plano_de_fundo, tela, fps, clock, uniform, randint
from recursos import dados
from src.jogo import player, visualizador, alvo, colisoes
from src.rede_neural import estrategia_evolutiva


def atualizar_objetos():

    # adiconar objetos sprites na tela
    dados.sprites.draw(tela)
    dados.sprites.update()

def finalizar_partida():
    
    dados.vento = uniform(-0.1, 0.1)
    player.jogador = player.Player(2, 1, real=True)

    estrategia_evolutiva.gerenciador.nova_partida()

def responder_a_eventos():
    
    for event in pygame.event.get(): # responder a eventos

        if event.type == pygame.QUIT:
            print("game over")
            quit()

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for agente in dados.sprites_agentes:
                    agente.disparar()

for i in range(3):
    a = alvo.Alvo(i)
dados.vento = uniform(-0.1, 0.1)
estrategia_evolutiva.gerenciador = estrategia_evolutiva.GerenciadorNeural(500, 4, 0.5, player.Player, (2, 1))
estrategia_evolutiva.gerenciador.nova_partida()
visualizador.informacoes = visualizador.Visualizador()
player.jogador = player.Player(2, 1, real=True)
colisao = colisoes.Colisoes()

while True: # loop principal

    if len(estrategia_evolutiva.gerenciador.agentes) == 0 and player.jogador == None:
        finalizar_partida()

    tela.fill((000, 000, 000))
    tela.blit(plano_de_fundo, (0, 0)) # plano de fundo da tela

    atualizar_objetos()

    colisao.update()

    visualizador.informacoes.update()

    responder_a_eventos()

    player.controle.mover()

    pygame.display.flip()  # atualizar a tela
    clock.tick(fps)