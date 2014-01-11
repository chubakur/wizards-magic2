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
pygame.init()
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
globals.infopanel1 = infopanel.Infopanel((0, 0), globals.player1) #Инициализация панели верхнего игрока #Initialize the top player's panel
globals.infopanel2 = infopanel.Infopanel((0, 545), globals.player2) #Инициализация панели нижнего игрока #Initialize the bottom player's panel
globals.actionpanel1 = actionpanel.Actionpanel((0, 25), globals.player1) #Панель с кнопками верхнего игрока #Button panel (top player)
globals.actionpanel2 = actionpanel.Actionpanel((0, 570), globals.player2) #Панель с кнопками нижнего игрока #Button panel (bottom player)
# 0 1 2 3 4   //Расположение //Locations
# 5 6 7 8 9
globals.cardbox0 = cardbox.Cardbox((0, 55), globals.player1, 0) #0 место на поле #Position 0 on the field
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
#playerscards = [globals.ccards_1, globals.ccards_2] #Ссылки #Links
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
globals.gameinformationpanel.display('Battle started.')
#********************************************************************************
globals.screen.blit(globals.background, (0, 0))
globals.panels.update()
globals.interface.update()
pygame.display.flip()
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
    clock.tick(10)
