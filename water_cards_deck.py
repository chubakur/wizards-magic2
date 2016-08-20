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

import player
import wzglobals


from base import Magic
from base import Prototype


def _(m):
    return gettext.dgettext(message=m, domain='wizards-magic')

cards = [
    "AcidStorm",
    "Hydra",
    "IceBolt",
    "IceGuard",
    "IceWizard",
    "Leviathan",
    "Nixie",
    "Paralyze",
    "Poison",
    "Poseidon",
    "SeaJustice",
    "Waterfall",
]


class AcidStorm(Magic):
    def __init__(self):
        self.element = "water"
        self.name = "AcidStorm"
        self.level = 9
        self.imagefile = 'acid_storm.gif'
        self.info = _(
            "Each creature suffers up to 16 points of damage. "
            "If a player has Poseidon on a field, "
            "his creatures left unaffected. "
            "Amazingly poisonous magic storm, "
            "has no mercy to both friends and foes."
        )
        Magic.__init__(self)

    def cast(self):
        Magic.cast(self)
        s_cards = self.get_self_cards()
        s_cards_immune = False
        e_cards = self.get_enemy_cards()
        e_cards_immune = False
        cards = []
        for card in s_cards:
            if card.name == "Poseidon":
                s_cards_immune = True
            else:
                continue
        if not s_cards_immune:
            cards += s_cards
        for card in e_cards:
            if card.name == "Poseidon":
                e_cards_immune = True
            else:
                continue
        if not e_cards_immune:
            cards += e_cards
        for card in cards:
            card.damage(16, self, True)
        # предварительный перевод
        # каждое существо на поле получает 16 повреждения.
        # Если игрок(какой ? ) имеет посейдона на поле,
        # то его карты остаются нетронутыми.


class Hydra(Prototype):
    def __init__(self):
        self.name = "Hydra"
        self.element = "water"
        self.level = 13
        self.power = 5
        self.cast = True
        self.focus_cast = True
        self.health = 29
        self.info = _(
            "Attacks both adjacent slots. Reduces owner`s Water by 2 "
            "every turn. \n"
            "CAST: Consumes friendly unit, receiving up "
            "to 50% of his health."
        )
        self.imagefile = 'hydra.gif'
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
                wzglobals.cardboxes[adjacent_position].card.damage(
                    self.power, self
                )
            self.run_attack_animation()
        else:
            return

    def turn(self):
        Prototype.turn(self)
        self.parent.player.mana['water'] -= 2
        if self.parent.player.mana['water'] < 0:
            self.parent.player.mana['water'] = 0

    def cast_action(self):
        Prototype.cast_action(self)
        for card in self.get_self_cards():
            if card != self:
                card.light_switch(True)

    def focus_cast_action(self, target):
        if target.name != 'player':  # if card exist
            if target.parent.player.id == self.parent.player.id:
                hp = target.health
                target.die()
                self.heal(int(ceil(hp / 2.0)), self.max_health)
            else:
                return
        else:
            return


class IceBolt(Magic):
    def __init__(self):
        self.element = "water"
        self.name = "IceBolt"
        self.level = 7
        self.imagefile = 'ice_bolt.gif'
        self.info = _(
            "Inflicts 10 + Water/2 damage to enemy player. "
            "Caster suffers 6 damage as a side effect. "
            "Large bolt of Ice, fired at a great speed. "
            "Superior efficiency"
        )
        Magic.__init__(self)

    def cast(self):
        Magic.cast(self)
        self.player.enemy.damage(
            10 + (self.player.mana['water'] + self.level) / 2, self, True
        )
        self.player.damage(6, self, True)
        self.player.mana['water'] = 0
        # наносится урон 10+Water/2 вражескому игроку .
        # Игроку, кто кастовал урон 6.


class IceGuard(Prototype):
    def __init__(self):
        self.name = "IceGuard"
        self.element = "water"
        self.level = 5
        self.info = _(
            "Reduces all damage done to owner by 50%. "
            "Suffers 200% damage from fire."
        )
        self.power = 4
        self.cast = False
        self.health = 19
        self.imagefile = 'ice_guard.gif'
        Prototype.__init__(self)

    def ai(self, type='summon', enemy=None):
        if type == 'summon':
            eff = 0
            if wzglobals.player.mana[self.element] >= self.level:
                eff = wzglobals.player.mana[self.element]/float(self.level)
                if enemy.name != 'player':
                    if enemy.element == 'fire':
                        eff = 0.01
            return eff
        elif type == 'cast':
            return 0

    def damage(self, damage, enemy, cast=False):
        if enemy.element == "fire":
            Prototype.damage(self, damage*2, enemy, cast)
        else:
            Prototype.damage(self, damage, enemy, cast)

    def owner_gets_damage(self, damage):
        self.parent.player.heal(damage/2)


