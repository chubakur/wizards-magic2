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


import os
import pygame

import animations
import wzglobals

IMAGESDIR = os.path.join(wzglobals.current_folder, 'misc', 'cards')


class Magic(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.type = "magic_card"
        self.magic = True
        self.field = False
        if self.imagefile:
            self.image = pygame.image.load(
                os.path.join(IMAGESDIR, self.element, self.imagefile)
            )
        self.image = self.image.convert_alpha()
        self.surface_backup = self.image.copy()
        self.font = pygame.font.Font(None, 19)
        self.cards = []
        if (
            self.element == "death" or
            self.element == "fire" or
            self.element == "earth" or
            self.element == "water"
        ):
            self.font_color = (255, 255, 255)
        else:
            self.font_color = (0, 0, 0)
        try:
            self.info
        except AttributeError:
            self.info = ""

    def cast(self):
        pygame.mixer.music.load(
            os.path.join(
                wzglobals.current_folder, 'misc', 'sounds', 'card_cast.ogg'
            )
        )
        wzglobals.playmusic()

    def unset(self, card):
        self.cards.remove(card)

    def set(self, card):
        self.cards.append(card)

    def get_self_cardboxes(self):
        cardboxes = []
        if self.player.id == 1:
            for cardbox in wzglobals.cardboxes[0:5]:
                cardboxes.append(cardbox)
        else:
            for cardbox in wzglobals.cardboxes[5:10]:
                cardboxes.append(cardbox)
        return cardboxes

    def get_enemy_cardboxes(self):
        cardboxes = []
        if self.player.id == 1:
            for cardbox in wzglobals.cardboxes[5:10]:
                cardboxes.append(cardbox)
        else:
            for cardbox in wzglobals.cardboxes[0:5]:
                cardboxes.append(cardbox)
        return cardboxes

    def get_enemy_cards(self):
        cards = []
        if self.player.id == 1:
            for cardbox in wzglobals.cardboxes[5:10]:
                if cardbox.card.name != "player":  # если есть карта
                    cards.append(cardbox.card)
        else:
            for cardbox in wzglobals.cardboxes[0:5]:
                if cardbox.card.name != "player":
                    cards.append(cardbox.card)
        return cards

    def get_self_cards(self):
        cards = []
        if self.player.id == 1:
            for cardbox in wzglobals.cardboxes[0:5]:
                if cardbox.card.name != "player":  # если есть карта
                    cards.append(cardbox.card)
        else:
            for cardbox in wzglobals.cardboxes[5:10]:
                if cardbox.card.name != "player":
                    cards.append(cardbox.card)
        return cards

    def spell_speaker(self):
        # This function tell to each card on game field about spell using.
        wzglobals.gameinformationpanel.display(self.name)
        for card in self.get_enemy_cards() + self.get_self_cards():
            card.spell_used(self)

    def periodical_cast(self):
        pass

    def ai(self, type='summon', enemy=None):
        if type == 'summon':
            if wzglobals.player.mana[self.element] >= self.level:
                return (
                    wzglobals.player.mana[self.element] / float(self.level)
                )
            else:
                return 0
        elif type == 'cast':
            return 0

    def update(self):
        # Field - True если рисовать на поле,
        # false - если рисовать в таблице выбора
        text_level = wzglobals.font2.render(
            str(self.level), True, self.font_color
        )
        self.image = self.surface_backup.copy()
        self.image.blit(text_level, (90, -7))
        if not self.field:  # Рисование в колоде
            self.parent = wzglobals.background
            xshift = (
                324 +
                self.position_in_deck * self.image.get_size()[0] +
                wzglobals.cardofelementsshower.shift *
                self.position_in_deck +
                2 * self.position_in_deck
            )
            yshift = 431
            self.parent.blit(self.image, (xshift, yshift))
            self.rect = self.image.get_rect()
            self.rect = self.rect.move(xshift, yshift)
        else:
            self.parent.image.blit(self.image, (0, 0))


# Basic class for the creatures
class Prototype(pygame.sprite.Sprite):

    def __init__(self):
        # image
        if self.imagefile:
            self.image = pygame.image.load(
                os.path.join(IMAGESDIR, self.element, self.imagefile)
            )
        else:
            print("DEBUG: %s has no imagefile" % self.name)
        pygame.sprite.Sprite.__init__(self)
        # cardbox where card is
        self.parent = 0
        self.light = False

        self.image = self.image.convert_alpha()
        self.light_image = pygame.image.load(
            os.path.join(
                wzglobals.current_folder, 'misc', 'light.gif'
            )
        ).convert_alpha()
        self.surface_backup = self.image.copy()
        self.font = pygame.font.Font(None, 19)
        # type of card ( creature or spell )
        self.type = "warrior_card"
        # count of killed creatures by this card
        self.killed = 0
        # array of long term spells
        self.spells = []
        self.default_power = self.power
        # count of turns how cards alive
        self.moves_alive = 0
        self.max_health = self.health
        self.default_power = self.power
        # Boolean. Card in field, on in deck.
        self.field = False
        # True if card has cast action
        self.used_cast = False
        if (
            self.element == "death" or
            self.element == "fire" or
            self.element == "earth" or
            self.element == "water"
        ):
            self.font_color = (255, 255, 255)
        else:
            self.font_color = (0, 0, 0)
        try:
            self.focus_cast
        except AttributeError:
            self.focus_cast = False
        try:
            self.cast
        except AttributeError:
            self.cast = False
        try:
            self.info
        except AttributeError:
            self.info = ""

    # Set Health
    def set_health(self, health):
        self.health = health
        self.update()

    # Set Power
    def set_power(self, power):
        self.power = power
        self.update()

    # Turn off/On label on card.
    # for example to distinguish cards for cast action
    def light_switch(self, on):
        if on:
            self.light = True
        else:
            self.light = False
        self.update()

    # play cast sound if sounds turned on in options
    def play_cast_sound(self):
        pygame.mixer.music.load(
            os.path.join(
                wzglobals.current_folder, 'misc', 'sounds', 'card_cast.ogg'
            )
        )
        wzglobals.playmusic()
        return

    # play summon sound if sounds turned on in options
    def play_summon_sound(self):
        pygame.mixer.music.load(
            os.path.join(
                wzglobals.current_folder, 'misc', 'sounds', 'card_summon.ogg'
            )
        )
        wzglobals.playmusic()
        return

    # returns opposite cardbox Id.
    def get_attack_position(self):
        if self.parent.position < 5:
            attack_position = self.parent.position + 5
        else:
            attack_position = self.parent.position - 5
        return attack_position

    # returns array of cards of player, who has this card
    def get_self_cards(self):
        cards = []
        if self.parent.position < 5:
            for cardbox in wzglobals.cardboxes[0:5]:
                if cardbox.card.name != "player":
                    cards.append(cardbox.card)
        else:
            for cardbox in wzglobals.cardboxes[5:10]:
                if cardbox.card.name != "player":
                    cards.append(cardbox.card)
        return cards

    # returns cardboxes of player, who has this card
    def get_self_cardboxes(self):
        cardboxes = []
        if self.parent.position < 5:
            for cardbox in wzglobals.cardboxes[0:5]:
                cardboxes.append(cardbox)
        else:
            for cardbox in wzglobals.cardboxes[5:10]:
                cardboxes.append(cardbox)
        return cardboxes

    # returns cardboxes of enemy of player, who has this card
    def get_enemy_cardboxes(self):
        cardboxes = []
        if self.parent.position < 5:
            for cardbox in wzglobals.cardboxes[5:10]:
                cardboxes.append(cardbox)
        else:
            for cardbox in wzglobals.cardboxes[0:5]:
                cardboxes.append(cardbox)
        return cardboxes

    # returns enemy cards
    def get_enemy_cards(self):
        cards = []
        if self.parent.position < 5:
            for cardbox in wzglobals.cardboxes[5:10]:
                if cardbox.card.name != "player":  # если есть карта
                    cards.append(cardbox.card)
        else:
            for cardbox in wzglobals.cardboxes[0:5]:
                if cardbox.card.name != "player":
                    cards.append(cardbox.card)
        return cards

    # return adjacent cardboxes ids
    # for example we has cardboxes [1, 2, 3, 4 ,5]
    # If we call this method from card, which is on cardbox with ID=4
    # this function returns [3,5]
    # If we call this method from card, which is on cardbox with ID=5
    # this function returns [4]
    def get_adjacent_position(self):
        adjacent_position = []
        self_position = self.parent.position
        if self_position < 5:
            if self_position > 0:
                if wzglobals.cardboxes[
                    self_position - 1
                ].card.name != "player":
                    adjacent_position.append(self_position - 1)
            if self_position < 4:
                if wzglobals.cardboxes[
                    self_position + 1
                ].card.name != "player":
                    adjacent_position.append(self_position + 1)
        else:
            if self_position > 5:
                if wzglobals.cardboxes[
                    self_position - 1
                ].card.name != "player":
                    adjacent_position.append(self_position - 1)
            if self_position < 9:
                if wzglobals.cardboxes[
                    self_position + 1
                ].card.name != "player":
                    adjacent_position.append(self_position + 1)
        return adjacent_position

    # return adjacent cardboxes ids of opposite cardbox
    # for example we has cardboxes:
    # [0, 1, 2, 3, 4]
    # [5, 6, 7, 8, 9]
    # if we call this method from card, which is on cardbox with ID=2,
    # function returns [6, 8]
    # if we call this method from card, which is on cardbox with ID=9,
    # function returns [3]
    def get_attack_adjacent_position(self, attack_position):
        adjacent_position = []
        if attack_position < 5:
            if attack_position > 0:
                if wzglobals.cardboxes[
                    attack_position - 1
                ].card.name != "player":
                    adjacent_position.append(attack_position - 1)
            if attack_position < 4:
                if wzglobals.cardboxes[
                    attack_position + 1
                ].card.name != "player":
                    adjacent_position.append(attack_position + 1)
        else:
            if attack_position > 5:
                if wzglobals.cardboxes[
                    attack_position - 1
                ].card.name != "player":
                    adjacent_position.append(attack_position - 1)
            if attack_position < 9:
                if wzglobals.cardboxes[
                    attack_position + 1
                ].card.name != "player":
                    adjacent_position.append(attack_position + 1)
        return adjacent_position

    # start attack animation
    def run_attack_animation(self):
        cardbox_location = (
            wzglobals.cardboxes[self.parent.position].rect[0],
            wzglobals.cardboxes[self.parent.position].rect[1]
        )
        if not self.image:
            print(
                'ERROR: run_attack_animation has been called '
                'without a valid image'
            )
            return
        attack_animation = animations.CustomAnimation(
            self.image, cardbox_location
        )  # Instantiating a animation object
        # dump method to determine which cardbox is used
        # (top/enemy or button/your)
        # TODO make different attack animation which not depend from
        # Y axis value.
        if (cardbox_location[1] > 200):
            attack_animation.path = [
                (cardbox_location[0], cardbox_location[1]-30)
            ]
        else:
            attack_animation.path = [
                (cardbox_location[0], cardbox_location[1]+30)
            ]
        attack_animation.attacking()  # Selecting Method

    # Function called when card in Attack phase
    def attack(self):  # Функция , срабатываемая при атаке персонажа
        if self.moves_alive:
            attack_position = self.get_attack_position()
            kill = wzglobals.cardboxes[attack_position].card.damage(
                self.power, self
            )
            self.run_attack_animation()
            return kill
        else:
            return 0

    # Function which called if card has some "cast action" and player
    # press on this card. Without choosing target!
    def cast_action(self):
        if self.focus_cast:
            # тут буду пробовать организовывать фокусированный каст
            wzglobals.cast_focus = True  # говорим программе,
            # что будет использоваться фокусированный каст
            wzglobals.cast_focus_wizard = self  # создаем ссылку на себя

    # function for cast which needs on target
    def focus_cast_action(self, target):
        pass

    # function which calls when any card summoned
    def card_summoned(self, card):
        pass

    # function which calls when any card dies
    def card_died(self, card):
        pass

    # function which calls when any spell used
    def spell_used(self, spell):
        pass

    # function for each friendly cards on field.
    # ( FUTURE FEATURE! NOT CODED YET )
    def for_each_self_card(self):
        pass

    # function which call when card in summon phase
    def summon(self):
        # TODO: use something else instead of turn function.
        self.play_summon_sound()
        for card in self.get_self_cards() + self.get_enemy_cards():
            card.card_summoned(self)
        if self.parent.player.id == 1:
            for card in wzglobals.ccards_1:
                Prototype.turn(card)
            # for card in wzglobals.ccards_1:
            #    card.additional_turn_action()
        else:
            for card in wzglobals.ccards_2:
                Prototype.turn(card)
            # for card in wzglobals.ccards_2:
            #    card.additional_turn_action()

    # tell to other cards about summon.
    # Calls card_summoned from each card on field.
    def summon_speaker(self):
        for card in (
            wzglobals.ccards_1.sprites() +
            wzglobals.ccards_2.sprites()
        ):
            card.card_summoned(self)

    # function which calls when card in damage phase.
    def damage(self, damage, enemy, cast=False):
        self.health -= damage
        self.update()
        if self.health <= 0:
            self.die()
            return 1
        return 0

    # Turn action, but with higher priority. Deprecated!
    # We will needs on new mechanism
    def additional_turn_action(self):
        return

    # function which calls when card in Die Phase
    def die(self):
        print("DEBUG: %s died" % self.name)
        for spell in self.spells:
            spell.unset(self)
        self.parent.card = self.parent.player
        self.parent.image.blit(self.parent.surface_backup, (0, 0))
        self.kill()
        for card in self.get_enemy_cards() + self.get_self_cards():
            card.card_died(self)
        try:
            pygame.mixer.music.load(
                os.path.join(
                    wzglobals.current_folder, 'misc', 'sounds', 'card_die.ogg'
                )
            )
        except:
            print("Unexpected error: while trying load die sound")
        wzglobals.playmusic()
        if self.image:
            del self.image

    # function which calls when card kill card in opposite cardbox
    def enemy_die(self):  # когда карта убивает противолежащего юнита
        self.killed += 1

    # function which called when card in Turn Phase
    # ( Beginning of player turn )
    def turn(self):
        self.power = self.default_power
        self.update()

    # Heal card.
    def heal(self, health, max_health):
        self.health += health
        if self.health > max_health:
            self.health = max_health
        self.update()

    # function that calculating factor of utility this card for some
    # type(summon, cast, etc) to some card.
    # For example this can to determine which card we should summon
    # againist Fire Drake
    def ai(self, type='summon', enemy=None):
        if type == 'summon':
            if wzglobals.player.mana[self.element] >= self.level:
                return (
                    wzglobals.player.mana[self.element] /
                    float(self.level)
                )
            else:
                return 0
        elif type == 'cast':
            return 0

    # Redraw
    def update(self):
        text_level = wzglobals.font2.render(
            str(self.level), True, self.font_color
        )
        text_power = wzglobals.font2.render(
            str(self.power), True, self.font_color
        )
        text_health = wzglobals.font2.render(
            str(self.health), True, self.font_color
        )
        self.image = self.surface_backup.copy()
        if self.cast:
            if self.field:
                if wzglobals.player == self.parent.player:
                    if not self.used_cast:
                        self.image.blit(
                            wzglobals.castlabel.cast_active, (0, 10)
                        )
                    else:
                        self.image.blit(
                            wzglobals.castlabel.cast_disabled, (0, 10)
                        )
        self.image.blit(text_level, (90, -7))
        self.image.blit(text_power, (5, 137))
        self.image.blit(text_health, (90, 137))
        if self.light:
            self.image.blit(self.light_image, (5, 5))
        if not self.field:  # Рисование в колоде
            self.parent = wzglobals.background
            xshift = (
                324 +
                self.position_in_deck * self.image.get_size()[0] +
                wzglobals.cardofelementsshower.shift *
                self.position_in_deck +
                2 * self.position_in_deck
            )
            yshift = 431
            self.parent.blit(self.image, (xshift, yshift))
            self.rect = self.image.get_rect()
            self.rect = self.rect.move(xshift, yshift)
        else:
            self.parent.image.blit(self.image, (0, 0))

    # function which called when the card`s owner gets damage
    def owner_gets_damage(self, damage):
        pass


class AbsoluteDefenceSpirit(Prototype):
    def __init__(self, card):
        self.name = card.name
        self.level = card.level
        self.element = card.element
        self.power = card.power
        self.health = card.health
        self.field = True
        self.imagefile = card.imagefile
        self.image = card.image
        self.card = card
        self.cast = card.cast
        Prototype.__init__(self)

    def damage(self, damage, enemy, cast=False):
        print("RESIST", damage, cast)
        return

    def attack(self):
        self.card.attack(self)

    def cast(self):
        self.card.cast(self)
