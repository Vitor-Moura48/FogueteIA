from config.configuracoes import pygame, plano_de_fundo, tela, fps, clock, uniform, randint, dimensoes_janela
from recursos import dados
from src.jogo import player, visualizador, alvo, colisoes
from src.rede_neural import estrategia_evolutiva


def atualizar_objetos():

    # adiconar objetos sprites na tela
    dados.sprites.draw(tela)
    dados.sprites.update()

def finalizar_partida():
    dados.sucessos = 0

    for sprite in dados.sprites_alvos:
        sprite.kill()
    for indice in range(7):
        alvo.Alvo(indice)

    dados.vento = 0#uniform(-dados.max_vento, dados.max_vento)

    dados.center_agentes = (randint(int(dimensoes_janela[0] * 0.1), int(dimensoes_janela[0] * 0.9)), randint(int(dimensoes_janela[1] * 0.3), int(dimensoes_janela[1] * 0.6)))

    player.jogador = player.Player(real=True)

    estrategia_evolutiva.gerenciador.nova_partida()


def responder_a_eventos():
    
    for event in pygame.event.get(): # responder a eventos

        if event.type == pygame.QUIT:
            print("game over")
            quit()

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for agente in dados.sprites_agentes:
                    agente.disparar()

for indice in range(7):
    alvo.Alvo(indice)

estrategia_evolutiva.gerenciador = estrategia_evolutiva.GerenciadorNeural(500, 6, 0.4, player.Player)
estrategia_evolutiva.gerenciador.nova_partida()
player.jogador = player.Player(real=True)
colisao = colisoes.Colisoes()
dados.vento = 0#uniform(-dados.max_vento, dados.max_vento)
visualizador.informacoes.criar_grafico()

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