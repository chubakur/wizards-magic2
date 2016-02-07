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

import gettext

import pygame

from base import Magic
from base import Prototype

import wzglobals


def _(m):
    return gettext.dgettext(message=m, domain='wizards-magic')


cards = [
    "BlackWind",
    "ChainLightning",
    "Fairy",
    "Gargoyle",
    "Manticore",
    "Nymph",
    "Phoenix",
    "Plague",
    "Spellbreaker",
    "Titan",
    "Zeus",
]


class BlackWind(Magic):
    def __init__(self):
        self.element = "air"
        self.name = "BlackWind"
        self.level = 8
        self.image = pygame.image.load(
            wzglobals.current_folder + '/misc/cards/air/black_wind.gif'
        )
        self.info = _(
            "Winds away strongest enemy creature. "
            "Perfect against high-level enemy creatures. "
            "One of the most useful spells."
        )
        Magic.__init__(self)

    def cast(self):
        Magic.cast(self)
        max = 0
        link_to_max = False
        for card in self.get_enemy_cards():
            if card.level > max:
                max = card.level
                link_to_max = card
            else:
                continue
        if link_to_max:
            link_to_max.die()


class ChainLightning(Magic):
    def __init__(self):
        self.element = "air"
        self.name = "ChainLightning"
        self.level = 9
        self.image = pygame.image.load(
            wzglobals.current_folder + '/misc/cards/air/chain_lightning.gif'
        )
        self.info = _(
            "First enemy creature suffers damage equal to owner's Air+2. "
            "Lightning travels forth and hits each enemy creature, losing "
            "2 damage each time it hits. "
            "For example, if owner has 10 Air and enemy has all 5 "
            "creatures, they suffer this damage (left to right): "
            "12-10-8-6-4"
        )
        Magic.__init__(self)

    def cast(self):
        Magic.cast(self)
        air_mana = self.player.mana['air'] + self.level
        power = air_mana + 2
        for card in self.get_enemy_cards():
            card.damage(power, self, True)
            power -= 2


class Fairy(Prototype):
    def __init__(self):
        self.name = "Fairy"
        self.element = "air"
        self.info = _(
            "Increases its attack by 1 for each creature, killed on "
            "a field. \n"
            "CAST: Enslave Mind forces strongest enemy creature "
            "to attack it`s owner. Costs 1 Air."
        )
        self.level = 3
        self.power = 3
        self.cast = True
        self.health = 7
        self.image = pygame.image.load(
            wzglobals.current_folder + '/misc/cards/air/fairy.gif'
        )
        Prototype.__init__(self)

    def turn(self):
        self.default_power = 3 + self.killed
        Prototype.turn(self)

    def enemy_die(self):
        Prototype.enemy_die(self)
        self.default_power = 3 + self.killed
        self.power = self.default_power
        self.update()

    def cast_action(self):
        if self.parent.player.mana['air']:
            self.used_cast = True
            self.parent.player.mana['air'] -= 1
            self.play_cast_sound()
            max = 0
            max_link = False
            for card in self.get_enemy_cards():
                if card.power > max:
                    max = card.power
                    max_link = card
            if max_link:
                self.parent.player.enemy.damage(
                    max_link.power, max_link, True
                )
        # Атака увеличивается на 1 за каждого убитого
        # КАСТ. Сильнейшая карта врага атакует своего героя. 1 воздух.


