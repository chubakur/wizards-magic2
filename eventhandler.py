# -*- coding: utf-8 -*-
#Wizards Magic
#Copyright (C) 2011-2014  https://code.google.com/p/wizards-magic/
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
import wzglobals
import pygame
import cards
import os
import sockets
import menu
from pygame.locals import QUIT, K_0, K_9, K_a, K_z, K_PERIOD, K_RETURN, \
    MOUSEBUTTONDOWN, MOUSEBUTTONUP, MOUSEMOTION
current_folder = os.path.dirname(os.path.abspath(__file__))

class Point(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(current_folder+'/misc/point_alpha.gif').convert_alpha()
        self.rect = self.image.get_rect()
    def draw(self, rect):
        wzglobals.background.blit(self.image, rect)
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(rect)
class Event_handler():
    def __init__(self):
        self.onmouse_element = False
    def event(self, event):
        if event.type == QUIT:
            menu.exit_program()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_ESCAPE:
                if not wzglobals.question:
                    if not 'importantmessage' in wzglobals.__dict__:
                        menu.menu_esc_question()
                    else: #handle ESC key when display importantmessage
                        if wzglobals.cli:
                            if not wzglobals.opponent_disconnect:
                                sockets.query({"action":"bye","player_id":wzglobals.player_id})
                            else:
                                sockets.query({"action":"bbye"})
                        wzglobals.information_group.remove(wzglobals.importantmessage)
                        del wzglobals.importantmessage
                        wzglobals.stage = 0
                        wzglobals.cli = False
                    return
                else:
                    menu.clean_question()
                    return
            if wzglobals.question and (event.key>=K_0 and event.key<=K_9 or event.key>=K_a and event.key<=K_z or event.key==K_PERIOD):
                wzglobals.answer=wzglobals.answer+pygame.key.name(event.key)
            if wzglobals.question and (event.key==K_RETURN or len(wzglobals.answer)>=wzglobals.answer_maxchar):
                exec(wzglobals.answer_cmd)
                menu.clean_question()
                return
            if wzglobals.itemfocus:
                wzglobals.itemfocus.change(event)
        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                wzglobals.point.draw(event.pos)
                if wzglobals.stage==0:
                    collided = pygame.sprite.spritecollide(wzglobals.point, wzglobals.menu_group, 0)
                elif wzglobals.stage<=2:
                    collided = pygame.sprite.spritecollide(wzglobals.point, wzglobals.cards_in_deck, 0)
                    if not collided:
                        collided = pygame.sprite.spritecollide(wzglobals.point, wzglobals.interface, 0)
                    if not collided:
                        collided = pygame.sprite.spritecollide(wzglobals.point, wzglobals.panels, 0)
                if not collided:
                    return
                item = collided[len(collided)-1]
                if item.type == "nicknamewindow":
                    return
                if item.type == "healthwindow":
                    return
                if item.type == 'outer':
                    return
                if item.type == 'button' or item.type == 'txtinput' or item.type == 'checkbox':
                    item.onmousedown()
                    return
                if item.type == "warrior_card": #Карта в колоде! Карта на поле в cardbox
                    #exec('selected_card_0 = cards.' + item.name + '()') #Переменной selected_card_0 присваиваем новый объект
                    wzglobals.selected_card = cards.links_to_cards[item.name]() # из локальной в глобальную
                    if wzglobals.player.id == 1:
                        for cardbox in wzglobals.cardboxes[0:5]:
                            if wzglobals.player.action_points:
                                if cardbox.card.name == "player": #если карты нет
                                    cardbox.light = True
                    else:
                        for cardbox in wzglobals.cardboxes[5:10]:
                            if cardbox.card.name == "player":
                                cardbox.light = True
                    return
                if item.type == "magic_card": #карта магии в колоде
                    if not wzglobals.player.action_points: #если уже ходил
                        wzglobals.gameinformationpanel.display("You've already made a move.")
                        return
                    selected_card = cards.links_to_cards[item.name]()
                    #exec('selected_card = cards.' + item.name + '()') #в переменную selected_card засовываем одну такую карту
                    #exec('available_mana = wzglobals.player.' + selected_card.element + '_mana') # Вычисляем сколько маны у нас есть. Значение помещаем в локальную переменную available_mana
                    available_mana = wzglobals.player.mana[selected_card.element]
                    if available_mana >= selected_card.level:
                        #exec('wzglobals.player.' + selected_card.element + '_mana -= ' + str(selected_card.level)) #Отнимаем ману
                        wzglobals.player.mana[selected_card.element] -= selected_card.level
                        wzglobals.player.action_points = False #ставим запись, что ход сделан
                        selected_card.player = wzglobals.player
                        sockets.query({"action":"card","card":selected_card.name,"type":"magic"})
                        selected_card.cast() #вызываем магию, периодизация делается уже внутри класса, путем добавления в группу wzglobals.magic_cards
                        selected_card.spell_speaker()
                        #Закрываем колоду
                        for cardbox in wzglobals.cardboxes:
                            cardbox.light = False
                    else:
                        wzglobals.gameinformationpanel.display('Not enough mana.')
                    return
                if wzglobals.cast_focus: #выбор цели для каста
                    if item.type == 'cardbox':
                        wzglobals.cast_focus_wizard.focus_cast_action(item.card)
                        sockets.query({"action":"cast","position":wzglobals.cast_focus_wizard.parent.position,"target":item.position,"focus":True})
                if item.player.id != wzglobals.player.id:
                    return
                if wzglobals.cli:
                    if item.player.id != wzglobals.player_id:
                        return
                if item.type == "cardbox": #Если клик на карточный бокс
                    if item.card.name != "player": #Если в этом блоке есть карта
                        if item.card.cast: #если есть каст
                            if not item.card.used_cast: # если еще не кастовали
                                if not item.card.focus_cast:
                                    sockets.query({"action":"cast","position":item.position,"focus":False})
                                item.card.cast_action()
                            else:
                                wzglobals.gameinformationpanel.display("You've already cast.")
                                return
                    if wzglobals.selected_card: #если выбрана карта
                        if item.card.name != 'player':
                            wzglobals.gameinformationpanel.display('This sector is busy.')
                            return
                        if not wzglobals.player.action_points: #если уже ходил
                            wzglobals.gameinformationpanel.display("You've already made a move.")
                            return
                        #отключаем подсветку
                        for cardbox in wzglobals.cardboxes:
                            cardbox.light = False
                        #Выводим карту
                        #exec('available_mana = wzglobals.player.' + wzglobals.selected_card.element + '_mana') # Вычисляем сколько маны у нас есть. Значение помещаем в локальную переменную available_mana
                        available_mana = wzglobals.player.mana[wzglobals.selected_card.element]
                        if available_mana < wzglobals.selected_card.level:
                            wzglobals.gameinformationpanel.display("Not enough mana.")
                            return
                        item.card = wzglobals.selected_card
                        item.card.parent = item
                        sockets.query({"action":"card","card":item.card.name,"position":item.position,"type":"warrior"})
                        #item.card.cardboxes = cardboxes
                        #item.card.playerscards = playerscards
                        item.card.field = True
                        item.card.summon() #функция которая хранит описание действий при выводе карты
                        wzglobals.player.action_points = False
                        #exec('wzglobals.player.' + wzglobals.selected_card.element + '_mana -= ' + str(wzglobals.selected_card.level)) #Отнимаем ману
                        wzglobals.player.mana[wzglobals.selected_card.element] -= wzglobals.selected_card.level
                        #wzglobals.cards_in_deck.empty() #очищаем группу карты в колоде
                        if item.player.id == 1:
                            wzglobals.ccards_1.add(item.card)
                        else:
                            wzglobals.ccards_2.add(item.card)
                        wzglobals.selected_card = 0
            elif event.button == 3: #ПРАВАЯ КНОПКА МЫШИ
                if wzglobals.cast_focus:
                    wzglobals.cast_focus = False
                    for card in wzglobals.ccards_1.sprites()+wzglobals.ccards_2.sprites():
                        card.light_switch(False)
                    return
                wzglobals.point.draw(event.pos)
                collided = pygame.sprite.spritecollide(wzglobals.point, wzglobals.cards_in_deck, 0)
                if not collided:
                    collided = pygame.sprite.spritecollide(wzglobals.point, wzglobals.interface, 0)
                if not collided:
                    collided = pygame.sprite.spritecollide(wzglobals.point, wzglobals.panels, 0)
                if not collided:
                    return
                item = collided[len(collided)-1]
                if item.type == "warrior_card" or item.type == "magic_card" : #по боевой карте
                    wzglobals.card_info_group.add(wzglobals.cardinfo)
                    #wzglobals.cardinfo.text = item.info
                    wzglobals.cardinfo.card = item
                    wzglobals.cardinfo.show = True
                if item.type == "cardbox":
                    if item.card.name != "player":
                        wzglobals.card_info_group.add(wzglobals.cardinfo)
                        #wzglobals.cardinfo.text = item.card.info
                        wzglobals.cardinfo.card = item.card
                        wzglobals.cardinfo.show = True
                if item.type == 'cardsofelementshower':
                    wzglobals.interface.remove(wzglobals.cardsofelementshower1)
                    wzglobals.interface.remove(wzglobals.cardsofelementshower2)
                    wzglobals.cards_in_deck.empty()
                    for cardbox in wzglobals.cardboxes:
                        cardbox.light = False
        elif event.type == MOUSEBUTTONUP: #отпускаем кнопку мыши
            if event.button == 3: #Правую
                if wzglobals.cardinfo.show:
                    wzglobals.cardinfo.show = False
                    wzglobals.card_info_group.empty()
            else: #1
                for elem in wzglobals.interface:
                    if elem.type == 'button':
                        elem.onmouseup()
        elif event.type == MOUSEMOTION:
            wzglobals.point.draw(event.pos)
            if wzglobals.stage==0:
                collided = pygame.sprite.spritecollide(wzglobals.point, wzglobals.menu_group, 0)
            elif wzglobals.stage<=2:
                collided = pygame.sprite.spritecollide(wzglobals.point, wzglobals.interface, 0)
            if not collided:
                if self.onmouse_element:
                    self.onmouse_element.onmouseout()
                    self.onmouse_element = False
                return
            item = collided[len(collided)-1]
            if item.type == 'button':
                if self.onmouse_element != item:
                    item.onmouseout()
                self.onmouse_element = item
                item.onmouse()
#>>>>>>> other
