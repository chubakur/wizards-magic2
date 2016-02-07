# -*- coding: utf-8 -*-
# Wizards Magic
# Copyright (C) 2016 Sandro Bonazzola <sandro.bonazzola@gmail.com>
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


import pygame.sprite
import pygame

import os
import gettext
from options import read_configuration
import wzglobals

import air_cards_deck
import death_cards_deck
import earth_cards_deck
import fire_cards_deck
import life_cards_deck
import water_cards_deck

current_folder = os.path.dirname(os.path.abspath(__file__))
__author__ = "chubakur"
__date__ = "$13.02.2011 18:46:32$"


LANGDIR = os.path.join(current_folder, 'languages')

try:
    t = gettext.translation(
        'cards', LANGDIR, languages=[wzglobals.language]
    )
except AttributeError:
    read_configuration()
    t = gettext.translation(
        'cards', LANGDIR, languages=[wzglobals.language]
    )
try:
    # Python 2
    _ = t.ugettext
except AttributeError:
    # Python 3
    _ = t.gettext
t.install()


pygame.font.init()
font = pygame.font.Font(None, 25)


class CastLabel(pygame.sprite.Sprite):

    def __init__(self):
        self.cast_active = pygame.image.load(
            os.path.join(
                current_folder, 'misc', 'card_cast_logo_active.png'
            )
        ).convert_alpha()
        self.cast_disabled = pygame.image.load(
            os.path.join(
                current_folder, 'misc', 'card_cast_logo_disabled.png'
            )
        ).convert_alpha()

links_to_cards = {}
for deck in (
    air_cards_deck,
    death_cards_deck,
    earth_cards_deck,
    fire_cards_deck,
    life_cards_deck,
    water_cards_deck,
):
    for cardname in deck.cards:
        class_to_load = deck.__name__ + '.' + cardname
        links_to_cards[cardname] = eval(class_to_load)