class Gargoyle(Prototype):
    def __init__(self):
        self.name = "Gargoyle"
        self.element = "air"
        self.info = _(
            "Suffers no damage from Earth and Air spells. \n"
            "CAST: Casts Petrification on self, as effect turns to stone. "
            "In stone form Gargoyle reduces damage done to it by 2 . "
            "Owner loses 3 Air and 1 Earth."
        )
        self.level = 5
        self.power = 4
        self.cast = True
        self.health = 15
        self.image = pygame.image.load(
            wzglobals.current_folder + '/misc/cards/air/gargoyle.gif'
        )
        self.stone = False
        Prototype.__init__(self)

    def attack(self):
        if self.stone:
            return
        else:
            Prototype.attack(self)

    def damage(self, damage, enemy, cast=False):
        if self.stone:
            if damage - 2 > 0:
                Prototype.damage(self, damage - 2, enemy)
            else:
                Prototype.damage(self, 0, enemy)
        else:
            Prototype.damage(self, damage, enemy)

    def cast_action(self):
        if (
            self.parent.player.mana['air'] >= 3 and
            self.parent.player.mana['earth']
        ):
            self.play_cast_sound()
            self.parent.player.mana['air'] -= 3
            self.parent.player.mana['earth'] -= 1
            self.used_cast = True
            self.stone = True

    def turn(self):
        Prototype.turn(self)
        self.stone = False


class Manticore(Prototype):
    def __init__(self):
        self.name = "Manticore"
        self.element = "air"
        self.info = _(
            "Attacks casters with additional 3 damage. "
            "Only suffers 50% damage from spells. \n"
            "CAST: Casts Memory Loss. "
            "Target enemy creature permanently loses ability to cast. "
            "Costs 2 Air."
        )
        self.level = 7
        self.power = 5
        self.cast = True
        self.focus_cast = True
        self.health = 19
        self.image = pygame.image.load(
            wzglobals.current_folder + '/misc/cards/air/manticore.gif'
        )
        Prototype.__init__(self)

    def attack(self):
        if self.moves_alive:
            attack_position = self.get_attack_position()
            if wzglobals.cardboxes[attack_position].card.name != 'player':
                # if card exist
                if wzglobals.cardboxes[attack_position].card.cast:
                    wzglobals.cardboxes[attack_position].card.damage(
                        self.power + 3, self
                    )
                else:
                    wzglobals.cardboxes[attack_position].card.damage(
                        self.power, self
                    )
            else:
                wzglobals.cardboxes[attack_position].card.damage(
                    self.power, self
                )
            self.run_attack_animation()

    def cast_action(self):
        if self.parent.player.mana['air'] >= 2:
            # if player have mana for cast
            Prototype.cast_action(self)  # activating focus-cast
            for card in self.get_enemy_cards():
                if card.cast:  # if it`s caster
                    card.light_switch(True)  # enable lighting

    def focus_cast_action(self, target):
        if target.name != 'player':  # if it is real card
            if target.parent.player.id != self.parent.player.id:
                # if it is enemy`s card
                if target.cast:  # if it is caster
                    target.cast = False  # target now can`t cast
                    self.used_cast = True
                    # This means, that this card cast already
                    wzglobals.cast_focus = False  # focus-cast off
                    self.parent.player.mana['air'] -= 2
                    # decrease player`s mana.
                    # It is payment for this action.
                    self.play_cast_sound()  # play cast sound
                    for card in self.get_enemy_cards():  # disable lighting
                        card.light_switch(False)
                else:
                    return
            else:
                return
        else:
            return


class Nymph(Prototype):
    def __init__(self):
        self.name = "Nymph"
        self.element = "air"
        self.level = 3
        self.power = 1
        self.cast = False
        self.info = _(
            "Owner receives 1 Air at the beginning of Owners turn."
        )
        self.health = 12
        self.image = pygame.image.load(
            wzglobals.current_folder + '/misc/cards/air/nymph.gif'
        )
        Prototype.__init__(self)

    def turn(self):
        Prototype.turn(self)
        self.parent.player.mana['air'] += 1
        # Каждый ход владелец получает дополнительно 1 воздух


