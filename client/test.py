# -*- coding: utf-8 -*-
import sys

import pgcontrols
import pygame
from pygame.locals import *
import pygame.sprite
screen = pygame.display.set_mode((800, 600))
background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill((0, 0, 0))
#pgcontrols_gr = pygame.sprite.Group()
#pgcontrols.init(pg_controls_gr)
pygame.display.set_caption('test')
def btn1_action():
    print 'bye'
    sys.exit(0)
class Point(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('misc/point_alpha.gif').convert_alpha()
        self.rect = pygame.Rect
    def draw(self, rect):
        background.blit(self.image, rect)
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(rect)
point = Point()
clock = pygame.time.Clock()
label = pgcontrols.Label(background, (0,0),'It`s LABEL!')
label2 = pgcontrols.Label(background, (0,label.get_size()[1]),'Second Label')
box = pgcontrols.Box(background,(100,100),[label,label2])
#label.set_label('Fuck!')
btn1 = pgcontrols.Button(background, (0, 0), btn1_action, 'QUIT')
def btn2_action():
    if btn1.shown:
        btn1.hide()
    else:
        btn1.show()
btn2 = pgcontrols.Button(background, (100, 0), btn2_action, 'SQ')
a = 0
def switch_language():
    global a
    if not a:
        label.set_color((255,255,255))
        btn1.set_label('EXIT')
        btn2.set_label('PSV')
        btn3.set_label('US')
        btn3.set_color((255, 0, 0))
        a = 1
    else:
        label.set_color((25,25,0))
        btn1.set_label('QUIT')
        btn2.set_label('SQ')
        btn3.set_label('RU')
        btn3.set_color((0, 255, 0))
        a = 0
btn3 = pgcontrols.Button(background, (200, 0), switch_language, 'RU')
btn3.set_color((0, 255, 0))
def show_hide_label():
    if label.shown:
        label.hide()
    else:
        label.show()
btn4 = pgcontrols.Button(background, (300,0), show_hide_label, 'LABEL')
while 1:
    for event in pygame.event.get():
        if event.type == QUIT:
            sys.exit(0)
        elif event.type == MOUSEBUTTONDOWN:
            point.draw(event.pos)
            collided = pygame.sprite.spritecollide(point, pgcontrols.group, 0)
            if collided:
                item = collided[-1]
                if item.type == "pgcontrols":
                    pgcontrols.event_handler(event,item)
        elif event.type == MOUSEBUTTONUP:
            point.draw(event.pos)
            collided = pygame.sprite.spritecollide(point, pgcontrols.group, 0)
            if collided:
                item = collided[-1]
                if item.type == "pgcontrols":
                    pgcontrols.event_handler(event,item)
        pgcontrols.group.update()
        screen.blit(background, (0, 0))
        background.fill((0, 0, 0))
        pygame.display.flip()
        #clock.tick(100)
