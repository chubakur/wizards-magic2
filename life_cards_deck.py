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


from base import Magic
from base import Prototype


def _(m):
    return gettext.dgettext(message=m, domain='wizards-magic')

cards = [
    "Apostate",
    "Bless",
    "Chimera",
    "GodsWrath",
    "LifeSacrifice",
    "MagicHealer",
    "Paladin",
    "Pegasus",
    "Priest",
    "Purify",
    "Rejuvenation",
    "Unicorn",
]


class Apostate(Prototype):
    def __init__(self):
        self.name = "Apostate"
        self.element = "life"
        self.level = 5
        self.info = _(
            "Steals 2 owner's Life and gives owner 1 Death in the "
            "beginning of owner's turn. \n"
            "Serves Death. Once cast, Apostate permanently turns into "
            "a Banshee. Banshee restores only 1/2 of normal health."
        )
        self.cast = True
        self.power = 4
        self.health = 14
        self.imagefile = 'apostate.gif'
        Prototype.__init__(self)

    def turn(self):
        Prototype.turn(self)
        if self.parent.player.mana['life'] >= 2:
            self.parent.player.mana['life'] -= 2
        else:
            self.parent.player.mana['life'] = 0
        self.parent.player.mana['death'] += 1

    def ai(self, type='summon', enemy=None):
        if type == 'summon':
            eff = 0
            if wzglobals.player.mana[self.element] >= self.level:
                eff = wzglobals.player.mana[self.element]/float(self.level)
            return eff
        elif type == 'cast':
            if (
                enemy.power >= self.health and
                enemy.moves_alive
            ):
                self.cast_action()

    def cast_action(self):
        from death_cards_deck import Banshee
        card = Banshee()
        card.parent = self.parent
        card.field = True
        card.health = card.health / 2
        self.parent.card = card
        self.kill()
        if self.parent.player.id == 1:
            wzglobals.ccards_1.add(self.parent.card)
        else:
            wzglobals.ccards_2.add(self.parent.card)


class Bless(Magic):  # TODO: restore of health
    def __init__(self):
        self.element = "life"
        self.name = "Bless"
        self.level = 5
        self.imagefile = 'bless.gif'
        self.info = _(
            "All owner's creatures Blessed: "
            "receive +1 to attack, restore 1 point of health every "
            "time they are hit. "
            "Undead creatures cannot be blessed and suffer 10 "
            "damage instead. "
            "Your army's now under God's protection, "
            "and your enemy is doomed forever!"
        )
        Magic.__init__(self)

    def cast(self):
        Magic.cast(self)
        cards = self.get_self_cards()
        for card in cards:
            if card.element != 'death':
                card.set_power(card.power + 1)
                self.cards.append(card)
            else:
                card.damage(10, self, True)
        wzglobals.magic_cards.add(self)

    def periodical_cast(self):
        if self.cards:  # if has cards
            if self.player.id != wzglobals.player.id:
                # if enemy turn started
                for card in self.cards:
                    card.heal(1, card.max_health)
        else:
            self.kill()


class Chimera(Prototype):
    def __init__(self):
        self.name = "Chimera"
        self.element = "life"
        self.info = _(
            "When Chimera is on a field, every spell casting costs "
            "50% less for the owner. "
            "Whenever you summon creature, you gain health equal to "
            "this creature's level."
        )
        self.level = 11
        self.power = 11
        self.cast = False
        self.health = 30
        self.imagefile = 'chimera.gif'
        Prototype.__init__(self)

    def card_summoned(self, card):
        if self.parent.player.id == card.parent.player.id:
            # if it`s my card
            if card != self:
                self.parent.player.heal(card.level)


class GodsWrath(Magic):
    def __init__(self):
        self.element = "life"
        self.name = "GodsWrath"
        self.level = 10
        self.imagefile = 'gods_wrath.gif'
        self.info = _(
            "All undead on a field are destroyed. "
            "Owner receives 3 Life and 1 health for each "
            "destroyed creature. "
            "The great day of The Lord is near and coming quickly. "
            "That day will be a day of Wrath, "
            "a day of distress and anguish."
        )
        Magic.__init__(self)

    def cast(self):
        Magic.cast(self)
        cards = self.get_enemy_cards() + self.get_self_cards()
        for card in cards:
            if card.element == "death":
                card.die()
                self.player.mana['life'] += 3
                self.player.heal(1)


