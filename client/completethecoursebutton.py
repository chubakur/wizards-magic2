# -*- coding: utf-8 -*-
import pygame
import globals
class CompleteTheCourseButton(pygame.sprite.Sprite):
    def __init__(self, rect, panel):
        pygame.sprite.Sprite.__init__(self)
        self.panel = panel
        self.type = 'completethecoursebutton'
        self.player = panel.player
        self.image = pygame.image.load('misc/complete_the_course.gif').convert_alpha()
        self.relative_rect = self.image.get_rect().move((rect[0], rect[1]))
        self.rect = self.relative_rect.move(self.panel.rect[0], self.panel.rect[1])
        globals.interface.add(self)
    def draw(self):
        if not self.player.id == globals.player.id:
            return
        self.panel.image.blit(self.image, self.relative_rect)
    def update(self):
        self.draw()