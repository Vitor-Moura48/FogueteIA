from config.configuracoes import pygame, tela, largura, altura
import json, time, os
import matplotlib.pyplot as plt 
from recursos import dados

import json
import matplotlib.pyplot as plt

class Visualizador:
    def __init__(self):
        self.contador_frames = 0
        self.tempo_inicial = 0
        self.fonte = pygame.font.Font(None, 32)

    def criar_grafico(self):
        try:
            plt.close()
        except: pass

        dados = self.ler_json()
        _, ax = plt.subplots()
        bars = ax.bar(list(range(1, dados['geracao'] + 1)), dados['records'])
        plt.xticks(range(1, dados['geracao'] + 1))
        plt.show()
        
    def ler_json(self):
        if os.path.exists("recursos/saves/informacoes.json"):
            with open("recursos/saves/informacoes.json", 'r') as arquivo:
                return json.load(arquivo)
        else:
            return {'records': [0]}

    def update(self, contador_geracoes, contador_partidas):

        #self.visualizar_rede()

        self.contador_frames += 1
        tempo_atual = time.time()
        delta = max(1e-10, tempo_atual - self.tempo_inicial) # nunca zerar
        
        tela.blit(self.fonte.render('fps ' + str(round(self.contador_frames / delta)), True, (255, 000, 000)), (largura * 0.8, altura * 0.05))
        tela.blit(self.fonte.render(f"geração {contador_geracoes}", True, (255, 000, 000)), (largura * 0.8, altura * 0.1))
        tela.blit(self.fonte.render(f"partida {contador_partidas}", True, (255, 000, 000)), (largura * 0.8, altura * 0.15))
        tela.blit(self.fonte.render(f"agentes {len(dados.sprites_agentes)}", True, (255, 000, 000)), (largura * 0.8, altura * 0.2))
        tela.blit(self.fonte.render(f"sucessos {dados.sucessos}", True, (255, 000, 000)), (largura * 0.8, altura * 0.25))

        if (delta) > 0.6: # a cada x segundos, atualiza a taxa de frames
            self.contador_frames = 0
            self.tempo_inicial = tempo_atual

informacoes = Visualizador()