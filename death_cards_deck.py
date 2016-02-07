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

import gettext
from math import ceil
from math import floor

from base import Magic
from base import Prototype

import wzglobals


def _(m):
    return gettext.dgettext(message=m, domain='wizards-magic')


cards = [
    "ChaosVortex",
    "CoverOfDarkness",
    "Curse",
    "Banshee",
    "Darklord",
    "Ghost",
    "GrimReaper",
    "Lich",
    "StealLife",
    "TotalWeakness",
    "Vampire",
    "Werewolf",
    "Zombie",
]


class ChaosVortex(Magic):
    def __init__(self):
        self.element = "death"
        self.name = "ChaosVortex"
        self.level = 13
        self.imagefile = 'chaos_vortex.gif'
        self.info = _(
            "Banishes each creature into hell. "
            "Each banished creature gives caster 1 Death. "
            "Whenever one unfolds Chaos, no mortal can stand its "
            "fearful ugly nature."
        )
        Magic.__init__(self)

    def cast(self):
        Magic.cast(self)
        cards = self.get_enemy_cards() + self.get_self_cards()
        self.player.mana['death'] += len(cards)
        for card in cards:
            card.die()


class CoverOfDarkness(Magic):
    def __init__(self):
        self.element = "death"
        self.name = "CoverOfDarkness"
        self.level = 11
        self.imagefile = 'cover_of_darkness.gif'
        self.info = _(
            "All living creatures suffer 13 damage. "
            "All undead creatures heal for 5. "
            "The Lord of Chaos most useful tool. "
            "Your army of darkness shall reign forever."
        )
        Magic.__init__(self)

    def cast(self):
        Magic.cast(self)
        cards = self.get_enemy_cards() + self.get_self_cards()
        for card in cards:
            if card.element == "death":
                card.heal(5, card.max_health)
            else:
                card.damage(13, self, True)


class Curse(Magic):
    def __init__(self):
        self.element = "death"
        self.name = "Curse"
        self.level = 4
        self.imagefile = 'curse.gif'
        self.info = _(
            "Reduces all enemy elements by 1. "
            "Curse and Doom are now your enemy's only guests."
        )
        Magic.__init__(self)

    def cast(self):
        Magic.cast(self)
        if wzglobals.player.enemy.mana['water']:
            wzglobals.player.enemy.mana['water'] -= 1
        if wzglobals.player.enemy.mana['fire']:
            wzglobals.player.enemy.mana['fire'] -= 1
        if wzglobals.player.enemy.mana['air']:
            wzglobals.player.enemy.mana['air'] -= 1
        if wzglobals.player.enemy.mana['earth']:
            wzglobals.player.enemy.mana['earth'] -= 1
        if wzglobals.player.enemy.mana['life']:
            wzglobals.player.enemy.mana['life'] -= 1
        if wzglobals.player.enemy.mana['death']:
            wzglobals.player.enemy.mana['death'] -= 1


class Banshee(Prototype):
    def __init__(self):
        self.name = "Banshee"
        self.element = "death"
        self.info = _(
            "When summoned, deals 8 damage to enemy. "
            "Once it attacks enemy player, dies and enemy player suffers "
            "10 points of extra damage. "
            "If Banshee dies from other creature or spell, "
            "enemy player doesn't suffer."
        )
        self.level = 7
        self.cast = False
        self.power = 5
        self.health = 12
        self.imagefile = 'banshee.gif'
        Prototype.__init__(self)

    def attack(self):
        if self.moves_alive:
            if wzglobals.cardboxes[
                self.get_attack_position()
            ].card.name == "player":
                self.run_attack_animation()
                wzglobals.cardboxes[
                    self.get_attack_position()
                ].card.damage(self.power + 10, self)
                self.die()
            else:
                Prototype.attack(self)

    def summon(self):
        Prototype.summon(self)
        self.parent.player.enemy.damage(8, self)


