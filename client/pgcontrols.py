#PGControls
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

import pygame
import pygame.sprite
from pygame.locals import *
pygame.font.init()
font = pygame.font.Font("misc/Domestic_Manners.ttf", 10)
font2 = pygame.font.Font('misc/Domestic_Manners.ttf', 30)
group = pygame.sprite.Group()
def event_handler(event,item):
    if event.type == MOUSEBUTTONDOWN:
        if item.pgcontrols_type == "button":
            item.press()
    elif event.type == MOUSEBUTTONUP:
        if item.pgcontrols_type == "button":
            item.pull()
class Button(pygame.sprite.Sprite):
    def __init__(self, parent, rect, func, label, group_u=False):
        pygame.sprite.Sprite.__init__(self)
        self.font = font
        self.type = "pgcontrols"
        self.pgcontrols_type = "button"
        self.button_image = pygame.image.load('misc/pgcontrols/button.png')
        self.button_pressed_image = pygame.image.load('misc/pgcontrols/button_pressed.png')
        self.button_image_backup = self.button_image.copy()
        self.button_pressed_image_backup = self.button_pressed_image.copy()
        self.rect = self.button_image.get_rect().move(rect)
        self.parent = parent
        self.func = func
        self.pressed = 0
        self.label_text = label
        self.color = (255, 255, 255)
        self.render_label(label)
        self.impose_label()
        self.box = None
        if not group_u:
            self.group = group
        else:
            self.group = group_u
        self.group.add(self)
        self.shown = True
    def get_size(self):
        return self.button_image.get_size()
    def hide(self):
        if self.shown:
            self.shown = False
            self.group.remove(self)
        else:
            return
    def show(self):
        if not self.shown:
            self.shown = True
            self.group.add(self)
        else:
            return
    def press(self):
        self.pressed = 1
    def pull(self):
        self.pressed = 0
        self.func()
    def impose_label(self):
        self.button_image = self.button_image_backup.copy()
        self.button_pressed_image = self.button_pressed_image_backup.copy()
        self.button_image.blit(self.label, (self.button_image.get_size()[0] / 2-self.label.get_size()[0] / 2, self.button_image.get_size()[1] / 2-self.label.get_size()[1] / 2))
        self.button_pressed_image.blit(self.label, (self.button_image.get_size()[0] / 2-self.label.get_size()[0] / 2, self.button_image.get_size()[1] / 2-self.label.get_size()[1] / 2))
        #self.button_image_backup = self.button_image.copy()
        #self.button_pressed_image_backup = self.button_pressed_image.copy()
    def set_label(self, label):
        #self.label = label
        #self.button_image = self.button_image_backup.copy()
        #self.button_pressed_image = self.button_pressed_image_backup.copy()
        self.label_text = label
        self.render_label(label)
        self.impose_label()
    def render_label(self, label):
        self.label = self.font.render(label, True, self.color)
    def set_color(self, color):
        self.color = color
        self.render_label(self.label_text)
        self.impose_label()
    def draw(self):
        if not self.pressed:
            self.parent.blit(self.button_image, self.rect)
        else:
            self.parent.blit(self.button_pressed_image, self.rect)
    def update(self):
        self.draw()
class Label(pygame.sprite.Sprite):
    def __init__(self, parent, rect, label, group_u=False):
        pygame.sprite.Sprite.__init__(self)
        self.font = font2
        self.parent = parent
        self.color = (255, 255, 255)
        self.label_text = label
        self.type = "pgcontrols"
        self.pgcontrols_type = "label"
        #self.label = self.font.render(label, True, self.color)
        self.render_label()
        self.rect = self.label.get_rect().move(rect)
        self.shown = True
        self.box = None
        self.move = False
        if not group_u:
            self.group = group
        else:
            self.group = group_u
        self.group.add(self)
    def get_size(self):
        return self.label.get_size()
    def render_label(self):
        self.label = self.font.render(self.label_text, True, self.color)
    def set_color(self, color):
        self.color = color
        self.render_label()
    def set_label(self, label):
        self.label_text = label
        self.render_label()
    def show(self):
        if not self.shown:
            self.shown = True
            self.group.add(self)
        else:
            return
    def hide(self):
        if self.shown:
            self.shown = False
            self.group.remove(self)
        else:
            return
    def draw(self):
        self.parent.blit(self.label, self.rect)
    def update(self):
        self.draw()
class Box(pygame.sprite.Sprite):
    def __init__(self, parent, rect, elements, group_u = False):
        pygame.sprite.Sprite.__init__(self)
        self.parent = parent
        self.x_size = 0
        self.y_size = 0
        self.type = "pgcontrols"
        self.pgcontrols_type = "box"
        for element in elements:
            el_size = element.get_size()
            if el_size[0]>self.x_size:
                self.x_size = el_size[0]
            self.y_size += el_size[1]
            #element.parent = self
        self.x_size+=20
        self.box_image = pygame.Surface((self.x_size,self.y_size)).convert()
        self.box_image.fill((0,0,255))
        self.box_image_backup = self.box_image.copy()
        self.rect = self.box_image.get_rect().move(rect)
        if not group_u:
            self.group = group
        else:
            self.group = group_u
        self.group.add(self)
        for element in elements:
            element.group.remove(element)
            element.parent = self.box_image
            element.group.add(element)
            #element.parent = self.box_image
        print self.x_size,self.y_size
    def draw(self):
        #self.box_image = self.box_image_backup.copy()
        #self.box_image = self.box_image_backup.copy()
        self.parent.blit(self.box_image,self.rect)
    def update(self):
        self.draw()