# -*- coding: utf-8 -*-
import globals
import pygame
class CardsOfElementShower(pygame.sprite.Sprite):
    #Не прототип!
    def __init__(self, rect, player):
        pygame.sprite.Sprite.__init__(self)
        self.player = player
        self.type = 'cardsofelementshower'
        self.image = pygame.image.load('misc/cards_box.gif').convert_alpha()
        self.rect = self.image.get_rect().move((rect[0], rect[1]))
        self.cards = 0
        self.shift = 32
    def draw(self):
        globals.background.blit(self.image, self.rect)
    def update(self):
        if self.player.id != globals.player.id:
            return
        self.cards = 0
        #{МОЖНО УПРОСТИТЬ АЛГОРИТМ!}&?????
        if self.player.id == 1:
            if globals.cards_of_element_shower_element == "water":
                for card in globals.player1.water_cards:
                    exec("globals.cards_in_deck.add(globals.player1." + card.lower() + ")")
            elif globals.cards_of_element_shower_element == "fire":
                for card in globals.player1.fire_cards:
                    exec("globals.cards_in_deck.add(globals.player1." + card.lower() + ")")
            elif globals.cards_of_element_shower_element == "air":
                for card in globals.player1.air_cards:
                    exec("globals.cards_in_deck.add(globals.player1." + card.lower() + ")")
            elif globals.cards_of_element_shower_element == "earth":
                for card in globals.player1.earth_cards:
                    exec("globals.cards_in_deck.add(globals.player1." + card.lower() + ")")
            elif globals.cards_of_element_shower_element == "life":
                for card in globals.player1.life_cards:
                    exec("globals.cards_in_deck.add(globals.player1." + card.lower() + ")")
            else:
                for card in globals.player1.death_cards:
                    exec("globals.cards_in_deck.add(globals.player1." + card.lower() + ")")
        else:
            if globals.cards_of_element_shower_element == "water":
                for card in globals.player2.water_cards:
                    exec("globals.cards_in_deck.add(globals.player2." + card.lower() + ")")
            elif globals.cards_of_element_shower_element == "fire":
                for card in globals.player2.fire_cards:
                    exec("globals.cards_in_deck.add(globals.player2." + card.lower() + ")")
            elif globals.cards_of_element_shower_element == "air":
                for card in globals.player2.air_cards:
                    exec("globals.cards_in_deck.add(globals.player2." + card.lower() + ")")
            elif globals.cards_of_element_shower_element == "earth":
                for card in globals.player2.earth_cards:
                    exec("globals.cards_in_deck.add(globals.player2." + card.lower() + ")")
            elif globals.cards_of_element_shower_element == "life":
                for card in globals.player2.life_cards:
                    exec("globals.cards_in_deck.add(globals.player2." + card.lower() + ")")
            else:
                for card in globals.player2.death_cards:
                    exec("globals.cards_in_deck.add(globals.player2." + card.lower() + ")")
        self.draw()