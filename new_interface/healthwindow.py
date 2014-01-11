# -*- coding: utf-8 -*-
import pygame
import globals
class HealthWindow(pygame.sprite.Sprite):
    def __init__(self, rect):
        pygame.sprite.Sprite.__init__(self)
        self.type = 'healthwindow'
        globals.interface.add(self)
        self.font = pygame.font.Font(None, 22)
        text = self.font.render('1', True, (1,1,1))
        self.rect = text.get_rect().move(rect)
    def draw(self):
        #cb3b3a
        if not globals.cli:
            text = self.font.render(str(globals.player.health), True, (203, 59, 58))
        else:
            if globals.player_id == 1:
                text = self.font.render(str(globals.player1.health), True, (203, 59, 58))
            else:
                text = self.font.render(str(globals.player2.health), True, (203, 59, 58))
        globals.background.blit(text, self.rect)
    def update(self):
        self.draw()
class HealthWindowEnemy(pygame.sprite.Sprite):
    def __init__(self, rect):
        pygame.sprite.Sprite.__init__(self)
        self.type = 'healthwindow'
        globals.interface.add(self)
        self.font = pygame.font.Font(None, 22)
        text = self.font.render('1', True, (1,1,1))
        self.rect = text.get_rect().move(rect)
    def draw(self):
        #cb3b3a
        if not globals.cli:
            text = self.font.render(str(globals.player.enemy.health), True, (203, 59, 58))
        else:
            if globals.player_id == 1:
                text = self.font.render(str(globals.player2.health), True, (203, 59, 58))
            else:
                text = self.font.render(str(globals.player1.health), True, (203, 59, 58))
        globals.background.blit(text, self.rect)
    def update(self):
        self.draw()