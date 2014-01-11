# -*- coding: utf-8 -*-
import globals
import os
import pygame
current_folder = os.path.dirname(os.path.abspath(__file__))

#globals.cards_of_element_shower_element содержит стихию
class LeftArrow(pygame.sprite.Sprite):
    def __init__(self, rect):
        pygame.sprite.Sprite.__init__(self)
        self.type = 'button'
        self.image_normal = pygame.image.load(current_folder+'/misc/book_button_left_normal.gif')
        self.image_onmouse = pygame.image.load(current_folder+'/misc/book_button_left_onmouse.gif')
        self.image_onclick = pygame.image.load(current_folder+'/misc/book_button_left_onclick.gif')
        self.image = self.image_normal
        self.rect = self.image.get_rect().move(rect)
        globals.interface.add(self)
    def onmousedown(self):
        self.image = self.image_onclick
        globals.cardofelementsshower.first_part = True
    def onmouse(self):
        self.image = self.image_onmouse
    def onmouseout(self):
        self.image = self.image_normal
    def onmouseup(self):
        self.image = self.image_normal
    def draw(self):
        globals.background.blit(self.image, self.rect)
    def update(self):
        self.draw()
class RightArrow(pygame.sprite.Sprite):
    def __init__(self, rect):
        pygame.sprite.Sprite.__init__(self)
        self.type = 'button'
        self.image_normal = pygame.image.load(current_folder+'/misc/book_button_right_normal.gif')
        self.image_onmouse = pygame.image.load(current_folder+'/misc/book_button_right_onmouse.gif')
        self.image_onclick = pygame.image.load(current_folder+'/misc/book_button_right_onclick.gif')
        self.image = self.image_normal
        self.rect = self.image.get_rect().move(rect)
        globals.interface.add(self)
    def onmousedown(self):
        self.image = self.image_onclick
        globals.cardofelementsshower.first_part = False
    def onmouse(self):
        self.image = self.image_onmouse
    def onmouseout(self):
        self.image = self.image_normal
    def onmouseup(self):
        self.image = self.image_normal
    def draw(self):
        globals.background.blit(self.image, self.rect)
    def update(self):
        self.draw()
class CardsOfElementShower(pygame.sprite.Sprite):
    #Не прототип!
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        #self.player = player
        self.type = 'cardsofelementshower'
        #self.rect = self.image.get_rect().move((rect[0], rect[1]))
        self.cards = 0
        self.shift = 2
        self.first_part = True #True - shows 1,2,3 from list, False shows 2,3,4 elements
    def draw(self):
        pass
        #globals.background.blit(self.image, self.rect)
    def update(self):
        #print self.type, 'update'
        globals.cards_in_deck.empty()
        if globals.cli:
            if globals.player_id != globals.player.id:
                return
        if globals.cards_of_element_shower_element == "water":
            if self.first_part:
                for card in globals.player.water_cards[0:3]:
                    exec("globals.cards_in_deck.add(globals.player." + card.lower() + ")")
            else:
                for card in globals.player.water_cards[1:4]:
                    exec("globals.cards_in_deck.add(globals.player." + card.lower() + ")")
        elif globals.cards_of_element_shower_element == "fire":
            if self.first_part:
                for card in globals.player.fire_cards[0:3]:
                    exec("globals.cards_in_deck.add(globals.player." + card.lower() + ")")
            else:
                for card in globals.player.fire_cards[1:4]:
                    exec("globals.cards_in_deck.add(globals.player." + card.lower() + ")")
        elif globals.cards_of_element_shower_element == "air":
            if self.first_part:
                for card in globals.player.air_cards[0:3]:
                    exec("globals.cards_in_deck.add(globals.player." + card.lower() + ")")
            else:
                for card in globals.player.air_cards[1:4]:
                    exec("globals.cards_in_deck.add(globals.player." + card.lower() + ")")
        elif globals.cards_of_element_shower_element == "earth":
            if self.first_part:
                for card in globals.player.earth_cards[0:3]:
                    exec("globals.cards_in_deck.add(globals.player." + card.lower() + ")")
            else:
                for card in globals.player.earth_cards[1:4]:
                    exec("globals.cards_in_deck.add(globals.player." + card.lower() + ")")
        elif globals.cards_of_element_shower_element == "life":
            if self.first_part:
                for card in globals.player.life_cards[0:3]:
                    exec("globals.cards_in_deck.add(globals.player." + card.lower() + ")")
            else:
                for card in globals.player.life_cards[1:4]:
                    exec("globals.cards_in_deck.add(globals.player." + card.lower() + ")")
        else:
            if self.first_part:
                for card in globals.player.death_cards[0:3]:
                    exec("globals.cards_in_deck.add(globals.player." + card.lower() + ")")
            else:
                for card in globals.player.death_cards[1:4]:
                    exec("globals.cards_in_deck.add(globals.player." + card.lower() + ")")
