from .base import Mob
from config.configuracoes import randint, pygame, math, numpy, tela, cache, uniform
from recursos import dados
from ..rede_neural.rede_neural import RedeNeural
from .navio import barco

class Player(Mob):
    def __init__(self, vida, dano, real=False):
        Mob.__init__(self, 'recursos/imagens/rocketg.png', (1, 1), (225, 225), (0, 0), vida, dano, escala=(70, 150))

        self.rede_neural = RedeNeural([7, 14, 3], ['relu', 'sigmoid'], 0, 0.05)

        self.rect.centerx = randint(barco.rect.left, barco.rect.right)
        self.rect.bottom = randint(150, 400)

        self.forca = 0.7
        self.velocidade_x = 0
        self.velocidade_y = 0
        self.velocidade_angular = 0
        self.angulo_foquete = randint(80, 100)
        self.resistencia_do_ar = 0.01
        self.vento = dados.vento

        self.real = real
        self.img = self.image
        self.pontos = self.obter_pontos(self.rect.center, self.angulo_foquete)
        self.pousado = False
        self.index_alvo = 0
        self.frames_parado = 0

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
            self.rect.x += int(self.velocidade_x)
        if abs(self.velocidade_y) >= 1:
            self.rect.y += int(self.velocidade_y)
    
    def mover_esquerda(self, potencia=1):
        self.velocidade_angular += (self.forca * numpy.cos(numpy.deg2rad(30))) * potencia
        self.angulo_foquete += self.velocidade_angular
        self.angulo_foquete %= 360
    def mover_direita(self, potencia=1):
        self.velocidade_angular += (self.forca * numpy.cos(numpy.deg2rad(150))) * potencia
        self.angulo_foquete += self.velocidade_angular
        self.angulo_foquete %= 360
        
    def acelerar(self, potencia=1):
        self.velocidade_x += self.forca * numpy.cos(numpy.deg2rad(self.angulo_foquete)) * potencia
        self.velocidade_y -= self.forca * numpy.sin(numpy.deg2rad(self.angulo_foquete)) * potencia

    def gravidade(self):
        self.velocidade_y += 0.3
    
    def obter_entradas(self):
        entradas = [self.velocidade_x, self.velocidade_y, self.angulo_foquete, self.rect.centerx, self.rect.centery]

        for sprite in dados.sprites_alvos:
            if sprite.indice == self.index_alvo:
                entradas.extend(sprite.rect.center)
        
        entradas.extend([0] * (7 - len(entradas))) # preenche com 0 oq faltar
               
        return entradas

    def aplicar_resistencia(self):
        self.velocidade_x -= self.velocidade_x * self.resistencia_do_ar
        self.velocidade_y -= self.velocidade_y * self.resistencia_do_ar
        self.velocidade_angular -= self.velocidade_angular * self.resistencia_do_ar * 12
    
    def aplicar_vento(self):
        self.velocidade_x += self.vento

    def update(self):
        
        if not self.real:

            if self.frames_parado > 50:
                self.kill()
            self.rede_neural.recompensa -= 1
            self.rede_neural.definir_entrada(self.obter_entradas())
            output = self.rede_neural.obter_saida()

            if output[2]:
                self.acelerar(self.rede_neural.estado_atual_da_rede[2] * 2)
                
                if output[0]:
                    self.mover_esquerda(self.rede_neural.estado_atual_da_rede[0] * 2)
                if output[1]:
                    self.mover_direita(self.rede_neural.estado_atual_da_rede[1] * 2)

        self.gravidade() if not self.pousado else None
        self.aplicar_vento()
        self.aplicar_resistencia()
        self.mover()

        self.image = pygame.transform.rotate(self.img, self.angulo_foquete - 90)
        self.rect = self.image.get_rect(center=self.rect.center)
        
        self.pontos = self.obter_pontos(self.rect.center, self.angulo_foquete)
        









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
