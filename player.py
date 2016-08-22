# -*- coding: utf-8 -*-
# Wizards Magic
# Copyright (C) 2011-2014  https://code.google.com/p/wizards-magic/
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

import os
import random

import pygame

import ai
import cards
import sockets
import wzglobals


current_folder = os.path.dirname(os.path.abspath(__file__))


class Player():  # Прототип игрока
    def __init__(self, game_id=0):
        self.health = 50
        self.name = "player"
        self.nickname = None
        self.action_points = True  # Ходил игрок, или нет
        self.game_id = game_id
        self.get_cards()
        self.mana = {}
        self.get_mana()
        self.element = "none"
        self.ai = False
        self.cards_generated = False
        self.enemy = None

    def get_self_cards(self):
        return (
            wzglobals.ccards_1.sprites()
            if self.id == 1
            else wzglobals.ccards_2.sprites()
        )

    def get_opponent_cards(self):
        return (
            wzglobals.ccards_2.sprites()
            if self.id == 1
            else wzglobals.ccards_1.sprites()
        )

    def damage(self, damage, enemy, cast=False):
        for card in self.get_self_cards():
            card.owner_gets_damage(damage)
        self.health -= damage
        if self.health <= 0:
            wzglobals.gameinformationpanel.display(
                _("Game Over! Player {player} loose!").format(
                    player=self.nickname,
                )
            )
            wzglobals.stage = False

    def heal(self, health):
        self.health += health

    def get_mana(self):
        # маны должно быть 25 в сумме!!
        manas = [
            "water",
            "fire",
            "air",
            "earth",
            "life",
            "death"
        ]
        random.shuffle(manas)  # раскидываем массив рендомно
        sum = 0
        for mana_id in range(0, len(manas)):
            if mana_id != len(manas) - 1:
                rand = random.randint(2, 5)
                sum += rand
                self.mana[manas[mana_id]] = rand
            else:
                self.mana[manas[mana_id]] = 25 - sum

    def get_mana_count(self):  # просмотр кол-ва маны
        return [
            self.mana['water'],
            self.mana['fire'],
            self.mana['air'],
            self.mana['earth'],
            self.mana['life'],
            self.mana['death']
        ]

    def get_cards(self, server_cards=None):
        ''' server_cards = list of cards sent from remote server '''
        self.cards = {}
        tmpcards = {}
        cards_for_sort = {}
        for element in ['water', 'fire', 'air', 'earth', 'life', 'death']:
            tmpcards[element] = {}
            cards_for_sort[element] = []
            for i in range(0, 4):
                # получаем карту элемента воды
                if not server_cards:
                    randnum = random.randint(
                        0,
                        len(wzglobals.games_cards[self.game_id][element]) - 1
                    )
                    card = \
                        wzglobals.games_cards[self.game_id][element][randnum]
                    wzglobals.games_cards[self.game_id][element].remove(card)
                else:
                    card = server_cards[element][i]
                if self.game_id == 0:
                    tmpcards[element][card] = cards.links_to_cards[card]()
                    cards_for_sort[element].append(
                        [
                            tmpcards[element][card].level,
                            tmpcards[element][card]
                        ]
                    )
                else:
                    tmpcards[element][card] = card

            if self.game_id == 0:
                cards_for_sort[element].sort(key=lambda item: item[0])
                for i in range(0, 4):
                    cards_for_sort[element][i][1].position_in_deck = i
        self.cards = tmpcards.copy()

        del cards_for_sort
        del tmpcards


class Player1(Player):
    def __init__(self):
        self.id = 1
        Player.__init__(self)


class Player2(Player):
    def __init__(self):
        self.id = 2
        Player.__init__(self)


def switch_position():
    # wzglobals.attack_started = False
    if wzglobals.attack_started:
        wzglobals.attack_started.pop()
    n = wzglobals.nickname1.name
    wzglobals.nickname1.set_nickname(wzglobals.nickname2.name)
    wzglobals.nickname2.set_nickname(n)
    for cardbox in wzglobals.cardboxes:
        cardbox.opposite = not cardbox.opposite


def me_finish_turn():
    # Добавляем ману другому игроку.
    # wzglobals.attack_started = True
    wzglobals.attack_started.append(True)
    wzglobals.player.enemy.mana['water'] += 1
    wzglobals.player.enemy.mana['fire'] += 1
    wzglobals.player.enemy.mana['air'] += 1
    wzglobals.player.enemy.mana['earth'] += 1
    wzglobals.player.enemy.mana['life'] += 1
    wzglobals.player.enemy.mana['death'] += 1
    # Меняем игрока
    try:
        pygame.mixer.music.load(current_folder+'/misc/sounds/card_attack.ogg')
    except:
        print("Unexpected error: while trying play attack sound")
    wzglobals.playmusic()
    if wzglobals.player.id == 1:
        wzglobals.player = wzglobals.player2
        wzglobals.player.action_points = True
        for card in wzglobals.ccards_1:  # Атакуем
            kill = card.attack()
            if kill:
                card.enemy_die()
            card.used_cast = False
        # вызываем функцию повторения магия
        for spell in wzglobals.magic_cards:
            spell.periodical_cast()
        for card in wzglobals.ccards_2:
            card.turn()
            card.moves_alive += 1
        for card in wzglobals.ccards_2:
            card.additional_turn_action()
    else:
        wzglobals.player = wzglobals.player1
        wzglobals.player.action_points = True
        for card in wzglobals.ccards_2:  # Атакуем
            kill = card.attack()
            if kill:
                card.enemy_die()
            card.used_cast = False
        # вызываем функцию повторения магия
        for spell in wzglobals.magic_cards:
            spell.periodical_cast()
        for card in wzglobals.ccards_1:
            card.turn()
            card.moves_alive += 1
        for card in wzglobals.ccards_1:
            card.additional_turn_action()
    if wzglobals.player.ai:
        cb = ai.select_cardbox()
        if cb:
            c = ai.select_card(cb.card)
            # print 'SELECTED',c
            cb.card = c()
            cb.card.field = True
            wzglobals.player.mana[cb.card.element] -= cb.card.level
            cb.card.parent = cb
            if wzglobals.player.id == 1:
                wzglobals.ccards_1.add(cb.card)
            else:
                wzglobals.ccards_2.add(cb.card)
            cb.card.summon()
        finish_turn()


def finish_turn():
    me_finish_turn()
    sockets.query({"action": "switch_turn"})
    # switch_position()
