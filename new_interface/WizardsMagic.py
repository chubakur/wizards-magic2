# -*- coding: utf-8 -*-
import pygame.sprite
#Wizards Magic
#Copyright (C) 2011  сhubakur
#This program is free software; you can redistribute it and/or
#modify it under the terms of the GNU General Public License
#as published by the Free Software Foundation; either version 2
#of the License, or (at your option) any later version.

#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.

#You should have received a copy of the GNU General Public License
#along with this program; if not, write to the Free Software
#Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

# To change this template, choose Tools | Templates
# and open the template in the editor.
#import pygame.sprite
#Внимание!! Для того, чтоsбы слои не наслаивались, я использую объект surface_backup , который является копией изображения. После этого они заменяются
# Caution! To chtosby layers are layered, I use an object surface_backup, which is a copy of the image. After that, they are replaced
__author__ = "chubakur"
__date__ = "$12.02.2011 12:11:42$"
import pygame
from pygame.locals import *
import sys
import os
import player
import globals
import elementbutton
import cards
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
import thread
import important_message
current_folder = os.path.dirname(os.path.abspath(__file__))
globals.current_folder = current_folder
def server_handler():
    while True:
        gi = sockets.get_package()
        #si = sock.recv(256)
        #print 'si'
        #print si
        #print "RETURN:"
        #print get_package()
        print gi
        if gi['action'] == 'join':
            print("Join to Game with Player_id " + str(gi['id']))
            globals.player_id = gi['id']
            if globals.player_id == 1:
                player.switch_position()
        elif gi['action'] == 'update':
            #Устанавливаем ники
            globals.player1.nickname = gi['nicknames'][0]
            globals.player2.nickname = gi['nicknames'][1]
            #TODO: draw nicknames
            #nickname_window.NicknameWindow((200,10), globals.player1)
            #nickname_window.NicknameWindow((200,400), globals.player2)
            #кидаем ману первому игроку
            globals.player1.water_mana = gi['mana'][0][0]
            globals.player1.fire_mana = gi['mana'][0][1]
            globals.player1.air_mana = gi['mana'][0][2]
            globals.player1.earth_mana = gi['mana'][0][3]
            globals.player1.life_mana = gi['mana'][0][4]
            globals.player1.death_mana = gi['mana'][0][5]
            #кидаем ману второму игроку
            globals.player2.water_mana = gi['mana'][1][0]
            globals.player2.fire_mana = gi['mana'][1][1]
            globals.player2.air_mana = gi['mana'][1][2]
            globals.player2.earth_mana = gi['mana'][1][3]
            globals.player2.life_mana = gi['mana'][1][4]
            globals.player2.death_mana = gi['mana'][1][5]
            if globals.player2.cards_generated == 0 and globals.player1.cards_generated == 0:
                print "Выдаем карты"
                globals.player1.water_cards = gi['deck_cards'][0]['water_cards']
                globals.player1.fire_cards = gi['deck_cards'][0]['fire_cards']
                globals.player1.air_cards = gi['deck_cards'][0]['air_cards']
                globals.player1.earth_cards = gi['deck_cards'][0]['earth_cards']
                globals.player1.life_cards = gi['deck_cards'][0]['life_cards']
                globals.player1.death_cards = gi['deck_cards'][0]['death_cards']
                position = 0
                for card in globals.player1.water_cards + globals.player1.fire_cards + globals.player1.air_cards + globals.player1.earth_cards + globals.player1.life_cards + globals.player1.death_cards:
                    exec("globals.player1." + card.lower() + "= cards." + card + "()")
                    exec("globals.player1." + card.lower() + ".position_in_deck = " + str(position))
                    position += 1
                    if position > 3:
                        position = 0
                globals.player1.cards_generated = True
                #а теперь второму
                globals.player2.water_cards = gi['deck_cards'][1]['water_cards']
                globals.player2.fire_cards = gi['deck_cards'][1]['fire_cards']
                globals.player2.air_cards = gi['deck_cards'][1]['air_cards']
                globals.player2.earth_cards = gi['deck_cards'][1]['earth_cards']
                globals.player2.life_cards = gi['deck_cards'][1]['life_cards']
                globals.player2.death_cards = gi['deck_cards'][1]['death_cards']
                position = 0
                for card in globals.player2.water_cards + globals.player2.fire_cards + globals.player2.air_cards + globals.player2.earth_cards + globals.player2.life_cards + globals.player2.death_cards:
                    exec("globals.player2." + card.lower() + "= cards." + card + "()")
                    exec("globals.player2." + card.lower() + ".position_in_deck = " + str(position))
                    position += 1
                    if position > 3:
                        position = 0
                globals.player2.cards_generated = True
            globals.information_group.remove(globals.importantmessage)
            del globals.importantmessage
            globals.gameinformationpanel.display('Battle started.')
        elif gi['action'] == 'switch_turn':
            player.me_finish_turn()
        elif gi['action'] == 'card':
            #print gi
            #if gi['position'] == 0:
                #cardbox = globals.cardbox0
            if gi['type'] == 'warrior':
                exec("tmp_card = cards." + gi['card'] + "()")
                exec("globals.cardbox" + str(gi['position']) + ".card =  tmp_card")
                exec("globals.cardbox" + str(gi['position']) + ".card.parent = globals.cardbox" + str(gi['position']))
                exec("globals.cardbox" + str(gi['position']) + ".card.field = True")
                exec("globals.cardbox" + str(gi['position']) + ".card.summon()")
                exec('globals.player.' + tmp_card.element + '_mana -= ' + str(tmp_card.level)) #Отнимаем ману
                exec("globals.ccards_" + str(globals.player.id) + ".add(globals.cardbox" + str(gi['position']) + ".card)")
                #exec("globals.ccards_2.add(globals.cardbox"+str(gi['position'])+".card)")
                #print globals.player.id,tmp_card
            elif gi['type'] == 'magic':
                exec("tmp_card = cards." + gi['card'] + "()")
                exec('globals.player.' + tmp_card.element + '_mana -= ' + str(tmp_card.level)) #Отнимаем ману
                globals.player.action_points = False #ставим запись, что ход сделан
                tmp_card.player = globals.player
                tmp_card.cast()
                globals.gameinformationpanel.display('Enemy used ' + gi['card'])
        elif gi['action'] == 'cast':
            if not gi['focus']:
                exec('globals.cardbox' + str(gi['position']) + ".card.cast_action()")
            else:#фокус каст
                exec('globals.cardbox' + str(gi['position']) + ".card.focus_cast_action(" + "globals.cardbox" + str(gi['target']) + ".card)")
                   # if not item.card.used_cast: # если еще не кастовали
                             #  item.card.cast_action()
        elif gi['action'] == "opponent_disconnect":
            globals.opponent_disconnect = True
            globals.importantmessage = important_message.MessageWindow('Sorry, your opponent was disconnected from game.')
