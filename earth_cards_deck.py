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

import wzglobals


from base import AbsoluteDefenceSpirit
from base import Magic
from base import Prototype


def _(m):
    return gettext.dgettext(message=m, domain='wizards-magic')


cards = [
    "AbsoluteDefence",
    "Centaur",
    "Dryad",
    "Earthquake",
    "Echidna",
    "Elemental",
    "Ent",
    "ForestSpirit",
    "Golem",
    "Quicksands",
    "Restructure",
    "Revival",
    "Satyr",
]


class AbsoluteDefence(Magic):
    def __init__(self):
        self.element = "earth"
        self.name = "AbsoluteDefence"
        self.level = 7
        self.imagefile = 'absolute_defence.gif'
        self.info = _(
            "Owner's creatures gain protection from all attacks. "
            "This defence only lasts one turn and lasts till next "
            "owner's turn. "
            "It's just like an unpenetrable wall has suddenly appeared. "
            "Anyone under your command will survive anything!"
        )
        Magic.__init__(self)

    def cast(self):
        Magic.cast(self)
        self.protected_cards = {}
        for cardbox in self.get_self_cardboxes():
            if cardbox.card.name != "player":  # if card exists
                self.protected_cards[cardbox.position] = cardbox.card
                cardbox.card = AbsoluteDefenceSpirit(cardbox.card)
        wzglobals.magic_cards.add(self)

    def periodical_cast(self):
        if self.player.id == wzglobals.player.id:
            for cardboxid in self.protected_cards:
                wzglobals.cardboxes[cardboxid].card = \
                    self.protected_cards[cardboxid]
            self.kill()


class Centaur(Prototype):
    def __init__(self):
        self.name = "Centaur"
        self.element = "earth"
        self.level = 6
        self.info = _(
            "Attacks the same turn he was summoned(No summon sickness). "
            "\nCAST: Strikes magic arrow into enemy player, "
            "dealing 3 damage. Costs 1 Earth."
        )
        self.power = 5
        self.cast = True
        self.health = 14
        self.imagefile = 'centaur.gif'
        Prototype.__init__(self)
        self.moves_alive = 1

    def cast_action(self):
        if self.parent.player.mana['earth']:
            self.play_cast_sound()
            self.parent.player.enemy.damage(3, self, True)
            self.parent.player.mana['earth'] -= 1
            self.used_cast = True


class Dryad(Prototype):
    def __init__(self):
        self.name = "Dryad"
        self.element = "earth"
        self.level = 4
        self.power = 4
        self.cast = False
        self.health = 12
        self.info = _(
            "Adjacent owner creatures attack increases by 1, "
            "and if it`s Earth creature, by 2 whenever anyone casts "
            "Earth spell or summons Earth creature."
        )
        self.imagefile = 'dryad.gif'
        Prototype.__init__(self)

    def additional_turn_action(self):
        ids = self.get_adjacent_position()
        if ids:
            for id in ids:
                wzglobals.cardboxes[id].card.set_power(
                    wzglobals.cardboxes[id].card.power + 1
                )

    def summon(self):
        Prototype.summon(self)
        self.additional_turn_action()


class Earthquake(Magic):
    def __init__(self):
        self.element = "earth"
        self.name = "Earthquake"
        self.level = 10
        self.imagefile = 'earthquake.gif'
        self.info = _(
            "Hits each creature for 15 damage. "
            "Doesn't affect owner's creatures, if onwer's Earth > 12. "
            "Even the earth itself is a powerful weapon."
        )
        Magic.__init__(self)

    def cast(self):
        Magic.cast(self)
        earth_mana = self.player.mana['earth'] + self.level
        if earth_mana > 12:
            cards = self.get_enemy_cards()
        else:
            cards = self.get_enemy_cards() + self.get_self_cards()
        for card in cards:
            card.damage(15, self, True)


class Echidna(Prototype):
    def __init__(self):
        self.name = "Echidna"
        self.element = "earth"
        self.level = 10
        self.power = 7
        self.cast = False
        self.health = 26
        self.info = _(
            "When attacks, poisons her target. "
            "This target will lose 2 health every turn. "
            "In the beginning og owner`s turn, "
            "Echidna hits all poisoned creatures for 1."
        )
        self.imagefile = 'echidna.gif'
        Prototype.__init__(self)


class Elemental(Prototype):
    def __init__(self):
        self.name = "Elemental"
        self.element = "earth"
        self.level = 13
        self.power = 1
        self.cast = False
        self.info = _(
            "Attack equal to owner`s Earth. Increases Earth by 2 "
            "every turn. Fire spells deal additional 10 damage. \n"
            "CAST: Casts Stone Skin onto owner`s creature. "
            "That creature gain 1 point of defence from all attacks "
            "greater than 1.")
        self.health = 45
        self.imagefile = 'elemental.gif'
        Prototype.__init__(self)

    def summon(self):
        Prototype.summon(self)
        self.set_power(self.parent.player.mana[self.element] - self.level)

    def turn(self):
        Prototype.turn(self)
        self.parent.player.mana['earth'] += 2
        self.set_power(self.parent.player.mana[self.element])