class LifeSacrifice(Magic):
    def __init__(self):
        self.element = "life"
        self.name = "LifeSacrifice"
        self.level = 8
        self.imagefile = 'life_sacrifice.gif'
        self.info = _(
            "Owner loses health equal to his Life. "
            "Enemy suffers damage, double of this amount. "
            "Sacrificing is the true loving act."
        )
        Magic.__init__(self)

    def cast(self):
        Magic.cast(self)
        power = self.player.mana['life'] + self.level
        # mana['life'] - count of Life ;
        # level - cast this spell, because mana decreased before
        # spell activated.
        self.player.damage(power, self, True)
        self.player.enemy.damage(power * 2, self, True)


class MagicHealer(Prototype):
    def __init__(self):
        self.name = "MagicHealer"
        self.info = _(
            "Whenever owner player loses health, "
            "Magic Healer health player by this amount, "
            "losing hit points equally."
        )
        self.element = "life"
        self.level = 3
        self.power = 2
        self.cast = False
        self.health = 10
        self.security_slots = []
        self.imagefile = 'magic_healer.gif'
        Prototype.__init__(self)

    def owner_gets_damage(self, damage):
        self.parent.player.heal(damage)
        self.damage(damage, self)


class Paladin(Prototype):
    def __init__(self):
        self.name = "Paladin"
        self.element = "life"
        self.info = _(
            "Brings 300% of damage to undead creatures. \n"
            "CAST: Casts Exorcism. "
            "Destroys any undead, but suffers 10 damage himself. "
            "Owner also loses 2 Life as a cost of this holy casting."
        )
        self.cast = True
        self.focus_cast = True
        self.level = 8
        # self.level = 1
        self.power = 4
        self.health = 20
        self.imagefile = 'paladin.gif'
        Prototype.__init__(self)

    def ai(self, type='summon', enemy=None):
        if type == 'summon':
            eff = 0
            if wzglobals.player.mana[self.element] >= self.level:
                eff = \
                    wzglobals.player.mana[self.element] / float(self.level)
                if enemy.name != 'player':
                    if enemy.element == 'death':
                        eff += 2
            return eff
        elif type == 'cast':
            return 0

    def cast_action(self):
        if self.parent.player.mana['life'] >= 2:
            # если хватает маны, то активируем фокус
            Prototype.cast_action(self)
            for card in self.get_enemy_cards():
                if card.element == "death":
                    card.light_switch(True)

    def focus_cast_action(self, target):
        if target.name != "player":  # если это реальная карта
            if target.parent.player.id != self.parent.player.id:
                # если это чужая карта
                if target.element == "death":
                    # действие
                    self.used_cast = True
                    wzglobals.cast_focus = False
                    target.die()
                    self.damage(10, self, True)
                    self.parent.player.mana['life'] -= 2
                    self.play_cast_sound()
                    for card in self.get_enemy_cards():
                        # отключаем подсветку
                        card.light_switch(False)
                else:
                    # Если паладин не может подействовать на эту карту
                    return
            else:
                return  # если своя карта
        else:
            return  # если тут вообще нет карты