def start_game(cli=False):
    globals.background = pygame.image.load(current_folder+'/misc/bg_sample.gif')
    #globals.background = globals.background.convert()
    #globals.background = pygame.Surface(globals.screen.get_size())
    globals.background = globals.background.convert_alpha()
    #globals.background.fill((0, 0, 0))
    background_backup = globals.background.copy()
    #font.set_bold(0)
    cards.water_cards = list([c for c in cards.water_cards_deck])
    cards.fire_cards = list([c for c in cards.fire_cards_deck])
    cards.air_cards = list([c for c in cards.air_cards_deck]) 
    cards.earth_cards = list([c for c in cards.earth_cards_deck]) 
    cards.life_cards = list([c for c in cards.life_cards_deck]) 
    cards.death_cards = list([c for c in cards.death_cards_deck]) 
    globals.player1 = player.Player1()
    globals.player2 = player.Player2()
    globals.player1.enemy = globals.player2
    globals.player2.enemy = globals.player1
    globals.player = globals.player1
    ###############################################################################################################
    #ACTIONS
    ###############################################################################################################
    #globals.infopanel1 = infopanel.Infopanel((0, 0), globals.player1) #Инициализация панели верхнего игрока
    #globals.infopanel2 = infopanel.Infopanel((0, 545), globals.player2) #Инициализация панели нижнего игрока
    #globals.actionpanel1 = actionpanel.Actionpanel((0, 25), globals.player1) #Панель с кнопками верхнего игрока
    #globals.actionpanel2 = actionpanel.Actionpanel((0, 570), globals.player2) #Панель с кнопками нижнего игрока
    # 0 1 2 3 4   //Расположение
    # 5 6 7 8 9
    globals.cardbox0 = cardbox.Cardbox((32, 44), globals.player1, 0) #0 место на поле
    globals.cardbox1 = cardbox.Cardbox((187, 44), globals.player1, 1) #1 место на поле
    globals.cardbox2 = cardbox.Cardbox((341, 44), globals.player1, 2) #2 место на поле
    globals.cardbox3 = cardbox.Cardbox((497, 44), globals.player1, 3) #3 место на поле
    globals.cardbox4 = cardbox.Cardbox((651, 44), globals.player1, 4) #4 место на поле
    globals.cardbox5 = cardbox.Cardbox((32, 248), globals.player2, 5) #5 место на поле
    globals.cardbox6 = cardbox.Cardbox((187, 248), globals.player2, 6) #6 место на поле
    globals.cardbox7 = cardbox.Cardbox((341, 248), globals.player2, 7) #7 место на поле
    globals.cardbox8 = cardbox.Cardbox((497, 248), globals.player2, 8) #8 место на поле
    globals.cardbox9 = cardbox.Cardbox((651, 248), globals.player2, 9) #9 место на поле
    globals.cardboxes = [globals.cardbox0, globals.cardbox1, globals.cardbox2, globals.cardbox3, globals.cardbox4, globals.cardbox5, globals.cardbox6, globals.cardbox7, globals.cardbox8, globals.cardbox9] #Ссылки на объекты
    for tcardbox in globals.cardboxes:
        tcardbox.normal_rect = tcardbox.rect.copy()
        tcardbox.opposite_rect = tcardbox.get_opposite_cardbox().rect.copy()
    #playerscards = [globals.ccards_1, globals.ccards_2] #Ссылки
    #exec('Cardbox((640,301),2)')
    #ElementsWindow((0,0),actionpanel1)
    #ElementsWindow((0,0),actionpanel2)
    globals.castlabel = cards.CastLabel()
    healthwindow.HealthWindowEnemy((90, 10)) #Окошко здоровья верхнего игрока
    healthwindow.HealthWindow((90, 464)) #Окошко здоровья нижнего игрока
    # Кнопки колод стихий первого игрока
    elementbutton.WaterElementShower((385, 10))
    elementbutton.FireElementShower((419, 10))
    elementbutton.AirElementShower((450, 10))
    elementbutton.EarthElementShower((480, 10))
    elementbutton.LifeElementShower((514, 10))
    elementbutton.DeathElementShower((546, 10))
    # Кнопки колод стихий второго игрока
    globals.water_element_button = elementbutton.WaterElementButton((176, 429))
    globals.fire_element_button = elementbutton.FireElementButton((207, 429))
    globals.air_element_button = elementbutton.AirElementButton((238, 429))
    globals.earth_element_button = elementbutton.EarthElementButton((269, 429))
    globals.life_element_button = elementbutton.LifeElementButton((300, 429))
    globals.death_element_button = elementbutton.DeathElementButton((331, 429))
    #Кнопки завершения хода первого и второго игрока.
    completethecoursebutton.CompleteTheCourseButton((760, 430))
    #Окна выбора карты стихии
    globals.cardofelementsshower = cardsofelementshower.CardsOfElementShower()
    #стрелочки для сдвига карт в колоде
    globals.leftarrow = cardsofelementshower.LeftArrow((356, 489))
    globals.rightarrow = cardsofelementshower.RightArrow((739, 491))
    if not cli:
        globals.gameinformationpanel.display('Battle Started')
        globals.cli = False
        sockets.query = lambda x: x
    else:
       globals.importantmessage = important_message.MessageWindow('We are waiting for another player')
       sockets.connect()
       sockets.query = sockets.query_
       globals.cli = True
       thread.start_new_thread(server_handler, ())
    if not globals.cli:
       player.switch_position()
    #********************************************************************************
    globals.screen.blit(globals.background, (0, 0))
    globals.panels.update()
    globals.interface.update()
    pygame.display.flip()
    sockets.query({"action":"join", "nickname":globals.nick}) #входим в игру
    while globals.stage == 1:
        #if globals.turn_ended and len(cards_attacking) = 0:
        #    for cardbox in globals.cardboxes:
        #        cardbox.opposite = not cardbox.opposite
        for event in pygame.event.get():
            globals.event_handler.event(event)
        globals.panels.update()
        globals.interface.update()
        if globals.player.id == 1:
            globals.ccards_1.update()
        else:
            globals.ccards_2.update()
        globals.cardofelementsshower.update()
        globals.cards_in_deck.update()
        globals.card_info_group.update()
        globals.information_group.update()
        #interface_up_layer.update()
        globals.screen.blit(globals.background, (0, 0))
        #globals.background.fill((0,0,0))
        globals.background = background_backup.copy()
        if len(globals.animations_running) == False and globals.attack_started:
             if not globals.cli:
                 player.switch_position()
        for animation_running in globals.animations_running:
            animation_running.run()
            if globals.attack_started and len(globals.cards_attacking) == False:
                if not globals.cli:
                  player.switch_position()
        pygame.display.flip()
        clock.tick(50)



pygame.init()
globals.screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption('Wizards Magic')
clock = pygame.time.Clock()

#read configuration file
options.read_configuration()
globals.bg_sound = pygame.mixer.Sound(current_folder+'/misc/sounds/11_the_march_of_the_goblins__tobias_steinmann.ogg')
if globals.music == "Y":
    globals.bg_sound.play(-1)
menu.menu_main()

globals.event_handler = eventhandler.Event_handler()
globals.point = eventhandler.Point()
globals.gameinformationpanel = gameinformation.GameInformationPanel()
globals.cardinfo = cardinfo.CardInfo()

globals.screen.blit(globals.background, (0, 0))

pygame.display.flip()
while 1:
    for event in pygame.event.get():
        globals.event_handler.event(event)
    if globals.stage == 1:
        if globals.cli: 
            start_game(1)
        else:
            start_game()
        globals.clean()
        menu.menu_main()

    globals.menu_group.update()
    globals.information_group.update()
    globals.screen.blit(globals.background, (0, 0))
    globals.background = globals.background_backup.copy()
    pygame.display.flip()
    clock.tick(50)    
