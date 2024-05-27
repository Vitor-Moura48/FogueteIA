from .base import Mob
from config.configuracoes import randint, pygame, math, numpy, tela
from recursos import dados
from ..rede_neural.rede_neural import RedeNeural

class Player(Mob):
    def __init__(self, vida, dano, real=False):
        Mob.__init__(self, 'recursos/imagens/rocket.png', (1, 1), (124, 335), (0, 0), vida, dano, escala=(30, 110))

        self.rede_neural = RedeNeural([4, 8, 8, 3], ['relu', 'relu', 'sigmoid'], 0, 0.05)

        self.rect.centerx = randint(100, 500)
        self.rect.centery = randint(500, 600)

        self.forca = 0.7
        self.velocidade_x = 0
        self.velocidade_y = 0
        self.angulo_foquete = 90

        self.real = real
    
    def mover(self):
        if abs(self.velocidade_x) >= 1:
            self.rect.x += self.velocidade_x
        if abs(self.velocidade_y) >= 1:
            self.rect.y += self.velocidade_y
    
    def mover_esquerda(self):
        self.angulo_foquete += (self.forca * numpy.cos(numpy.deg2rad(30))) % 360
    def mover_direita(self):
        self.angulo_foquete -= (self.forca * numpy.cos(numpy.deg2rad(30))) % 360
        
    def acelerar(self):

        self.velocidade_x += self.forca * numpy.cos(numpy.deg2rad(self.angulo_foquete))
        self.velocidade_y -= self.forca * numpy.sin(numpy.deg2rad(self.angulo_foquete))

    def gravidade(self):
        self.velocidade_y += 0.5
    
    def obter_entradas(self):
        entradas = [self.rect.centerx, self.rect.centery]
        
        entradas.extend([0] * (4 - len(entradas))) # preenche com 0 oq faltar
               
        return entradas

    def update(self):

        if not self.real:
            self.rede_neural.recompensa += 1
            self.rede_neural.definir_entrada(self.obter_entradas())
            output = self.rede_neural.obter_saida()

            if output[0]:
                self.mover_esquerda()
            if output[1]:
                self.mover_direita()
            if output[2]:
                self.acelerar()

        else: # temporário (só para saber o angulo de rotação do foquete)
            fimx = self.rect.centerx + ( numpy.cos(numpy.deg2rad(self.angulo_foquete)) * 100 )
            fimy = self.rect.centery - ( numpy.sin(numpy.deg2rad(self.angulo_foquete)) * 100 )
            pygame.draw.line(tela, (255, 000, 255), self.rect.center, (fimx, fimy), 4)

        self.gravidade()
        self.mover()
            
        if self.rect.left < 0:
            self.rect.left = 0
            self.velocidade_x = 0
        elif self.rect.right > dados.dimensoes_janela[0]:
            self.rect.right = dados.dimensoes_janela[0]
            self.velocidade_x = 0
        if self.rect.top < 0:
            self.rect.top = 0
            self.velocidade_y = 0
        elif self.rect.bottom > dados.dimensoes_janela[1]:
            self.rect.bottom = dados.dimensoes_janela[1]
            self.velocidade_y = 0
        

class Controle:  # criar classe para resolver coisas sobre controle
    def __init__(self):

        self.eixo_x = 0
        self.eixo_y = 0

        self.iniciar_joy()
    
    def iniciar_joy(self):
        
        quantidade_joysticks = pygame.joystick.get_count() # verificar se há joysticks
        if quantidade_joysticks > 0:
            self.controle = pygame.joystick.Joystick(0)
            self.controle.init()
    
    def conferir_joystik(self, event):
        eixo_joystick = event.axis
        if eixo_joystick == 0:
            self.eixo_x = event.value
        if eixo_joystick == 1:
            self.eixo_y = event.value
    
    def mover(self):
        if jogador != None:

            # para mover player ao pressionar tecla, ou joystick
            if pygame.key.get_pressed()[pygame.K_a] or pygame.key.get_pressed()[pygame.K_LEFT] or self.eixo_x <= -0.4:
                jogador.mover_esquerda()
            if pygame.key.get_pressed()[pygame.K_d] or pygame.key.get_pressed()[pygame.K_RIGHT] or self.eixo_x >= 0.4:
                jogador.mover_direita()
         
            if pygame.key.get_pressed()[pygame.K_SPACE] or self.eixo_y <= -0.4:
                jogador.acelerar()
        
controle = Controle()
jogador = None
