# -*- coding: utf-8 -*-
import pygame
import globals
import threading
import os
current_folder = os.path.dirname(os.path.abspath(__file__))

class GameInformationPanel(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.type = "gameinformationpanel"
        self.image = pygame.image.load(current_folder+'/misc/game_information.gif').convert_alpha()
        self.surface_backup = self.image.copy()
        self.rect = (globals.screen.get_size()[0] / 2-self.image.get_size()[0] / 2, globals.screen.get_size()[1] / 2-self.image.get_size()[1] / 2)
        self.show = False
        self.text = ""
        self.auto_hide_time = 0.7
        self.timer = threading.Timer(self.auto_hide_time, self.hide)
        globals.information_group.add(self)
    def draw(self):
        if not self.show:
            return 
        self.image = self.surface_backup.copy()
        text = globals.font.render(self.text, True, (255,255,255))
        self.image.blit(text, (0,0))
        globals.background.blit(self.image, self.rect)
    def update(self):
        self.draw()
    def hide(self):
        self.timer = threading.Timer(self.auto_hide_time, self.hide)
        self.show = False
    def display(self,text, persistent=False):
        if self.show:
            self.text = text
            return
        self.text = text
        self.show = True
        if not persistent:
            self.timer.start()