class Darklord(Prototype):
    def __init__(self):
        self.name = "Darklord"
        self.element = "death"
        self.info = _(
            "Whenever creature dies, Darklord heals owner for 3 and "
            "regenerates self for 2. \n"
            "Steal Spell steals all spell effects from any enemy "
            "creature, DarkLord receives these spells. "
            "Owner loses 1 Death."
        )
        self.level = 8
        self.power = 4
        self.cast = False
        self.health = 14
        self.imagefile = 'darklord.gif'
        Prototype.__init__(self)

    def card_died(self, card):
        self.heal(2, self.max_health)
        self.parent.player.heal(3)


class Ghost(Prototype):
    def __init__(self):
        self.name = "Ghost"
        self.element = "death"
        self.info = _(
            "Whenever attacked by a creature, suffers 50% less damage, "
            "and owner suffers other 50% damage. "
            "When suffers from spell, Ghost recieves 200% of "
            "normal damage. \n"
            "Casts Bloody Ritual. "
            "As a result, owner loses 5 health, but receives one Death."
        )
        self.level = 3
        self.cast = True
        self.power = 3
        self.health = 13
        self.imagefile = 'ghost.gif'
        Prototype.__init__(self)

    def damage(self, damage, enemy, cast=False):
        if not cast:
            Prototype.damage(self, int(ceil(damage / floor(2))), enemy)
            self.parent.player.damage(int(ceil(damage / floor(2))), enemy)
        else:
            Prototype.damage(self, damage * 2, enemy, True)

    def cast_action(self):
        self.parent.player.mana['death'] += 1
        self.parent.player.health -= 5
        self.used_cast = True
        self.play_cast_sound()


class GrimReaper(Prototype):
    def __init__(self):
        self.name = "GrimReaper"
        self.info = _(
            "Whenever creature dies, increases owner`s Death by one. \n"
            "CAST: Consumes target enemy creature of level 3 or less. "
            "Owner player loses 3 Death elements."
        )
        self.element = "death"
        self.level = 12
        self.power = 8
        self.cast = True
        self.focus_cast = True
        self.health = 22
        self.imagefile = 'grim_reaper.gif'
        Prototype.__init__(self)

    def cast_action(self):
        if self.parent.player.mana['death'] >= 3:
            Prototype.cast_action(self)
            for card in self.get_enemy_cards():
                if card.level <= 3:
                    card.light_switch(True)

    def focus_cast_action(self, target):
        if target.name != 'player':  # if it is real card!
            if self.parent.player.id != target.parent.player.id:
                self.play_cast_sound()
                self.parent.player.mana['death'] -= 3
                target.die()
                self.used_cast = True
                wzglobals.cast_focus = False
                for card in self.get_enemy_cards():
                    card.light_switch(False)
        else:
            return


