# -*- coding: utf-8 -*-
import pygame
import globals
class HealthWindow(pygame.sprite.Sprite):
    def __init__(self, rect, panel):
        pygame.sprite.Sprite.__init__(self)
        self.panel = panel
        self.type = 'healthwindow'
        self.player = panel.player
        self.image = pygame.image.load('misc/health_window.gif').convert_alpha()
        self.surface_backup = self.image.copy()
        self.relative_rect = self.image.get_rect().move((rect[0], rect[1]))
        self.rect = self.relative_rect.move(self.panel.rect[0], self.panel.rect[1])
        globals.interface.add(self)
        self.font = pygame.font.Font(None, 22)
    def draw(self):
        self.image = self.surface_backup.copy()
        if self.player.id == 1:
            text = self.font.render(str(globals.player1.health), True, (255, 255, 255))
        else:
            text = self.font.render(str(globals.player2.health), True, (255, 255, 255))
        self.image.blit(text, (25, 5))
        self.panel.image.blit(self.image, self.relative_rect)
    def update(self):
        self.draw()