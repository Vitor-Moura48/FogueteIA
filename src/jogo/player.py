from .base import Mob
from config.configuracoes import randint, pygame, math, numpy, tela, cache, uniform
from recursos import dados
from ..rede_neural.rede_neural import RedeNeural
from .navio import barco

class Player(Mob):
    def __init__(self, vida, dano, real=False):
        Mob.__init__(self, 'recursos/imagens/rocketg.png', (1, 1), (225, 225), (0, 0), vida, dano, escala=(70, 150))

        self.rede_neural = RedeNeural([8, 16, 3], ['relu', 'sigmoid'], 0, 0.05)

        self.rect.center = dados.center_agentes
        self.antigo_rect = self.rect

        self.forca = 0.5
        self.velocidade_x = 1
        self.velocidade_y = 1
        self.velocidade_angular = 0
        self.angulo_foquete = randint(80, 100)
        self.resistencia_do_ar = 0.01
        self.vento = dados.vento
        self.max_combustivel = 2000
        self.combustivel = 2000

        self.real = real
        self.img = self.image
        self.pontos = self.obter_pontos(self.rect.center, self.angulo_foquete)
        self.pousado = False
        self.index_alvo = 0
        self.frames_fora = 0

        # Carregar a sprite sheet dos propulsores
        self.caminho_do_exhaust = pygame.image.load('recursos/imagens/rocket_exhaust.png').convert_alpha()
        self.exhaust_frames = self.carregar_frames_exhaust(self.caminho_do_exhaust, 4, 5) #carrega os frames com as linhas e colunas

        self.current_exhaust_frame = 0
        self.exhaust_frame_delay = 5  # controla a velocidade da animação
        self.exhaust_frame_counter = 0

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
        self.combustivel -= 1

        self.exhaust_frames.append([self.rect.centerx, self.rect.centery + self.rect.height // 2, (255, 255, 0), 5, 2])
        self.exhaust_frames.append([self.rect.centerx - 10, self.rect.centery + self.rect.height // 2, (255, 165, 0), 7, 2.5])
        self.exhaust_frames.append([self.rect.centerx + 10, self.rect.centery + self.rect.height // 2, (255, 0, 0), 6, 2.2])

    def gravidade(self):
        self.velocidade_y += 0.15
   
    def obter_entradas(self):
        
        velocidade_x_normalizada = self.velocidade_x / 16
        velocidade_y_normalizada = self.velocidade_x / 32
        velocidade_angular_normalizada = self.velocidade_angular / 8

        distancia_angulo = (self.angulo_foquete - 90)
        if distancia_angulo > 180:
            distancia_angulo = 360 - distancia_angulo
        distancia_angulo /= 180

        vento_normalizado = self.vento / dados.max_vento
        combustivel_normalizado = self.combustivel / self.max_combustivel

        entradas = [velocidade_x_normalizada, velocidade_y_normalizada, velocidade_angular_normalizada, distancia_angulo, vento_normalizado, combustivel_normalizado]

        for sprite in dados.sprites_alvos:
            if sprite.indice == self.index_alvo:
                distancia_x_normalizada = (self.rect.centerx - sprite.rect.centerx) / tela.get_size()[0]
                distancia_y_normalizada = (self.rect.centery - sprite.rect.centery) / tela.get_size()[1]
                entradas.extend([distancia_x_normalizada, distancia_y_normalizada])
        
        entradas.extend([0] * (8 - len(entradas))) # preenche com 0 oq faltar
               
        return entradas

    def aplicar_resistencia(self):
        self.velocidade_x -= self.velocidade_x * self.resistencia_do_ar
        self.velocidade_y -= self.velocidade_y * self.resistencia_do_ar
        self.velocidade_angular -= self.velocidade_angular * self.resistencia_do_ar * 10
    
    def estabilidade_foguete(self):
        self.angulo_foquete = self.angulo_foquete + (90 - self.angulo_foquete) * 0.005
    
    def aplicar_vento(self):
        self.velocidade_x += self.vento

    def update(self):
        
        if not self.real:
        
            if self.rect.center == self.antigo_rect.center or self.rect.bottom > dados.dimensoes_janela[1] or self.rect.right < 0 or self.rect.left > dados.dimensoes_janela[0]:
                self.frames_fora += 1
            else:
                self.frames_fora = 0

            self.rede_neural.definir_entrada(self.obter_entradas())
            output = self.rede_neural.obter_saida()

            if output[2]:
                if self.combustivel > 0:
                    self.acelerar(self.rede_neural.estado_atual_da_rede[2] * 2)
                
                    if output[0]:
                        self.mover_esquerda(self.rede_neural.estado_atual_da_rede[0] * 2)
                    if output[1]:
                        self.mover_direita(self.rede_neural.estado_atual_da_rede[1] * 2)

        self.gravidade() if not self.pousado else None
        self.aplicar_vento()
        self.estabilidade_foguete()
        self.aplicar_resistencia()
        self.mover()
        self.draw_exhaust(tela)
       

        self.image = pygame.transform.rotate(self.img, self.angulo_foquete - 90)
        self.rect = self.image.get_rect(center=self.rect.center)
        
        self.pontos = self.obter_pontos(self.rect.center, self.angulo_foquete)

    def carregar_frames_exhaust(self, sprite_sheet, rows, cols):
        frames = []
        sheet_rect = sprite_sheet.get_rect()
        frame_width = sheet_rect.width // cols
        frame_height = sheet_rect.height // rows

        for row in range(rows):
            for col in range(cols):
                frame = sprite_sheet.subsurface(pygame.Rect(
                    col * frame_width, row * frame_height, frame_width, frame_height
                ))
                frames.append(frame)

        return frames

    def draw_exhaust(self, tela):

        exhaust_pos = (self.rect.centerx, self.rect.centery + self.rect.height // 2)
        tela.blit(self.exhaust_frames[self.current_exhaust_frame], exhaust_pos)
            

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
