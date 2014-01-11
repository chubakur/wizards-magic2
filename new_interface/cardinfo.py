# -*- coding: utf-8 -*-
import pygame
import globals
import os
current_folder = os.path.dirname(os.path.abspath(__file__))

class CardInfo(pygame.sprite.Sprite):
    """ class to display information about a card """
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.type = 'cardinfo'
        #self.image = pygame.Surface((450, 300))
        #self.image = self.image.convert()
        #self.image.fill((0, 0, 0))
        self.image = pygame.image.load(current_folder+'/misc/card_information.gif').convert_alpha()
        self.surface_backup = self.image.copy()
        self.rect = (globals.screen.get_size()[0] / 2-self.image.get_size()[0] / 2, globals.screen.get_size()[1] / 2-self.image.get_size()[1] / 2)
        self.show = False
        self.text = ""
        self.card = None
        self.symbol_size = 8 #Размер символа по Х. Нужно для расчета переноса строк
        self.distance_between_rows = 20 #расстояние между строками
        self.symbols_in_row = int(self.image.get_size()[0] / self.symbol_size)
    def draw(self):
        self.text = self.card.info
        if self.card.type == "warrior_card":
            self.text += "\nSpells: "
            if not self.card.spells:
                self.text += "None"
            else:
                for spell in self.card.spells:
                    self.text += spell.name + " ; "
        self.image = self.surface_backup.copy()
        self.text = self.text.split('\n')
        last_y_offset = 0
        for ptext in self.text:
            rows = len(ptext) / self.symbols_in_row
            if len(ptext) % self.symbols_in_row:
                rows += 1
            for row in xrange(0, rows):
                text = globals.font.render(ptext[row * self.symbols_in_row:self.symbols_in_row * ( 1 + row)], True, (255, 255, 255))
                self.image.blit(text, (0, last_y_offset + self.distance_between_rows * row))
            last_y_offset = last_y_offset + self.distance_between_rows * rows
        globals.background.blit(self.image, self.rect)
    def update(self):
        self.draw()
