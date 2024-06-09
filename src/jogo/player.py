from .base import Mob
from config.configuracoes import randint, pygame, numpy, tela, cache
from recursos import dados
from ..rede_neural.rede_neural import RedeNeural
from .navio import barco


class Player(Mob):
    def __init__(self, real=False):
        Mob.__init__(self, 'recursos/imagens/sprite_rocket1.png', (1, 4), (132, 132), (0, 0), escala=(73, 110))

        self.rede_neural = RedeNeural([9, 18, 3], ['relu', 'sigmoid'], 0, 0.05)

        self.rect.center = dados.center_agentes
        self.antigo_rect = self.rect

        self.forca = 0.5
        self.aceleracao_x = 0
        self.aceleracao_y = 0
        self.velocidade_x = 0
        self.velocidade_y = 0
        self.velocidade_angular = 0
        self.angulo_foquete = randint(80, 100)
        self.resistencia_do_ar = 0.01
        self.vento = dados.vento
        self.max_combustivel = 1200
        self.combustivel = 1200

        self.real = real
        self.imgs = [self.sprites[0], self.sprites[1], self.sprites[3], self.sprites[2]]
        self.index_imagem = 0
        self.pontos = self.obter_pontos(self.rect.center, self.angulo_foquete)
        self.index_alvo = 0
        self.frames_fora = 0

    #@cache
    def obter_pontos(self, centro, angulo):
        
        x1 = centro[0] + ( numpy.cos(numpy.deg2rad(angulo)) * 35 )
        y1 = centro[1] - ( numpy.sin(numpy.deg2rad(angulo)) * 35 )
        #pygame.draw.circle(tela, (200,200,100), (x1.item(),y1.item()), 3)

        x2 = centro[0] + ( numpy.cos(numpy.deg2rad(angulo + 171)) * 30 )
        y2 = centro[1] - ( numpy.sin(numpy.deg2rad(angulo + 171)) * 30 )
        #pygame.draw.circle(tela, (200,200,100), (x2.item(),y2.item()), 3)

        x3 = centro[0] + ( numpy.cos(numpy.deg2rad(angulo + 191)) * 30 )
        y3 = centro[1] - ( numpy.sin(numpy.deg2rad(angulo + 191)) * 30 ) 

        x4 = centro[0] + ( numpy.cos(numpy.deg2rad(angulo + 191)) * 0 )
        y4 = centro[1] - ( numpy.sin(numpy.deg2rad(angulo + 191)) * 0 ) 
    
        return [(x1, y1), (x2, y2), (x3, y3), (x4, y4)]
    
    def mover(self):
        self.velocidade_x += self.aceleracao_x
        self.velocidade_y += self.aceleracao_y
        
        self.angulo_foquete += self.velocidade_angular
        self.angulo_foquete %= 360 
        
        self.angulo_foquete += self.velocidade_angular
        self.angulo_foquete %= 360
        

        if abs(self.velocidade_x) >= 1:
            self.rect.x += self.velocidade_x
            self.velocidade_x -= int(self.velocidade_x)
        if abs(self.velocidade_y) >= 1:
            self.rect.y += self.velocidade_y
            self.velocidade_y -= int(self.velocidade_y)
    
    def mover_esquerda(self, potencia=1):
        self.velocidade_angular += (self.forca * numpy.cos(numpy.deg2rad(30))) * potencia *0.6
        
    def mover_direita(self, potencia=1):
        self.velocidade_angular += (self.forca * numpy.cos(numpy.deg2rad(150))) * potencia *0.6
       
    def acelerar(self, potencia=1):
        self.aceleracao_x += self.forca * numpy.cos(numpy.deg2rad(self.angulo_foquete)) * potencia
        self.aceleracao_y -= self.forca * numpy.sin(numpy.deg2rad(self.angulo_foquete)) * potencia
        self.combustivel -= potencia

    def gravidade(self):
        self.aceleracao_y += 0.25
   
    def obter_entradas(self):
        
        velocidade_x_normalizada = self.aceleracao_x / 16
        velocidade_y_normalizada = self.aceleracao_y / 32
        velocidade_angular_normalizada = self.velocidade_angular / 8

        distancia_angulo = (self.angulo_foquete - 90)
        if distancia_angulo > 180:
            distancia_angulo = 360 - distancia_angulo
        distancia_angulo /= 180

        vento_normalizado = self.vento / dados.max_vento
        combustivel_normalizado = self.combustivel / self.max_combustivel
        combustivel_normalizado = 0

        entradas = [velocidade_x_normalizada, velocidade_y_normalizada, velocidade_angular_normalizada, distancia_angulo, vento_normalizado, combustivel_normalizado]
        for sprite in dados.sprites_alvos:
            if sprite.indice == self.index_alvo:
                distancia_x_normalizada = (self.rect.centerx - sprite.rect.centerx) / tela.get_size()[0]
                distancia_y_normalizada = (self.rect.centery - sprite.rect.centery) / tela.get_size()[1]
                distancia_navio_normalizada = 0
                if sprite.indice == 6:
                    distancia_navio_normalizada = 1 + distancia_y_normalizada
                    #print(distancia_navio_normalizada)
                    pygame.draw.line(tela, (255,000,000), self.rect.center, sprite.rect.center)    
                entradas.extend([distancia_x_normalizada, distancia_y_normalizada, distancia_navio_normalizada])
                self.rede_neural.recompensa += (1 - numpy.hypot(distancia_x_normalizada, distancia_y_normalizada)) * ((self.index_alvo + 1) ** 1.4)
                #pygame.draw.line(tela, (255,000,000), self.rect.center, sprite.rect.center)    
                
        entradas.extend([0] * (9 - len(entradas))) # preenche com 0 oq faltar
        return entradas

    def aplicar_resistencia(self):
        self.aceleracao_x -= self.aceleracao_x * self.resistencia_do_ar
        self.aceleracao_y -= self.aceleracao_y * self.resistencia_do_ar
        self.velocidade_angular -= self.velocidade_angular * self.resistencia_do_ar * 16
    
    def estabilidade_foguete(self):
        self.angulo_foquete = self.angulo_foquete + (90 - self.angulo_foquete) * 0.04
    
    def aplicar_vento(self):
        self.aceleracao_x += self.vento

    def update(self):
        #pygame.draw.line(tela, (255, 000, 000), self.rect.center, self.raycast(self.pontos[1], self.angulo_foquete, 100))
        if not self.real:
        
            if self.rect.center == self.antigo_rect.center or self.rect.bottom < 0 or self.rect.right < 0 or self.rect.left > dados.dimensoes_janela[0]:
                self.frames_fora += 1
            else:
                self.frames_fora = 0

            self.rede_neural.definir_entrada(self.obter_entradas())
            output = self.rede_neural.obter_saida()

            if output[2]:
                if self.combustivel > 0:
                    self.acelerar(self.rede_neural.estado_atual_da_rede[2] * 2)
                    self.index_imagem = 1
                
                    if output[0]:
                        self.mover_esquerda(self.rede_neural.estado_atual_da_rede[0] * 2)
                        self.index_imagem = 2
                    if output[1]:
                        self.mover_direita(self.rede_neural.estado_atual_da_rede[1] * 2)
                        self.index_imagem = 3
            else:
                self.index_imagem = 0
      

        self.gravidade()
        self.aplicar_vento()
        self.estabilidade_foguete()
        self.aplicar_resistencia()
        self.mover()
       
        self.image = pygame.transform.rotate(self.imgs[self.index_imagem], self.angulo_foquete - 90)
        self.rect = self.image.get_rect(center=self.rect.center)
        self.pontos = self.obter_pontos(self.rect.center, self.angulo_foquete)
        #self.debug()
        #pygame.draw.circle(tela, (200,200,100), self.rect.center, 3)

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
                jogador.index_imagem = 1

                # para mover player ao pressionar tecla, ou joystick
                if pygame.key.get_pressed()[pygame.K_a] or pygame.key.get_pressed()[pygame.K_LEFT] or self.eixo_x <= -0.4:
                    jogador.mover_esquerda()
                    jogador.index_imagem = 2
                if pygame.key.get_pressed()[pygame.K_d] or pygame.key.get_pressed()[pygame.K_RIGHT] or self.eixo_x >= 0.4:
                    jogador.mover_direita()
                    jogador.index_imagem = 3
            else:
                jogador.index_imagem = 0
         
controle = Controle()
jogador = None
