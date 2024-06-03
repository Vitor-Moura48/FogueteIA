from config.configuracoes import time, pygame, tela, largura, altura
from ..rede_neural import estrategia_evolutiva

class Visualizador:
    def __init__(self):
        self.contador_frames = 0
        self.tempo_inicial = 0
        self.fonte = pygame.font.Font(None, 32)

        self.config_camadas = [14, 16, 8, 4]
        self.espacamentox = 400 / (len(self.config_camadas) + 1)
        self.rects = []

        x = self.espacamentox
        for camada in self.config_camadas:
            self.espacamentoy = 200 / (camada + 1)
            y = self.espacamentoy
            for neuronio in range(camada):
                self.rects.append([(x, y), 5])
                y += self.espacamentoy
            x += self.espacamentox
    
    def visualizar_rede(self):
        if len(estrategia_evolutiva.gerenciador.agentes) > 0:
            pygame.draw.rect(tela, (20, 20, 20), (0, 0, 400, 200))

            cor = (150, 000, 000)
            for i in range(len(self.rects)):
                pygame.draw.circle(tela, cor, self.rects[i][0], self.rects[i][1])


    def update(self):

        #self.visualizar_rede()

        self.contador_frames += 1
        tempo_atual = time.time()
        delta = max(1e-10, tempo_atual - self.tempo_inicial) # nunca zerar
        
        tela.blit(self.fonte.render('fps ' + str(round(self.contador_frames / delta)), True, (255, 000, 000)), (largura * 0.8, altura * 0.05))
        tela.blit(self.fonte.render(f"geração {estrategia_evolutiva.gerenciador.contador_geracoes}", True, (255, 000, 000)), (largura * 0.8, altura * 0.1))
        tela.blit(self.fonte.render(f"partida {estrategia_evolutiva.gerenciador.contador_partidas}", True, (255, 000, 000)), (largura * 0.8, altura * 0.15))

        if (delta) > 0.6: # a cada x segundos, atualiza a taxa de frames
            self.contador_frames = 0
            self.tempo_inicial = tempo_atual

        