class IceWizard(Prototype):
    def __init__(self):
        self.name = "IceWizard"
        self.element = "water"
        self.level = 10
        self.info = _(
            "Increases Water by 2 every turn. Suffers 200% damage "
            "from fire. All damage from Water equal to 1. \n"
            "CAST: Casting Healing Water heals owner equal to "
            "2*Water points. Owner loses all Water."
        )
        self.power = 4
        self.cast = True
        self.health = 22
        self.imagefile = 'ice_wizard.gif'
        Prototype.__init__(self)

    def ai(self, type='summon', enemy=None):
        if type == 'summon':
            eff = 0
            if wzglobals.player.mana[self.element] >= self.level:
                eff = wzglobals.player.mana[self.element]/float(self.level)
                if enemy.name != 'player':
                    if enemy.element == 'fire':
                        eff = 0.01
            return eff
        elif type == 'cast':
            return 0

    def turn(self):
        Prototype.turn(self)
        self.parent.player.mana['water'] += 2

    def damage(self, damage, enemy, cast=False):
        if enemy.element == 'fire':
            Prototype.damage(self, damage * 2, enemy)
        elif enemy.element == 'water':
            Prototype.damage(self, 1, enemy)
        else:
            Prototype.damage(self, damage, enemy)

    def cast_action(self):
        water = self.parent.player.mana['water']
        self.parent.player.mana['water'] = 0
        self.parent.player.heal(water * 2)


class Leviathan(Prototype):
    def __init__(self):
        self.name = "Leviathan"
        self.element = "water"
        self.level = 11
        self.power = 6
        self.cast = True
        self.health = 37
        self.imagefile = 'leviathan.gif'
        self.info = _(
            "When attacking, each enemy creature suffers 1 damage "
            "in addition to standard attack. \n"
            "Casting Curing heals owner for 4. "
            "In exchange, owner loses 1 Water. "
            "Cannot be cast if owner's Water less than 6."
        )
        Prototype.__init__(self)

    def attack(self):
        Prototype.attack(self)
        for card in self.get_enemy_cards():
            card.damage(1, self, False)

    def cast_action(self):
        if self.parent.player.mana['water'] >= 6:
            self.play_cast_sound()
            self.parent.player.mana -= 1
            self.parent.player.heal(4)
            self.used_cast = True


