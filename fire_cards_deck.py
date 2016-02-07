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
from math import ceil
from math import floor

import pygame

from base import Magic
from base import Prototype

import wzglobals


def _(m):
    return gettext.dgettext(message=m, domain='wizards-magic')


cards = [
    "Armageddon",
    "Cerberus",
    "Demon",
    "Devil",
    "Efreet",
    "Firelord",
    "Fireball",
    "FireSpikes",
    "FlamingArrow",
    "RedDrake",
    "RitualFlame",
    "Salamander",
    "Vulcan",
]


class Armageddon(Magic):
    def __init__(self):
        self.element = "fire"
        self.name = "Armageddon"
        self.level = 11
        self.image = pygame.image.load(
            wzglobals.current_folder + '/misc/cards/fire/armageddon.gif'
        )
        self.info = _(
            "All units on a field suffer 25 damage. "
            "Each player suffers 25 damage. "
            "The ultimate spell of the game. "
            "The strongest and most harmful. "
            "Beware, it's far too powerful!"
        )
        Magic.__init__(self)

    def cast(self):
        Magic.cast(self)
        enemy_cards = self.get_enemy_cards()
        self_cards = self.get_self_cards()
        for card in enemy_cards + self_cards:
            card.damage(25, self, True)
        self.player.damage(25, self, True)
        self.player.enemy.damage(25, self, True)


class Cerberus(Prototype):
    def __init__(self):
        self.name = "Cerberus"
        self.element = "fire"
        self.level = 4
        self.power = 4
        self.info = _(
            "Attacks adjacent enemy units at a half of it`s strength."
        )
        self.cast = False
        self.health = 6
        self.image = pygame.image.load(
            wzglobals.current_folder + '/misc/cards/fire/cerberus.gif'
        )
        Prototype.__init__(self)

    def attack(self):
        if self.moves_alive:
            attack_position = self.get_attack_position()
            wzglobals.cardboxes[attack_position].card.damage(
                self.power, self
            )
            adjacent_positions = self.get_attack_adjacent_position(
                attack_position
            )
            for adjacent_position in adjacent_positions:
                if not wzglobals.cardboxes[
                    adjacent_position
                ].card.power / 2:
                    wzglobals.cardboxes[adjacent_position].card.damage(
                        1, self
                    )
                else:
                    wzglobals.cardboxes[adjacent_position].card.damage(
                        int(
                            ceil(
                                float(
                                    wzglobals.cardboxes[
                                        adjacent_position
                                    ].card.power
                                ) / 2
                            )
                        ), self
                    )
            self.run_attack_animation()
        else:
            return


class Demon(Prototype):
    def __init__(self):
        self.name = "Demon"
        self.element = "fire"
        self.level = 5
        self.power = 2
        self.info = _(
            "Doesn`t suffer from Fire and Earth spells. \n"
            "CAST: Whenever Demon casts Fire Bleed owner loses 1 "
            "Earth and receives 2 Fire elements."
        )
        self.cast = True
        self.health = 12
        self.image = pygame.image.load(
            wzglobals.current_folder + '/misc/cards/fire/demon.gif'
        )
        Prototype.__init__(self)

    def cast_action(self):
        if self.parent.player.mana['earth']:
            self.parent.player.mana['earth'] -= 1
            self.parent.player.mana['fire'] += 2
            self.play_cast_sound()
            self.used_cast = True
        # Не получает повреждения от заклинаний огня и земли
        # cast: владелец теряет один элемент земли и получает 2 огня


class Devil(Prototype):
    def __init__(self):
        self.name = "Devil"
        self.element = "fire"
        self.info = _(
            "Damage from Water is multiplied by 2. "
            "Whenever Devil dies, owner suffers 10 damage. \n"
            "CAST: Sacrificing owner`s Fire creature gives 3 Fire "
            "to the owner, also healing owner by this amount."
        )
        self.level = 6
        self.power = 4
        self.cast = True
        self.focus_cast = True
        self.health = 27
        self.image = pygame.image.load(
            wzglobals.current_folder + '/misc/cards/fire/devil.gif'
        )
        Prototype.__init__(self)

    def die(self):
        self.parent.player.damage(10, self)
        Prototype.die(self)

    def ai(self, type='summon', enemy=None):
        if type == 'summon':
            eff = 0
            if wzglobals.player.mana[self.element] >= self.level:
                eff = wzglobals.player.mana[self.element]/float(self.level)
                if enemy.name != 'player':
                    if enemy.element == 'water':
                        eff = 0.01
            return eff
        elif type == 'cast':
            return 0

    def damage(self, damage, enemy, cast=False):
        if enemy.element == "water":
            Prototype.damage(self, damage * 2, enemy)
        else:
            Prototype.damage(self, damage, enemy)

    def cast_action(self):
        Prototype.cast_action(self)  # enable focus-cast
        for card in self.get_self_cards():
            if card.element == 'fire' and card != self:
                card.light_switch(True)
            else:
                continue

    def focus_cast_action(self, target):
        if target.name != 'player':  # if it is real card
            if target.parent.player.id == self.parent.player.id:
                # if it is caster`s card
                if target.element == 'fire':
                    if target != self:
                        self.play_cast_sound()
                        self.used_cast = True
                        wzglobals.cast_focus = False
                        self.parent.player.mana['fire'] += 3
                        self.parent.player.heal(target.health)
                        target.die()
                        for card in self.get_self_cards():
                            card.light_switch(False)


