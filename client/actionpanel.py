# -*- coding: utf-8 -*-
import pygame
import globals
class Actionpanel(pygame.sprite.Sprite):
    def __init__(self, rect, player):
        pygame.sprite.Sprite.__init__(self)
        self.type = 'actionpanel'
        self.player = player
        self.image = pygame.image.load('misc/actionpanel_bg.gif').convert_alpha()
        self.surface_backup = self.image.copy()
        self.rect = self.image.get_rect().move((rect[0], rect[1]))
        globals.panels.add(self)
    def draw(self):
        globals.background.blit(self.image, self.rect)
        self.image = self.surface_backup.copy()
    def update(self):
        self.draw()