class Nixie(Prototype):

    def __init__(self):
        self.name = "Nixie"
        self.element = "water"
        self.level = 4
        self.power = 3
        self.health = 10
        self.cast = True
        self.imagefile = 'nixie.gif'
        self.info = _(
            "Causes 200% of damage to fire creatures. "
            "Gives owner 1 Water in the beginning of owner's turn. \n"
            "Casting Sea of Sacred increases owner's Water by 1 and "
            "reduces Fire by 1."
        )
        Prototype.__init__(self)

    def ai(self, type='summon', enemy=None):
        if type == 'summon':
            eff = 0
            if wzglobals.player.mana[self.element] >= self.level:
                eff = wzglobals.player.mana[self.element] / float(
                    self.level
                )
                if enemy.name != 'player':
                    if enemy.element == 'fire':
                        eff += 2
            return eff
        elif type == 'cast':
            return 0

    def attack(self):
        if self.moves_alive:
            attack_position = self.get_attack_position()
            if wzglobals.cardboxes[attack_position].card.name != "player":
                # если есть карта
                if wzglobals.cardboxes[
                    attack_position
                ].card.element == "fire":
                    # если стихия карты - огонь
                    wzglobals.cardboxes[attack_position].card.damage(
                        self.power * 2, self
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

    def cast_action(self):
        self.play_cast_sound()
        if self.parent.player.mana['fire']:
            self.parent.player.mana['fire'] -= 1
            self.parent.player.mana['water'] += 1
            self.used_cast = True

    def turn(self):
        self.parent.player.mana['water'] += 1


class Paralyze(Magic):
    def __init__(self):
        self.element = "water"
        self.name = "Paralyze"
        self.level = 10
        self.imagefile = 'paralyze.gif'
        self.info = _(
            "Paralyzes enemy player and creatures for one turn, "
            "so they skip one turn."
        )
        Magic.__init__(self)
        # противник пропускает ход

    def cast(self):
        Magic.cast(self)
        self.nt = False
        wzglobals.magic_cards.add(self)  # добавляем периодизацию

    def periodical_cast(self):
        self.kill()
        # player.switch_position()
        player.finish_turn()


class Poison(Magic):
    def __init__(self):
        self.element = "water"
        self.name = "Poison"
        self.level = 3
        self.imagefile = 'poison.gif'
        self.info = _(
            "Poisons all enemy units so that they lose health every turn, "
            "also hits them with 1 damage. "
            "Posion doesn`t affect undead."
        )
        Magic.__init__(self)
        # Каждый ход отнимает у карты противника по 1 здоровью.
        # Не действует на класс смерти

    def cast(self):
        Magic.cast(self)
        self.cards = self.get_enemy_cards()
        # берем "слепок" вражеских карт, которые будем травить
        for card in self.cards:
            if card.element != "death":
                card.spells.append(self)
                # говорим карте чтобы она начала креститься
                card.damage(1, self, True)
        wzglobals.magic_cards.add(self)  # добавляем периодизацию

    def periodical_cast(self):
        if self.cards:
            # если еще остались карты, на которые надо действовать
            if self.player.id != wzglobals.player.id:
                # если начался вражеский ход
                for card in self.cards:
                    card.damage(1, self, True)  # раним карту
        else:  # если кпд магии будет 0
            self.kill()  # прекращаем действие магии
        # P.S. неувязочка в алгоритме таки.
        # Карта выкидывается из группы, только если карта её убьет.
        # Если карту убьет другая карта,
        # то эта карта останется в памяти магии ,
        # что заставит её работать с КПД 0
        # Возможное решение: {{Вроде FIXED}}
        # Прописать в прототип боевой карты массив,
        # в котором будут храниться спеллы, наложенные на карту.
        # После своей смерти, карта разошлет магическим обработчикам
        # сообщения о своей смерти и они смогут очиститься.


class Poseidon(Prototype):
    def __init__(self):
        self.name = "Poseidon"
        self.element = "water"
        self.level = 8
        self.power = 3
        self.info = _(
            "Every time anyone casts Water spell or summons Water "
            "creature, opponent suffers 4 damage and owner gains 2 health."
        )
        self.cast = False
        self.health = 25
        self.imagefile = 'poseidon.gif'
        Prototype.__init__(self)

    def spell_used(self, spell):
        if spell.element == "water":
            self.parent.player.enemy.damage(4, self)
            self.parent.player.heal(2)

    def card_summoned(self, card):
        if card.element == "water":
            self.parent.player.enemy.damage(4, self)
            self.parent.player.heal(2)


class SeaJustice(Magic):
    def __init__(self):
        self.element = "water"
        self.name = "SeaJustice"
        self.level = 3
        self.info = _(
            "Every enemy creature suffers damage equal to its attack -1"
        )
        self.imagefile = 'sea_justice.gif'
        Magic.__init__(self)
        # Атакует каждую карту противника с силой равной силе карты-1

    def cast(self):
        # работает единожды, поэтому нет нужды добавлять в группу и
        # создавать ф-ию периодического каста.
        Magic.cast(self)
        enemy_cards = self.get_enemy_cards()  # берем список вражеских карт
        for card in enemy_cards:
            card.damage(card.power - 1, self, True)

    def ai(self, type='summon', enemy=None):
        eff = Magic.ai(self)
        if not eff:
            return eff
        for enemy in self.get_enemy_cards():
            if (
                (enemy.health <= enemy.damage - 1) or
                (
                    wzglobals.cardboxes[
                        enemy.get_attack_position()
                    ].card.name != player and
                    enemy.health - enemy.power + 1 <= wzglobals.cardboxes[
                        enemy.get_attack_position()
                    ].card.power
                )
            ):
                eff += 1


class Waterfall(Prototype):
    def __init__(self):
        self.name = "Waterfall"
        self.element = "water"
        self.level = 9
        self.power = 1
        self.cast = False
        self.health = 33
        self.imagefile = 'waterfall.gif'
        self.info = _(
            "One of the toughest Elementals. "
            "Health itself for 3 whenever any player casts water "
            "spell of summons water creature. "
            "Attack equal to owner`s Water."
        )
        Prototype.__init__(self)

    def turn(self):
        Prototype.turn(self)
        self.power = self.parent.player.mana['water']
        if not self.power:
            self.power = 1
