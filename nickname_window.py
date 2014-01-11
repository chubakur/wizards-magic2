# To change this template, choose Tools | Templates
# and open the template in the editor.
import globals
import pygame
#TODO: cout as globals.player
class NicknameWindow(pygame.sprite.Sprite):
    def __init__(self,rect, nickname):
        pygame.sprite.Sprite.__init__(self)
        self.type = 'nicknamewindow'
        #self.rect = rect
        self.name = nickname
        self.nickname = globals.font2.render(self.name, True, (255,255,255))
        self.rect = self.nickname.get_rect()
        self.rect = self.rect.move(rect)
        globals.interface.add(self)
    def draw(self):
        #return
        globals.background.blit(self.nickname, self.rect)
    def set_nickname(self, nickname):
        self.name = nickname
        self.nickname = globals.font2.render(nickname, True, (255,255,255))
    def update(self):
        self.draw()

