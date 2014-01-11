import cards
# -*- coding: utf-8 -*-
import json
#import pygame.sprite
#Wizards Magic Server
#Copyright (C) 2011  сhubakur
#This program is free software; you can redistribute it and/or
#modify it under the terms of the GNU General Public License
#as published by the Free Software Foundation; either version 2
#of the License, or (at your option) any later version.
#
#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License
#along with this program; if not, write to the Free Software
#Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
#
# To change this template, choose Tools | Templates
# and open the template in the editor.
#import pygame.sprite
#Внимание!! Для того, чтоsбы слои не наслаивались, я использую объект surface_backup , который является копией изображения. После этого они заменяются
#__author__ = "chubakur"
#__date__ = "$12.02.2011 12:11:42$"
#import pygame
#from pygame.locals import *
#Коды answ
#100 - NO
#200 - OK
#300 - ping packag
#400 - service message
import sys
import player
import globals
#import elementbutton
#import cards
import socket
import json
import threading
#host = "192.168.1.100"
host = "192.168.1.106"
port = 7712
sockets = [] #сокеты игроков
sockets.append([])
connections = [] #подключения
connections.append([])
class Connect(threading.Thread):
    def get_package(self):
        MSGLEN, answ = int( self.sock.recv(8) ), ''
        while len(answ)<MSGLEN: answ += self.sock.recv(MSGLEN - len(answ))
        #print "ANSW",answ
        return json.loads(answ)
    def __init__(self, sock, addr):
        self.sock = sock
        self.addr = addr
        global connections
        self.game_id = game_id
        #if players>=2:
         #   self.sock.send(json.dumps({"answ":100, "players":len(connections[self.game_id])}))
         #   return
        self.id = players
        #self.game = False
        sockets[self.game_id].append(self.sock)
        connections[self.game_id].append(self)
        threading.Thread.__init__(self)
    def send(self, sock, msg):
        msg = json.dumps(msg)
        service = '%08i'%len(msg)
        #service = json.dumps(service)
        sock.send(service)
        sock.send(msg)
    def run(self):
        while True:
            query = self.get_package()
            if query['action'] == "join":
                global players,game_id
                players+=1
                self.nickname = query['nickname']
                #print player
                globals.players[self.game_id].append(player.Player())
                id = len(globals.players[self.game_id]) - 1
                globals.players[self.game_id][id].id = players
                #массив игроки. Элемент 0 - 1 игрок , элемент 1 - второй игрок
                #Отправляем сообщение , что все прошло Гуд, id игрока
                self.send(self.sock, {"answ":200, "action":"join","id":globals.players[self.game_id][id].id})
                if players == 2: #когда заходит второй игрок. раздаем карты и ману.
                    #p_id = 0
                    players = 0
                    game_id += 1
                    sockets.append([])
                    connections.append([])
                    globals.players.append([])
                    cards.water_cards = cards.water_cards_copy[:]
                    cards.fire_cards = cards.fire_cards_copy[:]
                    cards.air_cards = cards.air_cards_copy[:]
                    cards.earth_cards = cards.earth_cards_copy[:]
                    cards.life_cards = cards.life_cards_copy[:]
                    cards.death_cards = cards.death_cards_copy[:]
                    for gamer in globals.players[self.game_id]: #GAMER = PLAYER. просто почему-то питон неверно обрабатывает в таком случае сообщения
                        gamer.get_mana()
                        gamer.get_cards()
                    deck_cards = []
                    deck_cards.append({"water_cards": globals.players[self.game_id][0].water_cards,"fire_cards":globals.players[self.game_id][0].fire_cards, "air_cards":globals.players[self.game_id][0].air_cards,"earth_cards":globals.players[self.game_id][0].earth_cards, "life_cards":globals.players[self.game_id][0].life_cards, "death_cards":globals.players[self.game_id][0].death_cards})
                    deck_cards.append({"water_cards": globals.players[self.game_id][1].water_cards,"fire_cards":globals.players[self.game_id][1].fire_cards, "air_cards":globals.players[self.game_id][1].air_cards,"earth_cards":globals.players[self.game_id][1].earth_cards, "life_cards":globals.players[self.game_id][1].life_cards, "death_cards":globals.players[self.game_id][1].death_cards})
                    for connection in connections[self.game_id]:
                        #p_id += 1
                        self.send(connection.sock,{"answ":200,"nicknames":[connections[self.game_id][0].nickname,connections[self.game_id][1].nickname] ,"action":"update","mana":[globals.players[self.game_id][0].get_mana_count(), globals.players[self.game_id][1].get_mana_count()], "deck_cards":deck_cards})
            elif query['action'] == "switch_turn":
                if self.id:
                    self.send(sockets[self.game_id][0],{"answ":200,"action":"switch_turn"})
                else:
                    self.send(sockets[self.game_id][1],{"answ":200,"action":"switch_turn"})
            elif query['action'] == "card":
                #print query
                if self.id:
                    #self.send()
                    if query['type'] == 'warrior':
                        self.send(sockets[self.game_id][0], {"answ":200,"action":"card","card":query['card'],"position":query['position'],"type":query['type']})
                    else:
                        self.send(sockets[self.game_id][0], {"answ":200,"action":"card","card":query['card'],"type":query['type']})
                else:
                    if query['type'] == 'warrior':
                        self.send(sockets[self.game_id][1], {"answ":200,"action":"card","card":query['card'],"position":query['position'],"type":query['type']})
                    else:
                        self.send(sockets[self.game_id][1], {"answ":200,"action":"card","card":query['card'],"type":query['type']})
            elif query['action'] == 'cast':
                if self.id:
                    if not query['focus']:
                        self.send(sockets[self.game_id][0], {"answ":200,"action":"cast","position":query['position'],"focus":False})
                    else:
                        self.send(sockets[self.game_id][0], {"answ":200,"action":"cast","position":query['position'],"target":query['target'],"focus":True})
                else:
                    if not query['focus']:
                        self.send(sockets[self.game_id][1], {"answ":200,"action":"cast","position":query['position'],"focus":False})
                    else:
                        self.send(sockets[self.game_id][1], {"answ":200,"action":"cast","position":query['position'],"target":query['target'],"focus":True})
            elif query['action'] == 'bye':
                global players,game_id
                players = 0
                game_id += 1
                connections.append([])
                sockets.append([])
                globals.players.append([])
                try:
                    if query['player_id'] == 1:
                      self.send(sockets[self.game_id][1], {"answ":200,"action":"opponent_disconnect"})
                    else:
                       self.send(sockets[self.game_id][0], {"answ":200,"action":"opponent_disconnect"})
                except IndexError:
                    print 'Player has left, not waiting for another'
                #print "Client ",query['player_id'],"disconnected"
                self.sock.close()
                break
            elif query['action'] == 'bbye':
                self.sock.close()
                break
            else:
                self.send(socket, {"answ":300})
        self.sock.close()
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((host, port))
s.listen(5)
players = 0
game_id = 0 # идентификатор игры
while True:
    sock, addr = s.accept()
    Connect(sock, addr).start()
