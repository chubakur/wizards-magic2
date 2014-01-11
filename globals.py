# -*- coding: utf-8 -*-
import pygame

pygame.font.init()
panels = pygame.sprite.Group() #Нижний уровень #Lower Level
interface = pygame.sprite.Group() #Уровень кнопок #Button Level
cards_in_deck = pygame.sprite.Group() #Уровень дополнительный #The level of additional
ccards_1 = pygame.sprite.Group() #  Карты, которые вывел первый игрок #Cards, which brought the first player
ccards_2 = pygame.sprite.Group() # Карты, которые вывел второй игрок #Cards, which brought the second player
magic_cards = pygame.sprite.Group() #Использующаяся магия #Magic Cards
cards_of_element_shower_element = "" #какой элемент показывать #Any element to show
selected_card = False #Выбранная карта #Selected Card
card_info_group = pygame.sprite.Group() #  Группа, которая содержит спрайт, содержащий панель вывода информации о карте
# The group, which contains a sprite that contains the panel displaying information about the card
font = pygame.font.Font("misc/Domestic_Manners.ttf", 15)
#print pygame.font.match_font('Arial')
screen = None
player = None
player1 = None
player2 = None
#Каст с выбором цели #Cast with the choice of target
cast_focus = False #включен ли режим # if the computer
cast_focus_wizard = None # ссылка на кастующий объект ( не цель ! ) # reference to the caster object (not a goal!)
#cast_focus_filter = None
information_group = pygame.sprite.Group() #Группа, содержащая панель вывода игровой информации # Group containing panel display game information
animations_running = []