class Pegasus(Prototype):
    def __init__(self):
        self.name = "Pegasus"
        self.element = "life"
        self.level = 6
        self.power = 6
        self.health = 15
        self.info = _(
            "When summoned, each owner`s creature is healed for 3. "
            "Also, it destroys harmful spell effects from each of them. \n"
            "CAST: Holy Strike deals 5 damage to a target creature. "
            "If it is undead creature, "
            "Pegasus also suffer 3 damage homself. "
            "Costs 2 Life."
        )
        self.cast = True
        self.focus_cast = True
        self.imagefile = 'pegasus.gif'
        Prototype.__init__(self)

    def summon(self):
        Prototype.summon(self)
        for card in self.get_self_cards():
            card.heal(3, card.max_health)

    def cast_action(self):
        if self.parent.player.mana['life'] >= 2:  # если хватает маны
            Prototype.cast_action(self)  # включаем фокус-каст
            for card in self.get_enemy_cards():  # включаем подсветку
                card.light_switch(True)

    def focus_cast_action(self, target):
        if target.name != "player":
            # если мы кликнули по карте, а не пустому боксу
            if target.parent.player.id != self.parent.player.id:
                # если карта чужая( Убивать своих не хорошо)
                if target.element == "death":  # если стихия карты - смерть
                    target.damage(5, self, True)  # наносим урон ей
                    self.damage(3, self, True)  # и себе
                else:  # если любой другой стихии
                    target.damage(5, self, True)  # наносим урон ей
                self.used_cast = True
                # отмечаем, что заклинание уже использовано
                wzglobals.cast_focus = False  # отключаем фокус-каст
                self.parent.player.mana['life'] -= 2  # отнимаем ману
                self.play_cast_sound()  # играем звук
                for card in self.get_enemy_cards():  # отключаем подсветку
                    card.light_switch(False)
            else:
                return
        else:
            return


class Priest(Prototype):
    def __init__(self):
        self.name = "Priest"
        self.element = "life"
        self.level = 4
        self.cast = False
        self.power = 1
        self.health = 9
        self.info = _(
            "Increases owner`s Life by 1 every turn, "
            "decreasing Death by the same amount. "
            "Decreases owner`s Life by 3 every time owner "
            "casts Death spells."
        )
        self.imagefile = 'priest.gif'
        Prototype.__init__(self)

    def turn(self):
        Prototype.turn(self)
        if self.parent.player.mana['death']:
            self.parent.player.mana['death'] -= 1
            self.parent.player.mana['life'] += 1

    def spell_used(self, spell):
        if spell.element == 'death' and spell.player is self.parent.player:
            self.parent.player.mana['life'] -= 3
            if self.parent.player.mana['life'] < 0:
                self.parent.player.mana['life'] = 0


class Purify(Magic):
    def __init__(self):
        self.element = "life"
        self.name = "Purify"
        self.level = 7
        self.imagefile = 'purify.gif'
        self.info = _(
            "If owner has Life creatures in play, "
            "heals owner for 5 and steals 4 health from each enemy "
            "creature, giving them to opposed owner's creature. "
            "Only pure souls can use God's blessings."
        )
        Magic.__init__(self)

    def cast(self):
        Magic.cast(self)
        has_life = False
        for card in self.get_self_cards():
            if card.element == 'life':
                has_life = True
        if has_life:
            self.player.heal(5)
            for e_card in self.get_enemy_cards():
                opp_card = wzglobals.cardboxes[
                    e_card.get_attack_position()
                ].card
                if opp_card.name != 'player':
                    # if card in opposed slot exist
                    e_card.damage(4, self, True)
                    opp_card.heal(4, opp_card.max_health)
                else:
                    e_card.damage(4, self, True)
        else:
            return


class Rejuvenation(Magic):
    def __init__(self):
        self.element = "life"
        self.name = "Rejuvenation"
        self.level = 6
        self.imagefile = 'rejuvenation.gif'
        self.info = _(
            "Heals owner equal to his Life*3. "
            "Owner loses all Life elements. "
            "Blessed creatures heal for 3. "
            "Now you live again, mortal. "
            "Life is the most precious, be careful next time!"
        )
        Magic.__init__(self)

    def cast(self):
        Magic.cast(self)
        life_mana = wzglobals.player.mana['life'] + self.level
        wzglobals.player.heal(life_mana * 3)
        for card in self.get_self_cards():
            card.heal(3, card.max_health)
        wzglobals.player.mana['life'] = 0


class Unicorn(Prototype):
    def __init__(self):
        self.name = "Unicorn"
        self.element = "life"
        self.level = 9
        self.power = 8
        self.cast = False
        self.info = _(
            "Unicorn reduces damage from spells to owner's creatures "
            "by 50%. Cures poison from owner's creatures. \n"
            "Casts Unicorn Aura. "
            "This Aura destroys useful spell effects from enemy creatures."
            " Costs 2 Life."
        )
        self.health = 25
        self.imagefile = 'unicorn.gif'
        Prototype.__init__(self)
