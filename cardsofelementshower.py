# -*- coding: utf-8 -*-
# Wizards Magic
# Copyright (C) 2011-2014  https://code.google.com/p/wizards-magic/
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.


import wzglobals
import pygame


class CardsOfElementShower(pygame.sprite.Sprite):
    # Не прототип!
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.type = 'cardsofelementshower'
        self.cards = 0
        self.shift = 2

    def draw(self):
        pass

    def update(self):
        wzglobals.cards_in_deck.empty()
        if wzglobals.cli:
            if wzglobals.player_id != wzglobals.player.id:
                return
        if not wzglobals.cli or wzglobals.player.cards_generated:
            for card in wzglobals.player.cards[
                wzglobals.cards_of_element_shower_element
            ]:
                wzglobals.cards_in_deck.add(
                    wzglobals.player.cards[
                        wzglobals.cards_of_element_shower_element
                    ][card]
                )
