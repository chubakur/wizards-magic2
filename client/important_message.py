import pygame.sprite
# To change this template, choose Tools | Templates
# and open the template in the editor.

__author__="chubakur"
__date__ ="$17.03.2011 16:55:19$"
import pygame
import globals
class MessageWindow(pygame.sprite.Sprite):
    def __init__(self,message):
        pygame.sprite.Sprite.__init__(self)
        self.type = 'informationwindow'
        self.image = pygame.Surface(globals.screen.get_size())
        self.image.fill((0,0,0))
        text = globals.font.render(message,True,(255,255,255))
        self.image.blit(text,(globals.screen.get_size()[0]/2 - text.get_size()[0]/2,globals.screen.get_size()[1]/2))
        globals.information_group.add(self)
    def draw(self):
        globals.background.blit(self.image,(0,0))
    def update(self):
        self.draw()