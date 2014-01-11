# -*- coding: utf-8 -*-
import pygame
import globals
import os
current_folder = os.path.dirname(os.path.abspath(__file__))

class Cardbox(pygame.sprite.Sprite):
    def __init__(self, rect, player, position):
        pygame.sprite.Sprite.__init__(self)
        self.type = 'cardbox'
        self.position = position
        self.location = rect
        self.player = player #ссылка на игрока
        self.opposite = False
        self.image = pygame.image.load(current_folder+'/misc/cardbox_bg.gif').convert_alpha()
        self.light_image = pygame.image.load(current_folder+'/misc/cardbox-activated.gif').convert_alpha()
        self.surface_backup = self.image.copy()
        self.rect = self.image.get_rect().move((rect[0], rect[1]))
        self.card = self.player
        self.light = False
        globals.panels.add(self)
    def get_opposite_cardbox(self):
        if self.position < 5:
            opposite_position = self.position + 5 #Id - блока, куда атаковать
        else:
            opposite_position = self.position - 5
        return globals.cardboxes[opposite_position]
    def draw(self):
        #self.image = self.surface_backup.copy()
        if self.light:
            self.image.blit(self.light_image,(0,0))
            if not self.opposite:
                self.rect = self.normal_rect
            else:
                self.rect = self.opposite_rect
            globals.background.blit(self.image, self.rect)
            self.image = self.surface_backup.copy()
            return
        if not self.opposite:
            self.rect = self.normal_rect
        else:
            self.rect = self.opposite_rect
        globals.background.blit(self.image, self.rect)
    def update(self):
        self.draw()
