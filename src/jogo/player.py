from .base import Mob
from config.configuracoes import randint, pygame, math, numpy, tela, cache
from recursos import dados
from ..rede_neural.rede_neural import RedeNeural
from .navio import barco

class Player(Mob):
    def __init__(self, vida, dano, real=False):
        Mob.__init__(self, 'recursos/imagens/rocketg.png', (1, 1), (225, 225), (0, 0), vida, dano, escala=(70, 150))

        self.rede_neural = RedeNeural([4, 8, 8, 3], ['relu', 'relu', 'sigmoid'], 0, 0.05)

        self.rect.centerx = randint(barco.rect.left, barco.rect.right)
        self.rect.bottom = barco.rect.top

        self.forca = 0.7
        self.velocidade_x = 0
        self.velocidade_y = 0
        self.angulo_foquete = 90

        self.real = real
        self.img = self.image
        self.pontos = self.obter_pontos(self.rect.center, self.angulo_foquete)
        self.pousado = False

    @cache
    def obter_pontos(self, centro, angulo):
        x1 = centro[0] + ( numpy.cos(numpy.deg2rad(angulo)) * 50 )
        y1 = centro[1] - ( numpy.sin(numpy.deg2rad(angulo)) * 50 )

        x2 = centro[0] + ( numpy.cos(numpy.deg2rad(angulo + 171)) * 45 )
        y2 = centro[1] - ( numpy.sin(numpy.deg2rad(angulo + 171)) * 45 )

        x3 = centro[0] + ( numpy.cos(numpy.deg2rad(angulo + 191)) * 45 )
        y3 = centro[1] - ( numpy.sin(numpy.deg2rad(angulo + 191)) * 45 ) 
    
        return [(x1, y1), (x2, y2), (x3, y3)]

    def mover(self):
        if abs(self.velocidade_x) >= 1:
            self.rect.x += self.velocidade_x
        if abs(self.velocidade_y) >= 1:
            self.rect.y += self.velocidade_y
    
    def mover_esquerda(self):
        self.angulo_foquete += (self.forca * numpy.cos(numpy.deg2rad(30)))
        self.angulo_foquete %= 360
    def mover_direita(self):
        self.angulo_foquete += (self.forca * numpy.cos(numpy.deg2rad(150)))
        self.angulo_foquete %= 360
        
    def acelerar(self):
        self.velocidade_x += self.forca * numpy.cos(numpy.deg2rad(self.angulo_foquete))
        self.velocidade_y -= self.forca * numpy.sin(numpy.deg2rad(self.angulo_foquete))

    def gravidade(self):
        self.velocidade_y += 0.3
    
    def obter_entradas(self):
        entradas = [self.rect.centerx, self.rect.centery]
        
        entradas.extend([0] * (4 - len(entradas))) # preenche com 0 oq faltar
               
        return entradas

    def conferir_pouso(self):

        for ponto in self.pontos[1:]:
            if (ponto[0] > barco.rect.left and ponto[0] < barco.rect.right) and ponto[1] >= barco.rect.top:
                if self.angulo_foquete < 100 and self.angulo_foquete > 80:
                    if not self.pousado:
                        self.velocidade_x = 0
                        self.velocidade_y = 0
                        return True
                else:
                    self.kill()
        return False

    def update(self):
    
        if not self.real:
            self.rede_neural.recompensa += 1
            self.rede_neural.definir_entrada(self.obter_entradas())
            output = self.rede_neural.obter_saida()

            if output[2]:
                self.acelerar()

                if output[0]:
                    self.mover_esquerda()
                if output[1]:
                    self.mover_direita()
            
        self.gravidade() if not self.pousado else None
        self.mover()

        self.image = pygame.transform.rotate(self.img, self.angulo_foquete - 90)
        self.rect = self.image.get_rect(center=self.rect.center)
            
        for ponto in self.pontos:
            if ponto[0] < 0 or ponto[0] > tela.get_width():
                self.kill()
            elif ponto[1] < 0 or ponto[1] > (tela.get_height() - 60):
                self.kill()
        
        self.pontos = self.obter_pontos(self.rect.center, self.angulo_foquete)
        self.pousado = True if self.conferir_pouso() else False
        











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
            if pygame.key.get_pressed()[pygame.K_SPACE] or self.eixo_y <= -0.4:
                jogador.acelerar()

                # para mover player ao pressionar tecla, ou joystick
                if pygame.key.get_pressed()[pygame.K_a] or pygame.key.get_pressed()[pygame.K_LEFT] or self.eixo_x <= -0.4:
                    jogador.mover_esquerda()
                if pygame.key.get_pressed()[pygame.K_d] or pygame.key.get_pressed()[pygame.K_RIGHT] or self.eixo_x >= 0.4:
                    jogador.mover_direita()
         
            
        
controle = Controle()
jogador = None
