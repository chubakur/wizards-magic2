#!/usr/bin/python2
# -*- coding: utf-8 -*-
import pygame.sprite
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

# To change this template, choose Tools | Templates
# and open the template in the editor.
# import pygame.sprite
# Внимание!! Для того, чтоsбы слои не наслаивались, я использую объект
# surface_backup , который является копией изображения.
# После этого они заменяются
# Caution! To chtosby layers are layered, I use an object surface_backup,
# which is a copy of the image. After that, they are replaced
__author__ = "chubakur"
__date__ = "$12.02.2011 12:11:42$"
import pygame
# from pygame.locals import *
import os
import cards
import time
import player
if pygame.version.vernum < (1, 9, 1):
    import copy
import animations
import wzglobals
import elementbutton
import cardinfo
import cardsofelementshower
import completethecoursebutton
import healthwindow
import cardbox
import eventhandler
import gameinformation
import menu
import options
import sockets
import nickname_window
import threading
import important_message
current_folder = os.path.dirname(os.path.abspath(__file__))
wzglobals.current_folder = current_folder


def server_handler():
    handling = True
    while handling:
        gi = sockets.get_package()
        # si = sock.recv(256)
        # print 'si'
        # print si
        # print "RETURN:"
        # print get_package()
        print(gi)
        if gi['action'] == 'join':
            print(("Join to Game with Player_id " + str(gi['id'])))
            wzglobals.player_id = gi['id']
            if wzglobals.player_id == 1:
                player.switch_position()
        elif gi['action'] == 'update':
            # Устанавливаем ники
            # wzglobals.player1.nickname = gi['nicknames'][0]
            # wzglobals.player2.nickname = gi['nicknames'][1]
            wzglobals.nickname1.set_nickname(gi['nicknames'][0])
            wzglobals.nickname2.set_nickname(gi['nicknames'][1])
            # TODO: draw nicknames
            # nickname_window.NicknameWindow((200,10), wzglobals.player1)
            # nickname_window.NicknameWindow((200,400), wzglobals.player2)
            # кидаем ману первому игроку
            manas = [
                "water",
                "fire",
                "air",
                "earth",
                "life",
                "death"
            ]
            for i, element in enumerate(manas):
                wzglobals.player1.mana[element] = gi['mana'][0][i]
                wzglobals.player2.mana[element] = gi['mana'][1][i]
            if (
                wzglobals.player2.cards_generated == 0 and
                wzglobals.player1.cards_generated == 0
            ):
                print("Выдаем карты")
                wzglobals.player1.get_cards(gi['deck_cards'][0])
                wzglobals.player1.cards_generated = True
                # а теперь второму
                wzglobals.player2.get_cards(gi['deck_cards'][1])
                wzglobals.player2.cards_generated = True
            wzglobals.information_group.remove(wzglobals.importantmessage)
            del wzglobals.importantmessage
            wzglobals.gameinformationpanel.display('Battle started.')
        elif gi['action'] == 'switch_turn':
            player.me_finish_turn()
        elif gi['action'] == 'card':
            # print gi
            # if gi['position'] == 0:
            #    cardbox = wzglobals.cardbox0
            if gi['type'] == 'warrior':
                # exec("tmp_card = cards." + gi['card'] + "()")
                tmp_card = cards.links_to_cards[gi['card']]()
                exec(
                    "wzglobals.cardbox" +
                    str(gi['position']) +
                    ".card =  tmp_card"
                )
                exec(
                    "wzglobals.cardbox" +
                    str(gi['position']) +
                    ".card.parent = wzglobals.cardbox" +
                    str(gi['position'])
                )
                exec(
                    "wzglobals.cardbox" +
                    str(gi['position']) +
                    ".card.field = True"
                )
                exec(
                    "wzglobals.cardbox" +
                    str(gi['position']) +
                    ".card.summon()"
                )
                # Отнимаем ману
                wzglobals.player.mana[tmp_card.element] -= tmp_card.level
                exec(
                    "wzglobals.ccards_" +
                    str(wzglobals.player.id) +
                    ".add(wzglobals.cardbox" +
                    str(gi['position']) +
                    ".card)"
                )
                # exec("wzglobals.ccards_2.add(wzglobals.cardbox"+str(gi['position'])+".card)")
                # print wzglobals.player.id,tmp_card
            elif gi['type'] == 'magic':
                # exec("tmp_card = cards." + gi['card'] + "()")
                tmp_card = cards.links_to_cards[gi['card']]()
                # Отнимаем ману
                wzglobals.player.mana[tmp_card.element] -= tmp_card.level
                # ставим запись, что ход сделан
                wzglobals.player.action_points = False
                tmp_card.player = wzglobals.player
                tmp_card.cast()
                wzglobals.gameinformationpanel.display(
                    'Enemy used ' + gi['card']
                )
        elif gi['action'] == 'cast':
            if not gi['focus']:
                exec(
                    'wzglobals.cardbox' +
                    str(gi['position']) +
                    ".card.cast_action()"
                )
            else:  # фокус каст
                exec(
                    'wzglobals.cardbox' +
                    str(gi['position']) +
                    ".card.focus_cast_action(" +
                    "wzglobals.cardbox" +
                    str(gi['target']) +
                    ".card)"
                )
                # if not item.card.used_cast: # если еще не кастовали
                #   item.card.cast_action()
        elif gi['action'] == "opponent_disconnect":
            handling = False
            wzglobals.opponent_disconnect = True
            wzglobals.importantmessage = \
                important_message.MessageWindow(
                    'Sorry, your opponent was disconnected from game.'
                )
            time.sleep(3)
            for s in wzglobals.information_group.sprites():
                if type(s) == important_message.MessageWindow:
                    wzglobals.information_group.remove(s)
            del wzglobals.importantmessage
            wzglobals.stage = 0
            wzglobals.cli = False
        elif gi['action'] == "server_close":
            handling = False
            wzglobals.importantmessage = \
                important_message.MessageWindow('Sorry, server is closing.')
            time.sleep(3)
            for s in wzglobals.information_group.sprites():
                if type(s) == important_message.MessageWindow:
                    wzglobals.information_group.remove(s)
            del wzglobals.importantmessage
            wzglobals.stage = 0
            wzglobals.cli = False
        elif gi['action'] == "value_error":
            handling = False
            wzglobals.importantmessage = \
                important_message.MessageWindow('Socket error. String Null')
            time.sleep(3)
            for s in wzglobals.information_group.sprites():
                if type(s) == important_message.MessageWindow:
                    wzglobals.information_group.remove(s)
            del wzglobals.importantmessage
            wzglobals.stage = 0
            wzglobals.cli = False
        elif gi['action'] == "socket_error":
            handling = False
            wzglobals.importantmessage = \
                important_message.MessageWindow('Socket error.')
            time.sleep(3)
            for s in wzglobals.information_group.sprites():
                if type(s) == important_message.MessageWindow:
                    wzglobals.information_group.remove(s)
            del wzglobals.importantmessage
            wzglobals.stage = 0
            wzglobals.cli = False
    sockets.sock.close()


