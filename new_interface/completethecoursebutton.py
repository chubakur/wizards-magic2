# -*- coding: utf-8 -*-
import pygame
import os
import globals
import player
current_folder = os.path.dirname(os.path.abspath(__file__))

class CompleteTheCourseButton(pygame.sprite.Sprite):
    def __init__(self, rect):
        pygame.sprite.Sprite.__init__(self)
        #self.panel = panel
        self.type = 'button'
        self.image = pygame.image.load(current_folder+'/misc/complete_the_course.gif').convert_alpha()
        self.relative_rect = self.image.get_rect().move((rect[0], rect[1]))
        self.rect = self.relative_rect #.move(self.panel.rect[0], self.panel.rect[1])
        globals.interface.add(self)
    def onmouse(self):
        return
    def onmouseout(self):
        return
    def onmousedown(self):
        if globals.cli:
            if globals.player_id != globals.player.id:
                return
        for cardbox in globals.cardboxes:
            cardbox.light = False
        player.finish_turn()
    def onmouseup(self):
        return
    def draw(self):
        if globals.cli:
            if globals.player_id != globals.player.id:
                return
        globals.background.blit(self.image, self.relative_rect)
    def update(self):
        self.draw()