class Phoenix(Prototype):
    def __init__(self):
        self.name = "Phoenix"
        self.element = "air"
        self.info = _(
            "If Phoenix was killed by Fire spell or creature, "
            "rebirth with full health."
        )
        self.level = 6
        self.power = 4
        self.cast = False
        self.health = 20
        self.recovered = 0  # Восстанавливалась ли карта
        self.image = pygame.image.load(
            wzglobals.current_folder+'/misc/cards/air/phoenix.gif'
        )
        Prototype.__init__(self)

    def ai(self, type='summon', enemy=None):
        if type == 'summon':
            eff = 0
            if wzglobals.player.mana[self.element] >= self.level:
                eff = wzglobals.player.mana[self.element]/float(self.level)
                if enemy.name != 'player':
                    if enemy.element == 'fire':
                        eff += 2
            return eff
        elif type == 'cast':
            return 0

    def damage(self, damage, enemy, cast=False):
        self.health -= damage
        self.update()
        if self.health <= 0:
            if enemy.element == "fire":  # Если стихия врага - огонь
                if not self.recovered:  # если не восстанавливалась
                    self.health = self.max_health
                    self.recovered = True
                    return 0
                else:
                    self.die()
                    return 1
            else:
                self.die()
                return 1
            return 0
        return 0
        # self.die()


class Plague(Magic):
    def __init__(self):
        self.element = "air"
        self.name = "Plague"
        self.level = 12
        self.image = pygame.image.load(
            wzglobals.current_folder + '/misc/cards/air/plague.gif'
        )
        self.info = _(
            "Every creature on a field plagued - loses all hit "
            "points except one. "
            "Ignores all defences and modifiers. "
            "None shall escape the Plague! "
            "Great lands burnt to dust where the plague passed."
        )
        Magic.__init__(self)

    def cast(self):
        Magic.cast(self)
        cards = self.get_enemy_cards() + self.get_self_cards()
        for card in cards:
            card.set_health(1)


class Spellbreaker(Magic):
    def __init__(self):
        self.element = "air"
        self.name = "Spellbreaker"
        self.level = 7
        self.image = pygame.image.load(
            wzglobals.current_folder + '/misc/cards/air/spellbreaker.gif'
        )
        self.info = _(
            "Owner's creatures become permanently immune to all "
            "damaging spells, spell effects, and poison. "
            "Remember that your creatures can no longer be affected "
            "by Bless, Restructure and other good spell effects."
        )
        Magic.__init__(self)


class Titan(Prototype):
    def __init__(self):
        self.name = "Titan"
        self.element = "air"
        self.level = 11
        self.power = 7
        self.cast = True
        self.info = _(
            "When summoned, enemy loses 3 Air. "
            "Titan`s attack is increased by 1 for each Air creature "
            "in play. \n"
            "CAST: Casts Thunder Fist. "
            "All enemy Earth creatures suffer 3 damage. "
            "Owner loses 1 Air."
        )
        self.health = 28
        self.image = pygame.image.load(
            wzglobals.current_folder + '/misc/cards/air/titan.gif'
        )
        Prototype.__init__(self)

    def summon(self):
        Prototype.summon(self)
        self.parent.player.enemy.mana['air'] -= 3
        if self.parent.player.enemy.mana['air'] < 0:
            self.parent.player.enemy.mana['air'] = 0

    def cast_action(self):
        self.play_cast_sound()
        if self.parent.player.mana['air']:
            self.parent.player.mana['air'] -= 1
            for enemy_card in self.get_enemy_cards():
                if enemy_card.element == "earth":
                    enemy_card.damage(3, self, True)


class Zeus(Prototype):
    def __init__(self):
        self.name = "Zeus"
        self.element = "air"
        self.level = 9
        self.power = 3
        self.cast = False
        self.health = 24
        self.info = _(
            "Owner receives 1 air element for each enemy creature, "
            "killed by Zeus. \n"
            "CAST: Strikes Lighting into choosen creature. "
            "Costs 1 Air and inflicts 8 damage. "
            "Cannot strike creatures of level 7 and highter."
        )
        self.image = pygame.image.load(
            wzglobals.current_folder + '/misc/cards/air/zeus.gif'
        )
        Prototype.__init__(self)

    def attack(self):
        if self.moves_alive:
            attack_position = self.get_attack_position()
            kill = wzglobals.cardboxes[attack_position].card.damage(
                self.power, self
            )
            if kill:
                self.parent.player.mana['air'] += 1
        else:
            return