def load_and_start_bg_music():
    wzglobals.bg_sound = pygame.mixer.Sound(
        current_folder + '/misc/sounds/' +
        '11_the_march_of_the_goblins__tobias_steinmann.ogg'
    )
    wzglobals.bg_sound.play(-1)


def start_game(cli=False, ai=False):
    wzglobals.attack_started = [True]
    wzglobals.background = \
        pygame.image.load(current_folder+'/misc/bg_sample.gif')
    # wzglobals.background = wzglobals.background.convert()
    # wzglobals.background = pygame.Surface(wzglobals.screen.get_size())
    wzglobals.background = wzglobals.background.convert_alpha()
    wzglobals.cards_of_element_shower_element = "water"
    # wzglobals.background.fill((0, 0, 0))
    background_backup = wzglobals.background.copy()
    # font.set_bold(0)
    wzglobals.games_cards[0]['water'] = cards.water_cards_deck.cards[:]
    wzglobals.games_cards[0]['fire'] = cards.fire_cards_deck.cards[:]
    wzglobals.games_cards[0]['air'] = cards.air_cards_deck.cards[:]
    wzglobals.games_cards[0]['earth'] = cards.earth_cards_deck.cards[:]
    wzglobals.games_cards[0]['life'] = cards.life_cards_deck.cards[:]
    wzglobals.games_cards[0]['death'] = cards.death_cards_deck.cards[:]
    if wzglobals.player1:
        wzglobals.player1.enemy = None
        wzglobals.player2.enemy = None
    wzglobals.player1 = player.Player1()
    wzglobals.player2 = player.Player2()
    wzglobals.player1.enemy = wzglobals.player2
    wzglobals.player2.enemy = wzglobals.player1
    wzglobals.player = wzglobals.player1
    # 0 1 2 3 4   //Расположение
    # 5 6 7 8 9
    wzglobals.cardbox0 = \
        cardbox.Cardbox((22, 46), wzglobals.player1, 0)  # 0 место на поле
    wzglobals.cardbox1 = \
        cardbox.Cardbox((172, 46), wzglobals.player1, 1)  # 1 место на поле
    wzglobals.cardbox2 = \
        cardbox.Cardbox((322, 46), wzglobals.player1, 2)  # 2 место на поле
    wzglobals.cardbox3 = \
        cardbox.Cardbox((472, 46), wzglobals.player1, 3)  # 3 место на поле
    wzglobals.cardbox4 = \
        cardbox.Cardbox((622, 46), wzglobals.player1, 4)  # 4 место на поле
    wzglobals.cardbox5 = \
        cardbox.Cardbox((22, 238), wzglobals.player2, 5)  # 5 место на поле
    wzglobals.cardbox6 = \
        cardbox.Cardbox((172, 238), wzglobals.player2, 6)  # 6 место на поле
    wzglobals.cardbox7 = \
        cardbox.Cardbox((322, 238), wzglobals.player2, 7)  # 7 место на поле
    wzglobals.cardbox8 = \
        cardbox.Cardbox((472, 238), wzglobals.player2, 8)  # 8 место на поле
    wzglobals.cardbox9 = \
        cardbox.Cardbox((622, 238), wzglobals.player2, 9)  # 9 место на поле
    wzglobals.cardboxes = [
        wzglobals.cardbox0,
        wzglobals.cardbox1,
        wzglobals.cardbox2,
        wzglobals.cardbox3,
        wzglobals.cardbox4,
        wzglobals.cardbox5,
        wzglobals.cardbox6,
        wzglobals.cardbox7,
        wzglobals.cardbox8,
        wzglobals.cardbox9
    ]  # Ссылки на объекты

    for tcardbox in wzglobals.cardboxes:
        if pygame.version.vernum < (1, 9, 1):
            tcardbox.normal_rect = copy.deepcopy(tcardbox.rect)
            tcardbox.opposite_rect = \
                copy.deepcopy(tcardbox.get_opposite_cardbox().rect)
        else:
            tcardbox.normal_rect = tcardbox.rect.copy()
            tcardbox.opposite_rect = \
                tcardbox.get_opposite_cardbox().rect.copy()
    wzglobals.castlabel = cards.CastLabel()
    # Окошко здоровья верхнего игрока
    healthwindow.HealthWindowEnemy((175, 10))
    healthwindow.HealthWindow((167, 557))  # Окошко здоровья нижнего игрока
    # Кнопки колод стихий первого игрока
    elementbutton.WaterElementShower((246, 2))
    elementbutton.FireElementShower((337, 2))
    elementbutton.AirElementShower((419, 2))
    elementbutton.EarthElementShower((509, 2))
    elementbutton.LifeElementShower((590, 2))
    elementbutton.DeathElementShower((668, 2))
    # Кнопки колод стихий второго игрока
    wzglobals.water_element_button = \
        elementbutton.WaterElementButton((11, 427))
    wzglobals.fire_element_button = \
        elementbutton.FireElementButton((56, 427))
    wzglobals.air_element_button = \
        elementbutton.AirElementButton((101, 427))
    wzglobals.earth_element_button = \
        elementbutton.EarthElementButton((146, 427))
    wzglobals.life_element_button = \
        elementbutton.LifeElementButton((191, 427))
    wzglobals.death_element_button = \
        elementbutton.DeathElementButton((236, 427))
    # Кнопки завершения хода первого и второго игрока.
    completethecoursebutton.CompleteTheCourseButton((758, 378))
    # Окна выбора карты стихии
    wzglobals.cardofelementsshower = \
        cardsofelementshower.CardsOfElementShower()
    wzglobals.nickname2 = \
        nickname_window.NicknameWindow((142, 530), 'Guest')
    wzglobals.nickname1 = \
        nickname_window.NicknameWindow((22, 0), wzglobals.nick)
    if ai:
        wzglobals.player2.ai = True
        wzglobals.nickname2.set_nickname('Computer')
    # стрелочки для сдвига карт в колоде
    # wzglobals.leftarrow = cardsofelementshower.LeftArrow((356, 489))
    # wzglobals.rightarrow = cardsofelementshower.RightArrow((739, 491))
    if not cli:
        wzglobals.gameinformationpanel.display('Battle Started')
        wzglobals.cli = False
        sockets.query = lambda x: x
    else:
        val = sockets.connect()
        if not val:
            wzglobals.gameinformationpanel.display('Cant connect to server.')
            menu.menu_main()
            wzglobals.stage = False
            return 0
        else:
            wzglobals.importantmessage = important_message.MessageWindow(
                'We are waiting for another player'
            )
        sockets.query = sockets.query_
        wzglobals.cli = True
        server_thread = threading.Thread(target=server_handler)
        server_thread.start()
    if not wzglobals.cli:
        player.switch_position()
    # **************************************************************************
    wzglobals.screen.blit(wzglobals.background, (0, 0))
    wzglobals.panels.update()
    wzglobals.interface.update()
    pygame.display.flip()
    sockets.query(
        {
            "action": "join",
            "nickname": wzglobals.nick
        }
    )  # входим в игру
    while wzglobals.stage == 1:
        # if wzglobals.turn_ended and len(cards_attacking) = 0:
        #     for cardbox in wzglobals.cardboxes:
        #         cardbox.opposite = not cardbox.opposite
        for event in pygame.event.get():
            wzglobals.event_handler.event(event)
        wzglobals.panels.update()
        wzglobals.interface.update()
        wzglobals.ccards_1.update()
        wzglobals.ccards_2.update()
        wzglobals.cardofelementsshower.update()
        wzglobals.cards_in_deck.update()
        wzglobals.card_info_group.update()
        wzglobals.information_group.update()
        # interface_up_layer.update()
        wzglobals.screen.blit(wzglobals.background, (0, 0))
        # wzglobals.background.fill((0, 0, 0))
        wzglobals.background = background_backup.copy()
        if wzglobals.animation == "N":
            for item in (
                animations.animations_running +
                animations.cards_attacking +
                animations.cards_dying
            ):
                del item
            animations.animations_running = []
            animations.cards_attacking = []
            animations.cards_dying = []
        if (
            not len(animations.animations_running) and
            len(wzglobals.attack_started)
        ):
            if not wzglobals.cli:
                player.switch_position()
        for animation_running in animations.animations_running:
            animation_running.run()
            if not (
                len(wzglobals.attack_started) and
                len(wzglobals.cards_attacking)
            ):
                if not wzglobals.cli:
                    player.switch_position()
        pygame.display.flip()
        clock.tick(50)


pygame.init()
wzglobals.screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption('Wizards Magic')
clock = pygame.time.Clock()

# read configuration file
options.read_configuration()
if wzglobals.music == "Y":
    music_thread = threading.Thread(target=load_and_start_bg_music)
    music_thread.start()
menu.menu_main()

wzglobals.event_handler = eventhandler.Event_handler()
wzglobals.point = eventhandler.Point()
wzglobals.gameinformationpanel = gameinformation.GameInformationPanel()
wzglobals.cardinfo = cardinfo.CardInfo()

wzglobals.screen.blit(wzglobals.background, (0, 0))

pygame.display.flip()
# noinspection PyPackageRequirements
while 1:
    for event in pygame.event.get():
        wzglobals.event_handler.event(event)
    if wzglobals.stage == 1:
        if wzglobals.cli:
            start_game(1)
        else:
            start_game(ai=wzglobals.ai)
            # start_game(ai=(wzglobals.ai == 'Y'))
        wzglobals.clean()
        menu.menu_main()

    wzglobals.menu_group.update()
    wzglobals.information_group.update()
    wzglobals.screen.blit(wzglobals.background, (0, 0))
    wzglobals.background = wzglobals.background_backup.copy()
    pygame.display.flip()
    clock.tick(50)