class Ent(Prototype):
    def __init__(self):
        self.name = "Ent"
        self.element = "earth"
        self.level = 7
        self.power = 3
        self.info = _(
            "Attacks opposed unit and enemy player at the same time. \n"
            "Casts Entangle Roots, damaging each enemy unit for 1 "
            "and losing 2 points of own health."
        )
        self.cast = True
        self.health = 22
        self.imagefile = 'ent.gif'
        Prototype.__init__(self)

    def attack(self):
        if self.moves_alive:
            e_card = wzglobals.cardboxes[self.get_attack_position()].card
            Prototype.attack(self)
            if e_card.name != 'player':
                self.parent.player.enemy.damage(self.power, self, True)
        e_card = None

    def cast_action(self):
        for card in self.get_enemy_cards():
            card.damage(1, self, True)
        self.used_cast = True
        self.damage(2, self, True)
        self.play_cast_sound()


class ForestSpirit(Prototype):
    def __init__(self):
        self.name = "ForestSpirit"
        self.element = "earth"
        self.level = 3
        self.info = _(
            "Damage from all non-magical attacks and abilities equal to 1."
            " \nCAST: Casts Youth of Forest, increasing owner "
            "player`s health by 5. Costs two Earth elements."
        )
        self.power = 2
        self.cast = True
        self.health = 3
        self.imagefile = 'forest_spirit.gif'
        Prototype.__init__(self)

    def damage(self, damage, enemy, cast=False):
        if not cast:
            Prototype.damage(self, 1, enemy, cast)
        else:
            Prototype.damage(self, damage, enemy, cast)

    def cast_action(self):
        if self.parent.player.mana['earth'] >= 2:
            self.parent.player.mana['earth'] -= 2
            self.used_cast = True
            self.play_cast_sound()
            self.parent.player.heal(5)


class Golem(Prototype):
    def __init__(self):
        self.name = "Golem"
        self.element = "earth"
        self.level = 5
        self.power = 4
        self.cast = False
        self.health = 15
        self.info = _(
            "Regenerates 3 health every turn. "
            "While owner's Earth less than 3, it suffers 3 damage instead."
        )
        self.imagefile = 'golem.gif'
        Prototype.__init__(self)

    def turn(self):
        Prototype.turn(self)
        if self.parent.player.mana['earth'] < 3:
            self.damage(3, self)
        else:
            self.heal(3, self.max_health)


class Quicksands(Magic):
    def __init__(self):
        self.element = "earth"
        self.name = "Quicksands"
        self.level = 6
        self.imagefile = 'quicksands.gif'
        self.info = _(
            "Kills all enemy creatures of level less than 5. "
            "Only the skilled one can survive the swamp's most "
            "dangerous weapon."
        )
        Magic.__init__(self)

    def cast(self):
        Magic.cast(self)
        for card in self.get_enemy_cards():
            if card.level < 5:
                card.die()
            else:
                continue


class Restructure(Magic):
    def __init__(self):
        self.element = "earth"
        self.name = "Restructure"
        self.level = 6
        self.imagefile = 'restructure.gif'
        self.info = _(
            "All onwer's creatures gain +3 health to their maximum, "
            "healing for 6 in the same time. "
            "Scatter to pieces, connect once again. "
            "Now you are stronger, none shall remain!"
        )
        Magic.__init__(self)

    def cast(self):
        Magic.cast(self)
        for card in self.get_self_cards():
            card.max_health += 3
            card.heal(6, card.max_health)


class Revival(Magic):
    def __init__(self):
        self.element = "earth"
        self.name = "Revival"
        self.level = 5
        self.imagefile = 'revival.gif'
        self.info = _(
            "Heals all friendly creatures for 4. "
            "Gives owner 2 health for each of his creatures on a field. "
            "Heal me! Heal me!"
        )
        Magic.__init__(self)

    def cast(self):
        Magic.cast(self)
        for card in self.get_self_cards():
            card.heal(4, card.max_health)
            self.player.heal(2)


class Satyr(Prototype):
    def __init__(self):
        self.name = "Satyr"
        self.element = "earth"
        self.level = 2
        self.power = 3
        self.cast = True
        self.info = _(
            "Increases Earth by 1 every turn. \n"
            "CAST: Once Satyr casts Dissolve, it dies and creature in "
            "the opposed slot suffers 5 damage. "
            "If there`s no creature, damage dealt to enemy player."
        )
        self.health = 10
        self.imagefile = 'satyr.gif'
        Prototype.__init__(self)

    def turn(self):
        Prototype.turn(self)
        self.parent.player.mana['earth'] += 1

    def cast_action(self):
        self.play_cast_sound()
        attack_position = self.get_attack_position()
        wzglobals.cardboxes[attack_position].card.damage(5, self, True)
        self.die()