class Efreet(Prototype):
    def __init__(self):
        self.name = "Efreet"
        self.element = "fire"
        self.level = 10  # 10
        self.power = 6
        self.cast = False
        self.health = 33
        self.info = _(
            "Whenever any creature attacks Efreet, that creature suffers "
            "half of damage send back (same applies to Fire Shield "
            "spell). Uppon summoning, all enemy Water creatures suffer "
            "6 damage. \n"
            "CAST: Casts Fire Shield on any owner`s creature. "
            "Costs 2 Fire. "
            "Fire Shield burns creature from inside, damaging it for 2 "
            "points per turn, unless it`s a Fire creature."
        )
        self.image = pygame.image.load(
            wzglobals.current_folder + '/misc/cards/fire/efreet.gif'
        )
        Prototype.__init__(self)

    def summon(self):
        Prototype.summon(self)
        for card in self.get_enemy_cards():
            if card.element == "water":
                card.damage(6, self)
            else:
                continue

    def damage(self, damage, enemy, cast=False):
        if not cast:
            Prototype.damage(self, damage, enemy, cast)
            Prototype.damage(enemy, damage / 2, self, cast)
        else:
            Prototype.damage(self, damage, enemy, cast)


class Fireball(Magic):
    def __init__(self):
        self.element = "fire"
        self.name = "Fireball"
        self.level = 8
        self.image = pygame.image.load(
            wzglobals.current_folder + '/misc/cards/fire/fireball.gif'
        )
        self.info = _(
            "Each enemy creature suffers damage equal to owner's "
            "Fire + 3. "
            "As easy as it is - a ball of burning fire."
        )
        Magic.__init__(self)

    def cast(self):
        Magic.cast(self)
        enemy_cards = self.get_enemy_cards()
        for card in enemy_cards:
            card.damage(
                self.player.mana['fire'] + self.level + 3, self, True
            )


class Firelord(Prototype):
    def __init__(self):
        self.name = "Firelord"
        self.element = "fire"
        self.level = 11
        self.power = 7
        self.cast = False
        self.info = _(
            "Opens fire gates. This means that both players should "
            "receive 1 additional Fire every turn. "
            "Upon dying, Firelord brings 8 damage to each player."
        )
        self.health = 21
        self.image = pygame.image.load(
            wzglobals.current_folder + '/misc/cards/fire/firelord.gif'
        )
        Prototype.__init__(self)

    def turn(self):
        Prototype.turn(self)
        self.parent.player.mana['fire'] += 1
        self.parent.player.enemy.mana['fire'] += 1

    def die(self):
        self.parent.player.damage(8, self)
        self.parent.player.enemy.damage(8, self)
        Prototype.die(self)


class FireSpikes(Magic):
    def __init__(self):
        self.element = "fire"
        self.name = "FireSpikes"
        self.level = 3
        self.image = pygame.image.load(
            wzglobals.current_folder + '/misc/cards/fire/fire_spikes.gif'
        )
        self.info = _(
            "Deals 3 damage to each enemy creature. "
            "Cheap and still good. Pure Fire."
        )
        Magic.__init__(self)

    def cast(self):
        Magic.cast(self)
        for card in self.get_enemy_cards():
            card.damage(3, self, True)


class FlamingArrow(Magic):
    def __init__(self):
        self.element = "fire"
        self.name = "FlamingArrow"
        self.level = 4
        self.image = pygame.image.load(
            wzglobals.current_folder + '/misc/cards/fire/flaming_arrow.gif'
        )
        self.info = _(
            "If enemy has less Fire than owner does, enemy suffers "
            "damage, equal to this difference, multiplied by 2. "
            "Otherwise enemy suffers 1 damage. "
            "Now this is a smart one - a magic arrow made of pure Fire, "
            "never misses your foe."
        )
        Magic.__init__(self)

    def cast(self):
        Magic.cast(self)
        diff = (
            self.player.mana['fire'] +
            self.level -
            self.player.enemy.mana['fire']
        )
        if diff > 0:
            self.player.enemy.damage(diff * 2, self, True)
        else:
            self.player.enemy.damage(1, self, True)