class Lich(Prototype):
    def __init__(self):
        self.name = "Lich"
        self.element = "death"
        self.level = 10
        self.info = _(
            "When summoned,deals 10 damage to creature in the opposite "
            "slot and two adjacent slots. "
            "Attacks Life units with additionial 5 damage. \n"
            "CAST:Casts Death Bolt, hitting enemy player with 7 of damage."
            " Owner loses 5 Death. "
            "If owner`s Death becomes zero, he suffers 10 damage himself."
        )
        self.cast = False
        self.power = 7
        self.health = 18
        self.imagefile = 'lich.gif'
        Prototype.__init__(self)

    def summon(self):
        Prototype.summon(self)
        attack_position = self.get_attack_position()
        wzglobals.cardboxes[attack_position].card.damage(10, self)
        for adjacent_pos in self.get_attack_adjacent_position(
            attack_position
        ):
            wzglobals.cardboxes[adjacent_pos].card.damage(10, self)

    def attack(self):
        if self.moves_alive:
            attack_position = self.get_attack_position()
            if wzglobals.cardboxes[attack_position].card.name != 'player':
                if wzglobals.cardboxes[
                    attack_position
                ].card.element == "life":
                    wzglobals.cardboxes[attack_position].card.damage(
                        self.power + 5, self
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
        else:
            return


class StealLife(Magic):
    def __init__(self):
        self.element = "death"
        self.name = "StealLife"
        self.level = 6
        self.imagefile = 'steal_life.gif'
        self.info = _(
            "If owner's Death less than 8, steals 5 health from enemy "
            "player. Otherwise steals Death + 5. Death's cold vampiric "
            "touch. So painful and surreal.."
        )
        Magic.__init__(self)

    def cast(self):
        Magic.cast(self)
        death_mana = wzglobals.player.mana['death'] + self.level
        if death_mana < 8:
            wzglobals.player.enemy.damage(5, self, True)
            wzglobals.player.heal(5)
        else:
            wzglobals.player.enemy.damage(death_mana + 5, self, True)
            wzglobals.player.heal(death_mana + 5)


class TotalWeakness(Magic):

    def __init__(self):
        self.element = "death"
        self.name = "TotalWeakness"
        self.level = 8
        self.imagefile = 'total_weakness.gif'
        self.info = _(
            "Every enemy creature suffers effect of Weakness: its attack "
            "decreased by 50% (rounded down). Make the strongest the "
            "weakest, and then assasinate him."
        )
        Magic.__init__(self)

    def cast(self):
        Magic.cast(self)
        cards = self.get_enemy_cards()
        for card in cards:
            card.default_power = int(floor(card.power / 2.0))
            card.set_power(int(floor(card.power / 2.0)))


class Vampire(Prototype):
    def __init__(self):
        self.name = "Vampire"
        self.element = "death"
        self.level = 9
        self.power = 6
        self.health = 22
        self.cast = False
        self.info = _(
            "When attacks living creature, restores health equal to "
            "50% of damage dealt. Maximum 30 health."
        )
        self.imagefile = 'vampire.gif'
        Prototype.__init__(self)

    def attack(self):
        if self.moves_alive:
            attack_position = self.get_attack_position()
            if wzglobals.cardboxes[attack_position].card.name != "player":
                if wzglobals.cardboxes[
                    attack_position
                ].card.element != "death":
                    self.heal(int(ceil(float(self.power / 2.0))), 30)
            wzglobals.cardboxes[attack_position].card.damage(
                self.power, self
            )
            self.run_attack_animation()


class Werewolf(Prototype):
    def __init__(self):
        self.name = "Werewolf"
        self.cast = True
        self.element = "death"
        self.level = 6
        self.power = 6
        self.info = _(
            "When dies, becomes a ghost. \n"
            "CAST: Casts Blood Rage on self. "
            "Strikes twice as hard this turn, "
            "but owner loses 3 Death points on casting."
        )
        self.health = 16
        self.imagefile = 'werewolf.gif'
        Prototype.__init__(self)

    def die(self):
        card = Ghost()
        card.parent = self.parent
        card.field = True
        self.parent.card = card
        self.kill()
        for card in self.get_enemy_cards() + self.get_self_cards():
            card.card_died(self)
        if self.parent.player.id == 1:
            wzglobals.ccards_1.add(self.parent.card)
        else:
            wzglobals.ccards_2.add(self.parent.card)
        card.update()

    def cast_action(self):
        if self.parent.player.mana['death'] >= 3:
            self.used_cast = True
            self.parent.player.mana['death'] -= 3
            self.power *= 2


class Zombie(Prototype):
    def __init__(self):
        self.name = "Zombie"
        self.element = "death"
        self.level = 4
        self.power = 3
        self.health = 11
        self.info = _(
            "Eats enemies corpses - every time if kills enemy creature, "
            "totally health and his health increases by 3."
        )
        self.cast = False
        self.imagefile = 'zombie.gif'
        Prototype.__init__(self)

    def enemy_die(self):
        self.max_health += 3
        self.health = self.max_health
        self.update()
