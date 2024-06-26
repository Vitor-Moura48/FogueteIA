from config.configuracoes import pygame, os, randint, tela
from recursos import dados

class Alvo(pygame.sprite.Sprite):
    def __init__(self, indice):
        pygame.sprite.Sprite.__init__(self)
        dados.sprites.add(self)
        dados.sprites_alvos.add(self)
    
        self.sprite = pygame.image.load(os.path.join('recursos/imagens/target.png')).convert_alpha()
        self.image = self.sprite
        self.image = pygame.transform.scale(self.image, (50, 50))

        self.rect = self.image.get_rect()

        self.rect.center = randint(50, 950), randint(50, 300)
        if indice == 6:
            self.rect.center = (630, 480)

        self.indice = indice
    def update(self):
        if self.indice == 6:
            pygame.draw.circle(tela, (100,0,0), self.rect.center, 6)