class RedDrake(Prototype):
    def __init__(self):
        self.name = "RedDrake"
        self.element = "fire"
        self.level = 7
        self.info = _(
            "When summoned, each enemy creature and enemy player "
            "suffers 3 damage. Red Drake Suffers no damage from "
            "Fire spells and creatures."
        )
        self.power = 5
        self.cast = False
        self.health = 16
        self.image = pygame.image.load(
            wzglobals.current_folder + '/misc/cards/fire/red_drake.gif'
        )
        Prototype.__init__(self)

    def summon(self):
        Prototype.summon(self)
        self.parent.player.enemy.damage(3, self)
        for card in self.get_enemy_cards():
            card.damage(3, self)

    def damage(self, damage, enemy, cast=False):
        if enemy.element == 'fire':
            return
        else:
            Prototype.damage(self, damage, enemy)

    def ai(self, type='summon', enemy=None):
        if type == 'summon':
            eff = 0
            if wzglobals.player.mana[self.element] >= self.level:
                eff = wzglobals.player.mana[self.element]/float(self.level)
                if enemy.element == 'fire':
                    eff += 2
            return eff
        elif type == 'cast':
            return 0


class RitualFlame(Magic):
    def __init__(self):
        self.element = "fire"
        self.name = "RitualFlame"
        self.level = 5
        self.image = pygame.image.load(
            wzglobals.current_folder + '/misc/cards/fire/ritual_flame.gif'
        )
        self.info = _(
            "Destroys all spell effects from all creatures, "
            "both owner's and enemy's. "
            "Heals all Fire creatures for 3."
        )
        Magic.__init__(self)

    def cast(self):
        Magic.cast(self)
        for card in self.get_enemy_cards() + self.get_self_cards():
            for spell in card.spells:
                spell.unset(card)
            card.spells = []
            if card.element == 'fire':
                card.heal(3, card.max_health)


class Salamander(Prototype):
    def __init__(self):
        self.name = "Salamander"
        self.element = "fire"
        self.level = 8
        self.power = 3
        self.cast = False
        self.info = _(
            "Increases attack of all owner's creatures by 2. "
            "Increases damage from owner player's spellcastings by 2."
        )
        self.health = 15
        self.image = pygame.image.load(
            wzglobals.current_folder + '/misc/cards/fire/salamander.gif'
        )
        Prototype.__init__(self)

    def additional_turn_action(self):
        for card in self.get_self_cards():
            # card.default_power += 2
            if card != self:
                card.power = card.power + 2
                card.update()

    def summon(self):
        Prototype.summon(self)
        self.additional_turn_action()


class Vulcan(Prototype):
    def __init__(self):
        self.name = "Vulcan"
        self.element = "fire"
        self.level = 12
        self.power = 1
        self.cast = True
        self.info = _(
            "Fire Elemental. Immune to harmful Fire spells. "
            "When summoned, enemy player loses 3 Fire, and opposed "
            "Elemental unit suffers 9 damage. Attack equal to "
            "owner`s Fire + 3. \n"
            "CAST: Casts Volcano Explode. "
            "Vulcan dies, but every unit on field suffers damage equal "
            "to 50% of Vulcan`s health."
        )
        self.health = 27
        self.image = pygame.image.load(
            wzglobals.current_folder + '/misc/cards/fire/vulcan.gif'
        )
        Prototype.__init__(self)

    def summon(self):
        Prototype.summon(self)
        self.set_power(self.parent.player.mana['fire'] - self.level + 3)
        if self.parent.player.enemy.mana['fire'] >= 3:
            self.parent.player.enemy.mana['fire'] -= 3
        else:
            self.parent.player.enemy.mana['fire'] = 0
        opp_card = wzglobals.cardboxes[self.get_attack_position()].card
        if opp_card.name != 'player':
            opp_card.damage(9, self)

    def turn(self):
        Prototype.turn(self)
        self.set_power(self.parent.player.mana['fire'] + 3)

    def cast_action(self):
        hp = self.health
        for card in self.get_enemy_cards() + self.get_self_cards():
            card.damage(int(floor(hp / 2.0)), self, True)
        self.die()
