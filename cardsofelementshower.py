# -*- coding: utf-8 -*-
import globals
import os
import pygame
#globals.cards_of_element_shower_element содержит стихию
class CardsOfElementShower(pygame.sprite.Sprite):
    #Не прототип!
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        #self.player = player
        self.type = 'cardsofelementshower'
        #self.rect = self.image.get_rect().move((rect[0], rect[1]))
        self.cards = 0
        self.shift = 2
        #self.first_part = True #True - shows 1,2,3 from list, False shows 2,3,4 elements
    def draw(self):
        pass
        #globals.background.blit(self.image, self.rect)
    def update(self):
        #print self.type, 'update'
        globals.cards_in_deck.empty()
        if globals.cli:
            if globals.player_id != globals.player.id:
                return
        if not globals.cli or  globals.player.cards_generated: 
            for card in globals.player.cards[globals.cards_of_element_shower_element]:
                #exec("globals.cards_in_deck.add(globals.player." + card.lower() + ")")
                globals.cards_in_deck.add(globals.player.cards[globals.cards_of_element_shower_element][card])
