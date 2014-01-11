# -*- coding: utf-8 -*-
import thread
import pygame.sprite
#Wizards Magic Multi-Player Client
#Copyright (C) 2011 chubakur@gmail.com
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
__author__ = "chubakur"
__date__ = "$12.02.2011 12:11:42$"
import pygame
from pygame.locals import *
try:
    pygame.display.init()
except pygame.error:
    import os
    os.environ['SDL_VIDEODRIVER'] = 'windib' # to avoid 'No available video device' error for old PC
import sys
import player
import globals
import elementbutton
import cards
import cardinfo
import cardsofelementshower
import completethecoursebutton
import healthwindow
import cardbox
import infopanel
import actionpanel
import eventhandler
import gameinformation
import sockets
import nickname_window
import important_message
#host = "192.168.1.100"
#port = 7712
#sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#sock.connect((host, port))
pygame.init()
try:
    nickname_file = file("nickname","r")
    nickname = nickname_file.readline()
    nickname_file.close()
except IOError:
    nickname = "player"
globals.screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption('Wizards Magic')
clock = pygame.time.Clock()
globals.background = pygame.Surface(globals.screen.get_size())
globals.background = globals.background.convert()
globals.background.fill((0, 0, 0))
#font.set_bold(0)
globals.player1 = player.Player1()
globals.player2 = player.Player2()
globals.player1.enemy = globals.player2
globals.player2.enemy = globals.player1
globals.player = globals.player1
globals.point = eventhandler.Point()
globals.cardinfo = cardinfo.CardInfo()
###############################################################################################################
#ACTIONS
#################################################################################################3
globals.event_handler = eventhandler.Event_handler()
globals.infopanel1 = infopanel.Infopanel((0, 0), globals.player1) #Инициализация панели верхнего игрока
globals.infopanel2 = infopanel.Infopanel((0, 545), globals.player2) #Инициализация панели нижнего игрока
globals.actionpanel1 = actionpanel.Actionpanel((0, 25), globals.player1) #Панель с кнопками верхнего игрока
globals.actionpanel2 = actionpanel.Actionpanel((0, 570), globals.player2) #Панель с кнопками нижнего игрока
# 0 1 2 3 4   //Расположение
# 5 6 7 8 9
globals.cardbox0 = cardbox.Cardbox((0, 55), globals.player1, 0) #0 место на поле
globals.cardbox1 = cardbox.Cardbox((160, 55), globals.player1, 1) #1 место на поле
globals.cardbox2 = cardbox.Cardbox((320, 55), globals.player1, 2) #2 место на поле
globals.cardbox3 = cardbox.Cardbox((480, 55), globals.player1, 3) #3 место на поле
globals.cardbox4 = cardbox.Cardbox((640, 55), globals.player1, 4) #4 место на поле
globals.cardbox5 = cardbox.Cardbox((0, 301), globals.player2, 5) #5 место на поле
globals.cardbox6 = cardbox.Cardbox((160, 301), globals.player2, 6) #6 место на поле
globals.cardbox7 = cardbox.Cardbox((320, 301), globals.player2, 7) #7 место на поле
globals.cardbox8 = cardbox.Cardbox((480, 301), globals.player2, 8) #8 место на поле
globals.cardbox9 = cardbox.Cardbox((640, 301), globals.player2, 9) #9 место на поле
globals.cardboxes = [globals.cardbox0, globals.cardbox1, globals.cardbox2, globals.cardbox3, globals.cardbox4, globals.cardbox5, globals.cardbox6, globals.cardbox7, globals.cardbox8, globals.cardbox9] #Ссылки на объекты
#playerscards = [globals.ccards_1, globals.ccards_2] #Ссылки
#exec('Cardbox((640,301),2)')
#ElementsWindow((0,0),actionpanel1)
#ElementsWindow((0,0),actionpanel2)
healthwindow.HealthWindow((0, 0), globals.infopanel1) #Окошко здоровья верхнего игрока
healthwindow.HealthWindow((0, 0), globals.infopanel2) #Окошко здоровья нижнего игрока
# Кнопки колод стихий первого игрока
elementbutton.WaterElementButton((0, 0), globals.actionpanel1)
elementbutton.FireElementButton((31, 0), globals.actionpanel1)
elementbutton.AirElementButton((62, 0), globals.actionpanel1)
elementbutton.EarthElementButton((93, 0), globals.actionpanel1)
elementbutton.LifeElementButton((124, 0), globals.actionpanel1)
elementbutton.DeathElementButton((155, 0), globals.actionpanel1)
# Кнопки колод стихий второго игрока
elementbutton.WaterElementButton((0, 0), globals.actionpanel2)
elementbutton.FireElementButton((31, 0), globals.actionpanel2)
elementbutton.AirElementButton((62, 0), globals.actionpanel2)
elementbutton.EarthElementButton((93, 0), globals.actionpanel2)
elementbutton.LifeElementButton((124, 0), globals.actionpanel2)
elementbutton.DeathElementButton((155, 0), globals.actionpanel2)
#Кнопки завершения хода первого и второго игрока.
completethecoursebutton.CompleteTheCourseButton((760, 0), globals.actionpanel1)
completethecoursebutton.CompleteTheCourseButton((760, 0), globals.actionpanel2)
#Окна выбора карты стихии
globals.cardsofelementshower1 = cardsofelementshower.CardsOfElementShower((0, 301), globals.player1)
globals.cardsofelementshower2 = cardsofelementshower.CardsOfElementShower((0, 55), globals.player2)
globals.gameinformationpanel = gameinformation.GameInformationPanel()
globals.importantmessage = important_message.MessageWindow('We are waiting for another player')
#globals.gameinformationpanel.display('Battle started.')
#********************************************************************************
globals.screen.blit(globals.background, (0, 0))
globals.panels.update()
globals.interface.update()
pygame.display.flip()
sockets.query({"action":"join","nickname":nickname[0:-1]}) #входим в игру
def server_handler():
    while True:
        gi = sockets.get_package()
        #si = sock.recv(256)
        #print 'si'
        #print si
        #print "RETURN:"
        #print get_package()
        if gi['action'] == 'join':
            print("Join to Game with Player_id "+str(gi['id']))
            globals.player_id = gi['id']
        elif gi['action'] == 'update':
            #Устанавливаем ники
            globals.player1.nickname = gi['nicknames'][0]
            globals.player2.nickname = gi['nicknames'][1]
            nickname_window.NicknameWindow((200,0), globals.infopanel1)
            nickname_window.NicknameWindow((200,0), globals.infopanel2)
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
                for card in globals.player1.water_cards + globals.player1.fire_cards + globals.player1.air_cards + globals.player1.earth_cards + globals.player1.life_cards + globals.player1.death_cards:
                    exec("globals.player1."+card.lower()+"= cards."+card+"()")
                globals.player1.cards_generated = True
                #а теперь второму
                globals.player2.water_cards = gi['deck_cards'][1]['water_cards']
                globals.player2.fire_cards = gi['deck_cards'][1]['fire_cards']
                globals.player2.air_cards = gi['deck_cards'][1]['air_cards']
                globals.player2.earth_cards = gi['deck_cards'][1]['earth_cards']
                globals.player2.life_cards = gi['deck_cards'][1]['life_cards']
                globals.player2.death_cards = gi['deck_cards'][1]['death_cards']
                for card in globals.player2.water_cards + globals.player2.fire_cards + globals.player2.air_cards + globals.player2.earth_cards + globals.player2.life_cards + globals.player2.death_cards:
                    exec("globals.player2."+card.lower()+"= cards."+card+"()")
                globals.player2.cards_generated = True
            globals.information_group.remove(globals.importantmessage)
            del globals.importantmessage
        elif gi['action'] == 'switch_turn':
            player.me_finish_turn()
        elif gi['action'] == 'card':
            #print gi
            #if gi['position'] == 0:
                #cardbox = globals.cardbox0
            if gi['type'] == 'warrior':
                exec("tmp_card = cards."+gi['card']+"()")
                exec("globals.cardbox"+str(gi['position'])+".card =  tmp_card")
                exec("globals.cardbox"+str(gi['position'])+".card.parent = globals.cardbox"+str(gi['position']))
                exec("globals.cardbox"+str(gi['position'])+".card.field = True")
                exec("globals.cardbox"+str(gi['position'])+".card.summon()")
                exec('globals.player.' + tmp_card.element + '_mana -= ' + str(tmp_card.level)) #Отнимаем ману
                exec("globals.ccards_"+str(globals.player.id)+".add(globals.cardbox"+str(gi['position'])+".card)")
                #exec("globals.ccards_2.add(globals.cardbox"+str(gi['position'])+".card)")
                #print globals.player.id,tmp_card
            elif gi['type'] == 'magic':
                exec("tmp_card = cards."+gi['card']+"()")
                exec('globals.player.' + tmp_card.element + '_mana -= ' + str(tmp_card.level)) #Отнимаем ману
                globals.player.action_points = False #ставим запись, что ход сделан
                tmp_card.player = globals.player
                tmp_card.cast()
                globals.gameinformationpanel.display('Enemy used '+gi['card'])
        elif gi['action'] == 'cast':
            if not gi['focus']:
                exec('globals.cardbox'+str(gi['position'])+".card.cast_action()")
            else:#фокус каст
                exec('globals.cardbox'+str(gi['position'])+".card.focus_cast_action("+"globals.cardbox"+str(gi['target'])+".card)")
                   # if not item.card.used_cast: # если еще не кастовали
                             #  item.card.cast_action()
        elif gi['action'] == "opponent_disconnect":
            globals.opponent_disconnect = True
            globals.importantmessage = important_message.MessageWindow('Sorry, your opponent was been disconnected from game.')
thread.start_new_thread(server_handler, ())
while 1:
    for event in pygame.event.get():
        globals.event_handler.event(event)
    globals.panels.update()
    globals.interface.update()
    if globals.player.id == 1:
        globals.ccards_1.update(None)
        globals.cards_in_deck.update(globals.cardsofelementshower1)
    else:
        globals.ccards_2.update(None)
        globals.cards_in_deck.update(globals.cardsofelementshower2)
    globals.card_info_group.update()
    globals.information_group.update()
    #interface_up_layer.update()
    globals.screen.blit(globals.background, (0, 0))
    globals.background.fill((0, 0, 0))
    pygame.display.flip()
    #print a
    clock.tick(10)
sock.close()
