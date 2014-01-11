# -*- coding: utf-8 -*-
#Client
import pygame
pygame.font.init()
panels = pygame.sprite.Group() #Нижний уровень
interface = pygame.sprite.Group() #Уровень кнопок
cards_in_deck = pygame.sprite.Group() #Уровень дополнительный
ccards_1 = pygame.sprite.Group() #  Карты, которые вывел первый игрок
ccards_2 = pygame.sprite.Group() # Карты, которые вывел второй игрок
magic_cards = pygame.sprite.Group() #Использующаяся магия
cards_of_element_shower_element = "" #какой элемент показывать
selected_card = False #Выбранная карта
card_info_group = pygame.sprite.Group() #  Группа, которая содержит спрайт, содержащий панель вывода информации о карте
font = pygame.font.Font("misc/Domestic_Manners.ttf", 15)
font2 = pygame.font.Font("misc/DroidSerif-Italic.ttf", 13)
#print pygame.font.match_font('Arial')
screen = None
player = None
opponent_disconnect = False
#player1 = None
#player2 = None
players = []
#Каст с выбором цели
cast_focus = False #включен ли режим
cast_focus_wizard = None # ссылка на кастующий объект ( не цель ! )
#cast_focus_filter = None
information_group = pygame.sprite.Group() #Группа, содержащая панель вывода игровой информации