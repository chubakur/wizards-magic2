# -*- coding: utf-8 -*-
import pygame
import globals
class Infopanel(pygame.sprite.Sprite):
    def __init__(self, rect, player):
        pygame.sprite.Sprite.__init__(self)
        self.type = 'infopanel'
        self.player = player
        #self.image = pygame.Surface((screen.get_size()[0],screen.get_size()[1]/25))
        self.image = pygame.image.load('misc/infopanel_bg.gif').convert_alpha()
        #self.image.convert()
        #self.image.fill((0,0,255))
        self.rect = self.image.get_rect().move((rect[0], rect[1]))
        globals.panels.add(self)
    def draw(self):
        globals.background.blit(self.image, self.rect)
    def update(self):
        self.draw()