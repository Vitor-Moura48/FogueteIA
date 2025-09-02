from config.configuracoes import pygame, plano_de_fundo, tela, fps, clock, dimensoes_janela
from recursos import dados
from src.jogo import player, visualizador, alvo, colisoes
from src.rede_neural.estrategia_evolutiva import GerenciadorNeural
from random import uniform, randint

import time
from concurrent.futures import ThreadPoolExecutor

executor = ThreadPoolExecutor(12)

def update_objects():

    dados.sprites.draw(tela)
    list(executor.map(lambda sprite: sprite.update(), dados.sprites))

def reset_game_state(wind_force=0):
    dados.sucessos = 0

    for sprite in dados.sprites_alvos:
        sprite.kill()
    for indice in range(7):
        alvo.Alvo(indice)

    dados.vento = uniform(-wind_force, wind_force)

    dados.center_agentes = (randint(int(dimensoes_janela[0] * 0.1), int(dimensoes_janela[0] * 0.9)), randint(int(dimensoes_janela[1] * 0.3), int(dimensoes_janela[1] * 0.6)))

    player.jogador = player.Player(real=True)

def spawn_agents(amount):
    for index in range(amount):
        agent = player.Player()
        agent.rede_neural = ES.get_nn(index)

def verify_match_end():

    if len(dados.sprites_agentes) == 0: # se todos os agentes morreram, reinicia o jogo
        reset_game_state()

        ES.new_match(num_agentes)
        ES.save_generation()
        spawn_agents(num_agentes)

ES: GerenciadorNeural = GerenciadorNeural(1, 2, 0.1, 0.1, [9, 18, 3], ['relu', 'sigmoid'], True)
colisao = colisoes.Colisoes()
visualizador.informacoes = visualizador.Visualizador() 
   
num_agentes = 200

reset_game_state()
ES.load_model()
ES.new_match(num_agentes)
spawn_agents(num_agentes)

while True: # loop principal

    tela.fill((000, 000, 000))
    tela.blit(plano_de_fundo, (0, 0)) # plano de fundo da tela

    update_objects()
  
    for object in colisao.verificar_colisao():
        ES.account_agent(object.rede_neural)
        object.kill()
        verify_match_end()

    visualizador.informacoes.update(ES.generation_counter, ES.matches_counter)

    for event in pygame.event.get(): 
        if event.type == pygame.QUIT:
            print("game over")
            quit()

    player.controle.mover()

    pygame.display.flip()  # atualizar a tela

    clock.tick(fps)