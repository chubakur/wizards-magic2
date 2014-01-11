# -*- coding: utf-8 -*-
#import pygame
import cards
import random
import globals
import sockets
import pygame
#CLIENT!
class Player(): #Прототип игрока
    def __init__(self):
        self.health = 50
        self.name = "player"
        self.cards_generated = False
        self.action_points = True #Ходил игрок, или нет
        self.water_cards = []
        self.fire_cards = []
        self.air_cards = []
        self.earth_cards = []
        self.life_cards = []
        self.death_cards = []
        self.water_mana = 0
        self.fire_mana = 0
        self.air_mana = 0
        self.earth_mana = 0
        self.life_mana = 0
        self.death_mana = 0
    def damage(self, damage, enemy, cast = False):
        self.health -= damage
        if self.health <= 0:
            globals.gameinformationpanel.display("Game Over!")
    def heal(self, health):
        self.health += health
class Player1(Player):
    def __init__(self):
        self.id = 1
        #self.nickname = "player1"
        Player.__init__(self)
class Player2(Player):
    def __init__(self):
        self.id = 2
        #self.nickname = "player2"
        Player.__init__(self)
def me_finish_turn():
    #Добавляем ману другому игроку.
    globals.player.enemy.water_mana += 1
    globals.player.enemy.fire_mana += 1
    globals.player.enemy.air_mana += 1
    globals.player.enemy.earth_mana += 1
    globals.player.enemy.life_mana += 1
    globals.player.enemy.death_mana += 1
    #Меняем игрока
    if globals.player.id == 1:
        globals.player = globals.player2
        globals.player.action_points = True
        for spell in globals.magic_cards: #вызываем функцию повторения магия
            spell.periodical_cast()
        for card in globals.ccards_1: #Атакуем
            kill = card.attack()
            if kill:
                card.enemy_die()
            card.used_cast = False
        for card in globals.ccards_2:
            card.turn()
        for card in globals.ccards_2:
            card.additional_turn_action()
    else:
        globals.player = globals.player1
        globals.player.action_points = True
        for spell in globals.magic_cards: #вызываем функцию повторения магия
            spell.periodical_cast()
        for card in globals.ccards_2: #Атакуем
            kill = card.attack()
            if kill:
                card.enemy_die()
            card.used_cast = False
        for card in globals.ccards_1:
            card.turn()
        for card in globals.ccards_1:
            card.additional_turn_action()
def finish_turn():
    me_finish_turn()
    sockets.query({"action":"switch_turn"})