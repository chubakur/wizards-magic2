# To change this template, choose Tools | Templates
# and open the template in the editor.
import globals
import pygame
class NicknameWindow(pygame.sprite.Sprite):
    def __init__(self,rect,player):
        pygame.sprite.Sprite.__init__(self)
        self.type = 'nicknamewindow'
        #self.rect = rect
        self.player = player
        self.nickname = globals.font2.render(self.player.nickname, True, (255,255,255))
        self.rect = self.nickname.get_rect()
        self.rect = self.rect.move(rect)
        globals.interface.add(self)
    def draw(self):
        #return
        self.panel.image.blit(self.nickname, self.rect)
    def update(self):
        self.draw()

