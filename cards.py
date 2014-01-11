# -*- coding: utf-8 -*-
import pygame.sprite
#from WizardsMagic import cardbox0
# To change this template, choose Tools | Templates
# and open the template in the editor.
__author__ = "chubakur"
__date__ = "$13.02.2011 18:46:32$"
water_cards = ["Nixie", "Hydra", "Waterfall", "Leviathan", "IceGuard", "Poseidon", "IceWizard", "Poison", "SeaJustice", "Paralyze", "AcidStorm", "IceBolt"]
fire_cards = ["Demon", "Devil", "Firelord", "RedDrake", "Efreet", "Salamander", "Vulcan", "Cerberus", "Armageddon", "Fireball", "FireSpikes", "FlamingArrow", "RitualFlame"]
air_cards = ["Phoenix", "Zeus", "Fairy", "Nymph", "Gargoyle", "Manticore", "Titan", "Plague", "Spellbreaker", "BlackWind", "ChainLightning"]
earth_cards = ["Satyr", "Golem", "Dryad", "Centaur", "Elemental", "Ent", "Echidna", "ForestSpirit", "AbsoluteDefence", "Earthquake", "Quicksands", "Restructure", "Revival"]
life_cards = ["Priest", "Paladin", "Pegasus", "Unicorn", "Apostate", "MagicHealer", "Chimera", "Bless", "GodsWrath", "LifeSacrifice", "Purify", "Rejuvenation"]
death_cards = ["Zombie", "Vampire", "GrimReaper", "Ghost", "Werewolf", "Banshee", "Darklord", "Lich", "ChaosVortex", "CoverOfDarkness", "Curse", "StealLife", "TotalWeakness"]
import pygame
from math import *
import globals
import player
pygame.font.init()
font = pygame.font.Font(None, 25)
class Prototype(pygame.sprite.Sprite): #Прототип карты воина
    def __init__(self):
        #self.group = group #Группа, в которой лежит эта карта
        pygame.sprite.Sprite.__init__(self)
        self.parent = 0
        self.light = False
        self.image = self.image.convert_alpha()
        self.light_image = pygame.image.load('misc/light.gif').convert_alpha()
        self.surface_backup = self.image.copy()
        self.font = pygame.font.Font(None, 19)
        self.type = "warrior_card"
        self.killed = 0
        self.spells = []
        self.default_power = self.power
        self.moves_alive = 0 #Сколько ходов прожила карта
        self.max_health = self.health #Максимальное кол-во жизней
        self.default_power = self.power
        self.field = False
        self.used_cast = False #Использовал cast
        if self.element == "death" or self.element == "fire" or self.element == "earth":
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
        #self.cast_button = pygame.Surface((30,20))
        #self.cast_button = self.cast_button.convert()
        #self.cast_button.fill((0,0,255))
    def set_health(self, health):
        self.health = health
        self.update()
    def set_power(self, power):
        self.power = power
        self.update()
    def light_switch(self, on):
        if on:
            self.light = True
        else:
            self.light = False
        self.update()
    def play_cast_sound(self):
        #pygame.mixer.music.load('misc/sounds/card_cast.wav')
        #pygame.mixer.music.play()
        return
    def play_summon_sound(self):
        #pygame.mixer.music.load('misc/sounds/card_summon.wav')
        #pygame.mixer.music.play()
        return
    def get_attack_position(self):
        if self.parent.position < 5:
            attack_position = self.parent.position + 5 #Id - блока, куда атаковать
        else:
            attack_position = self.parent.position-5
        return attack_position
    def get_self_cards(self):
        cards = []
        if self.parent.position < 5:
            for cardbox in globals.cardboxes[0:5]:
                if cardbox.card.name != "player": #если есть карта
                    cards.append(cardbox.card)
        else:
            for cardbox in globals.cardboxes[5:10]:
                if cardbox.card.name != "player":
                    cards.append(cardbox.card)
        return cards
    def get_self_cardboxes(self):
        cardboxes = []
        if self.parent.position < 5:
            for cardbox in globals.cardboxes[0:5]:
                cardboxes.append(cardbox)
        else:
            for cardbox in globals.cardboxes[5:10]:
                cardboxes.append(cardbox)
        return cardboxes
    def get_enemy_cardboxes(self):
        cardboxes = []
        if self.parent.position < 5:
            for cardbox in globals.cardboxes[5:10]:
                cardboxes.append(cardbox)
        else:
            for cardbox in globals.cardboxes[0:5]:
                cardboxes.append(cardbox)
        return cardboxes
    def get_enemy_cards(self):
        cards = []
        if self.parent.position < 5:
            for cardbox in globals.cardboxes[5:10]:
                if cardbox.card.name != "player": #если есть карта
                    cards.append(cardbox.card)
        else:
            for cardbox in globals.cardboxes[0:5]:
                if cardbox.card.name != "player":
                    cards.append(cardbox.card)
        return cards
    def get_adjacent_position(self):
        adjacent_position = []
        self_position = self.parent.position
        if self_position < 5:
            if self_position > 0:
                if globals.cardboxes[self_position - 1].card.name != "player":
                    adjacent_position.append(self_position - 1)
            if self_position < 4:
                if globals.cardboxes[self_position + 1].card.name != "player":
                    adjacent_position.append(self_position + 1)
        else:
            if self_position > 5:
                if globals.cardboxes[self_position - 1].card.name != "player":
                    adjacent_position.append(self_position - 1)
            if self_position < 9:
                if globals.cardboxes[self_position + 1].card.name != "player":
                    adjacent_position.append(self_position + 1)
        return adjacent_position
    def get_attack_adjacent_position(self, attack_position):
        adjacent_position = []
        if attack_position < 5:
            if attack_position > 0:
                if globals.cardboxes[attack_position-1].card.name != "player":
                    adjacent_position.append(attack_position-1)
            if attack_position < 4:
                if globals.cardboxes[attack_position + 1].card.name != "player":
                    adjacent_position.append(attack_position + 1)
        else:
            if attack_position > 5:
                if globals.cardboxes[attack_position-1].card.name != "player":
                    adjacent_position.append(attack_position-1)
            if attack_position < 9:
                if globals.cardboxes[attack_position + 1].card.name != "player":
                    adjacent_position.append(attack_position + 1)
        return adjacent_position
    def attack(self): #Функция , срабатываемая при атаке персонажа
        if self.moves_alive:
            attack_position = self.get_attack_position()
            kill = globals.cardboxes[attack_position].card.damage(self.power, self)
            return kill
        else:
            return 0
    def cast_action(self):
        if self.focus_cast: #тут буду пробовать организовывать фокусированный каст
            globals.cast_focus = True #говорим программе, что будет использоваться фокусированный каст
            globals.cast_focus_wizard = self #создаем ссылку на себя
    def focus_cast_action(self, target):
        pass
    def card_summoned(self, card): #when any card summon to the field
        pass
    def card_died(self, card): #when any card dies
        pass
    def summon(self): # когда призывают
        self.play_summon_sound()
        for card in self.get_self_cards() + self.get_enemy_cards():
            card.card_summoned(self)
        if self.parent.player.id == 1:
            for card in globals.ccards_1:
                Prototype.turn(card)
            for card in globals.ccards_1:
                card.additional_turn_action()
        else:
            for card in globals.ccards_2:
                Prototype.turn(card)
            for card in globals.ccards_2:
                card.additional_turn_action()
    def damage(self, damage, enemy, cast=False): #Функция, срабатываемая при получении урона.
        self.health -= damage
        self.update()
        if self.health <= 0:
            self.die()
            return 1
        return 0
    def additional_turn_action(self): # Turn action, but with higher priority.
        return
    def die(self): #Смерть персонажа
        for spell in self.spells:
            spell.unset(self)
        self.parent.card = self.parent.player #Обнуляем карту в объекте-родителе
        self.parent.image.blit(self.parent.surface_backup, (0, 0)) #Рисуем объект-родитель поверх карты
        self.kill() #Выкидываем карту из всех групп
        for card in self.get_enemy_cards() + self.get_self_cards():
            card.card_died(self)
        #pygame.mixer.music.load('misc/sounds/card_die.wav')
        #pygame.mixer.music.play()
    def enemy_die(self): #когда карта убивает противолежащего юнита
        self.killed += 1
    def turn(self):
        self.power = self.default_power
        self.used_cast = False
        self.moves_alive += 1
        self.update()
        #print 1
        #print self.playerscards[self.parent.player.id-1].sprites() # Функция, которая вызывается каждый ход. Например для ледяного голема, у которого отнимаются жизни каждый ход.
    def heal(self, health, max_health):
        self.health += health
        if self.health > max_health:
            self.health = max_health
        self.update()
    def update(self): #Field - True если рисовать на поле, false - если рисовать в таблице выбора
        text_level = globals.font.render(str(self.level), True, self.font_color)
        text_power = globals.font.render(str(self.power), True, self.font_color)
        text_health = globals.font.render(str(self.health), True, self.font_color)
        self.image = self.surface_backup.copy()
        if self.cast:
            if not self.used_cast:
                text_cast = font.render("Cast", True, (0, 0, 255))
                self.image.blit(text_cast, (50, 100))
            else:
                text_cast = font.render("Cast", True, (0, 0, 0))
                self.image.blit(text_cast, (50, 100))
        #print text_power
        self.image.blit(text_level, (85, 0))
        self.image.blit(text_power, (10, 130))
        self.image.blit(text_health, (85, 130))
        if self.light:
            self.image.blit(self.light_image, (10, 50))
        if not self.field: #Рисование в колоде
            self.parent = globals.background
            if globals.cardofelementsshower.first_part:
                xshift = 389 + self.position_in_deck * self.image.get_size()[0] + globals.cardofelementsshower.shift * self.position_in_deck
            else:
                xshift = 389 + (self.position_in_deck - 1) * self.image.get_size()[0] + globals.cardofelementsshower.shift * (self.position_in_deck - 1)
            yshift = 436
            self.parent.blit(self.image, (xshift, yshift))
            self.rect = self.image.get_rect()
            self.rect = self.rect.move(xshift, yshift)
        else:
            self.parent.image.blit(self.image, (0, 0))
    def owner_get_damage(self, damage): #Function call when card`s owner get damage
        pass
class Nixie(Prototype):
    def __init__(self):        
        self.name = "Nixie"
        self.element = "water"
        self.level = 4
        self.power = 3
        self.health = 10
        self.cast = True
        self.image = pygame.image.load('misc/cards/water/nixie.gif')
        self.info = "Causes 200% of damage to fire creatures. Gives owner 1 Water in the beginning of owner's turn. Casting Sea of Sacred increases owner's Water by 1 and reduces Fire by 1."
        Prototype.__init__(self)
    def attack(self):
        if self.moves_alive:
            attack_position = self.get_attack_position()
            if globals.cardboxes[attack_position].card.name != "player": #если есть карта
                if globals.cardboxes[attack_position].card.element == "fire": #если стихия карты - огонь
                    globals.cardboxes[attack_position].card.damage(self.power * 2, self)
                else:
                    globals.cardboxes[attack_position].card.damage(self.power, self)
            else:
                globals.cardboxes[attack_position].card.damage(self.power, self)
        else:
            return
    def cast_action(self):
        self.play_cast_sound()
        if self.parent.player.fire_mana:
            self.parent.player.fire_mana -= 1
            self.parent.player.water_mana += 1
            self.used_cast = True
        #Наносит картам элемента огня урон 200%
        #КАСТ:уменьшает ману огня на 1, увеличивает ману воды на 1
class Hydra(Prototype):
    def __init__(self):        
        self.name = "Hydra"
        self.element = "water"
        self.level = 13
        self.power = 5
        self.cast = True
        self.focus_cast = True
        self.health = 29
        self.info = "Attacks both adjacent slots. Reduces owner`s Water by 2 every turn. CAST: Consumes friendly unit, receiving up to 50% of his health."
        self.image = pygame.image.load('misc/cards/water/hydra.gif')
        Prototype.__init__(self)
    def attack(self):
        if self.moves_alive:
            attack_position = self.get_attack_position()
            globals.cardboxes[attack_position].card.damage(self.power, self)
            adjacent_positions = self.get_attack_adjacent_position(attack_position)
            for adjacent_position in adjacent_positions:
                globals.cardboxes[adjacent_position].card.damage(self.power, self)
        else:
            return
    def turn(self):
        Prototype.turn(self)
        self.parent.player.water_mana -= 2
        if self.parent.player.water_mana < 0:
            self.parent.player.water_mana = 0
    def cast_action(self):
        Prototype.cast_action(self)
        for card in self.get_self_cards():
            if card != self:
                card.light_switch(True)
    def focus_cast_action(self, target):
        if target.name != 'player': #if card exist
            if target.parent.player.id == self.parent.player.id:
                hp = target.health
                target.die()
                self.heal(int(ceil(hp / 2.0)), self.max_health)
            else:
                return
        else:
            return
class Waterfall(Prototype):
    def __init__(self):        
        self.name = "Waterfall"
        self.element = "water"
        self.level = 9
        self.power = 1
        self.cast = False
        self.health = 33
        self.image = pygame.image.load('misc/cards/water/waterfall.gif')
        self.info = "One of the toughest Elementals. Health itself for 3 whenever any player casts water spell of summons water creature. Attack equal to owner`s Water."
        Prototype.__init__(self)
    def turn(self):
        Prototype.turn(self)
        self.power = self.parent.player.water_mana
        if not self.power:
            self.power = 1
class Leviathan(Prototype):
    def __init__(self):        
        self.name = "Leviathan"
        self.element = "water"
        self.level = 11
        self.power = 6
        self.cast = False
        self.health = 37
        self.image = pygame.image.load('misc/cards/water/leviathan.gif')
        self.info = ""
        Prototype.__init__(self)
class IceGuard(Prototype):
    def __init__(self):        
        self.name = "IceGuard"
        self.element = "water"
        self.level = 5
        self.info = "Reduces all damage done to owner by 50%. Suffers 200% damage from fire."
        self.power = 4
        self.cast = False
        self.health = 19
        self.image = pygame.image.load('misc/cards/water/ice_guard.gif')
        Prototype.__init__(self)
    def damage(self, damage, enemy, cast=False):
        if enemy.element == "fire":
            Prototype.damage(self, damage*2, enemy, cast)
        else:
            Prototype.damage(self, damage, enemy, cast)
    def owner_get_damage(self, damage):
        self.parent.player.heal(damage/2)
class Poseidon(Prototype):
    def __init__(self):        
        self.name = "Poseidon"        
        self.element = "water"
        self.level = 8
        self.power = 3
        self.info = "Every time anyone casts Water spell or summons Water creature, opponent suffers 4 damage and owner gains 2 health."
        self.cast = False
        self.health = 25
        self.image = pygame.image.load('misc/cards/water/poseidon.gif')
        Prototype.__init__(self)
class IceWizard(Prototype):
    def __init__(self):        
        self.name = "IceWizard"        
        self.element = "water"
        self.level = 10
        self.info = "Increases Water by 2 every turn. Suffers 200% damage from fire. All damage from Water equal to 1. CAST: Casting Healing Water heals owner equal to 2*Water points. Owner loses all Water."
        self.power = 4
        self.cast = True
        self.health = 22
        self.image = pygame.image.load('misc/cards/water/ice_wizard.gif')
        Prototype.__init__(self)
    def turn(self):
        Prototype.turn(self)
        self.parent.player.water_mana += 2
    def damage(self, damage, enemy, cast=False):
        if enemy.element == 'fire':
            Prototype.damage(self, damage * 2, enemy)
        elif enemy.element == 'water':
            Prototype.damage(self, 1, enemy)
        else:
            Prototype.damage(self, damage, enemy)
    def cast_action(self):
        water = self.parent.player.water_mana
        self.parent.player.water_mana = 0
        self.parent.player.heal(water * 2)
class Demon(Prototype):
    def __init__(self):        
        self.name = "Demon"        
        self.element = "fire"
        self.level = 5
        self.power = 2
        self.info = "Doesn`t suffer from Fire and Earth spells. CAST: Whenever Demon casts Fire Bleed owner loses 1 Earth and receives 2 Fire elements."
        self.cast = True
        self.health = 12
        self.image = pygame.image.load('misc/cards/fire/demon.gif')
        Prototype.__init__(self)
    def cast_action(self):
        self.play_cast_sound()
        if self.parent.player.earth_mana:
            self.parent.player.earth_mana -= 1
            self.parent.player.fire_mana += 2
            self.used_cast = True
        #Не получает повреждения от заклинаний огня и земли
        #cast: владелец теряет один элемент земли и получает 2 огня
class Devil(Prototype):
    def __init__(self):        
        self.name = "Devil"        
        self.element = "fire"
        self.info = "Damage from Water is multiplied by 2. Whenever Devil dies, owner suffers 10 damage. CAST: Sacrificing owner`s Fire creature gives 3 Fire to the owner, also healing owner by this amount."
        self.level = 6
        self.power = 4
        self.cast = True
        self.focus_cast = True
        self.health = 27
        self.image = pygame.image.load('misc/cards/fire/devil.gif')
        Prototype.__init__(self)
    def die(self):
        self.parent.player.damage(10, self)
        Prototype.die(self)
    def damage(self, damage, enemy, cast=False):
        if enemy.element == "water":
            Prototype.damage(self, damage * 2, enemy)
        else:
            Prototype.damage(self, damage, enemy)
    def cast_action(self):
        Prototype.cast_action(self) #enable focus-cast
        for card in self.get_self_cards():
            if card.element == 'fire' and card != self:
                card.light_switch(True)
            else:
                continue
    def focus_cast_action(self, target):
        if target.name != 'player': #if it is real card
            if target.parent.player.id == self.parent.player.id: #if it is caster`s card
                if target.element == 'fire':
                    if target != self:
                        self.play_cast_sound()
                        self.used_cast = True
                        globals.cast_focus = False
                        self.parent.player.fire_mana += 3
                        self.parent.player.heal(target.health)
                        target.die()
                        for card in self.get_self_cards():
                            card.light_switch(False)
class RedDrake(Prototype):
    def __init__(self):        
        self.name = "RedDrake"        
        self.element = "fire"
        self.level = 7
        self.info = "When summoned, each enemy creature and enemy player suffers 3 damage. Red Drake Suffers no damage from Fire spells and creatures."
        self.power = 5
        self.cast = False
        self.health = 16
        self.image = pygame.image.load('misc/cards/fire/red_drake.gif')
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
class Firelord(Prototype):
    def __init__(self):        
        self.name = "Firelord"        
        self.element = "fire"
        self.level = 11
        self.power = 7
        self.cast = False
        self.info = "Opens fire gates. This means that both players should receive 1 additional Fire every turn. Upon dying, Firelord brings 8 damage to each player."
        self.health = 21
        self.image = pygame.image.load('misc/cards/fire/firelord.gif')
        Prototype.__init__(self)
    def turn(self):
        Prototype.turn(self)
        self.parent.player.fire_mana += 1
        self.parent.player.enemy.fire_mana += 1
    def die(self):
        self.parent.player.damage(8, self)
        self.parent.player.enemy.damage(8, self)
        Prototype.die(self)
class Salamander(Prototype):
    def __init__(self):        
        self.name = "Salamander"        
        self.element = "fire"
        self.level = 8
        self.power = 3
        self.cast = False
        self.info = "Increases attack of all owner's creatures by 2. Increases damage from owner player's spellcastings by 2."
        self.health = 15
        self.image = pygame.image.load('misc/cards/fire/salamander.gif')
        Prototype.__init__(self)
    def additional_turn_action(self):
        for card in self.get_self_cards():
            #card.default_power += 2
            if card != self:
                card.power = card.power + 2
                card.update(0)
    def summon(self):
        Prototype.summon(self)
        self.additional_turn_action()
class Efreet(Prototype):
    def __init__(self):        
        self.name = "Efreet"        
        self.element = "fire"
        self.level = 10 #10
        self.power = 6
        self.cast = False
        self.health = 33
        self.info = "Whenever any creature attacks Efreet, that creature suffers half of damage send back (same applies to Fire Shield spell). Uppon summoning, all enemy Water creatures suffer 6 damage. CAST: Casts Fire Shield on any owner`s creature. Costs 2 Fire. Fire Shield burns creature from inside, damaging it for 2 points per turn, unless it`s a Fire creature."
        self.image = pygame.image.load('misc/cards/fire/efreet.gif')
        Prototype.__init__(self)
    def summon(self):
        Prototype.summon(self)
        for card in self.get_enemy_cards():
            if card.element == "water":
                card.damage(6, self)
            else:
                continue
    def damage(self, damage, enemy, cast = False):
        if not cast:
            Prototype.damage(self, damage, enemy, cast)
            Prototype.damage(enemy, damage / 2, self, cast)
class Vulcan(Prototype):
    def __init__(self):        
        self.name = "Vulcan"        
        self.element = "fire"
        self.level = 12
        self.power = 1
        self.cast = True
        self.info = "Fire Elemental. Immune to harmful Fire spells. When summoned, enemy player loses 3 Fire, and opposed Elemental unit suffers 9 damage. Attack equal to owner`s Fire + 3. CAST: Casts Volcano Explode. Vulcan dies, but every unit on field suffers damage equal to 50% of Vulcan`s health."
        self.health = 27
        self.image = pygame.image.load('misc/cards/fire/vulcan.gif')
        Prototype.__init__(self)
    def summon(self):
        Prototype.summon(self)
        self.set_power(self.parent.player.fire_mana - self.level + 3)
        if self.parent.player.enemy.fire_mana >= 3:
            self.parent.player.enemy.fire_mana -= 3
        else:
            self.parent.player.enemy.fire_mana = 0
        opp_card = globals.cardboxes[self.get_attack_position()].card
        if opp_card.name != 'player':
            opp_card.damage(9, self)
    def turn(self):
        Prototype.turn(self)
        self.set_power(self.parent.player.fire_mana + 3)
    def cast_action(self):
        hp = self.health
        for card in self.get_enemy_cards() + self.get_self_cards():
            card.damage(int(floor(hp / 2.0)), self)
        self.die()
class Cerberus(Prototype):
    def __init__(self):        
        self.name = "Cerberus"        
        self.element = "fire"
        self.level = 4
        self.power = 4
        self.info = "Attacks adjacent enemy units at a half of it`s strength."
        self.cast = False
        self.health = 6
        self.image = pygame.image.load('misc/cards/fire/cerberus.gif')
        Prototype.__init__(self)
    def attack(self):
        if self.moves_alive:
            attack_position = self.get_attack_position()
            globals.cardboxes[attack_position].card.damage(self.power, self)
            adjacent_positions = self.get_attack_adjacent_position(attack_position)
            for adjacent_position in adjacent_positions:
                if not globals.cardboxes[adjacent_position].card.power / 2:
                    globals.cardboxes[adjacent_position].card.damage(1, self)
                else:
                    globals.cardboxes[adjacent_position].card.damage(int(ceil(float(globals.cardboxes[adjacent_position].card.power) / 2)), self)
        else:
            return
class Nymph(Prototype):
    def __init__(self):        
        self.name = "Nymph"        
        self.element = "air"
        self.level = 3
        self.power = 1
        self.cast = False
        self.info = "Owner receives 1 Air at the beginning of Owners turn."
        self.health = 12
        self.image = pygame.image.load('misc/cards/air/nymph.gif')
        Prototype.__init__(self)
    def turn(self):
        Prototype.turn(self)
        self.parent.player.air_mana += 1
        #Каждый ход владелец получает дополнительно 1 воздух
class Fairy(Prototype):
    def __init__(self):        
        self.name = "Fairy"        
        self.element = "air"
        self.info = "Increases its attack by 1 for each creature, killed on a field. CAST: Enslave Mind forces strongest enemy creature to attack it`s owner. Costs 1 Air."
        self.level = 3
        self.power = 3
        self.cast = True
        self.health = 7
        self.image = pygame.image.load('misc/cards/air/fairy.gif')
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
        if self.parent.player.air_mana:
            self.used_cast = True
            self.parent.player.air_mana -= 1
            self.play_cast_sound()
            max = 0
            max_link = False
            for card in self.get_enemy_cards():
                if card.power > max:
                    max = card.power
                    max_link = card
            if max_link:
                self.parent.player.enemy.damage(card.power, card)
        #Атака увеличивается на 1 за каждого убитого
        #КАСТ. Сильнейшая карта врага атакует своего героя. 1 воздух.
class Phoenix(Prototype):
    def __init__(self):        
        self.name = "Phoenix"        
        self.element = "air"
        self.info = "If Phoenix was killed by Fire spell or creature, rebirth with full health."
        self.level = 6
        self.power = 4
        self.cast = False
        self.health = 20
        self.recovered = 0 #Восстанавливалась ли карта
        self.image = pygame.image.load('misc/cards/air/phoenix.gif')
        Prototype.__init__(self)
    def damage(self, damage, enemy, cast=False):
        self.health -= damage
        self.update()
        if self.health <= 0:
            if enemy.element == "fire": #Если стихия врага - огонь
                if not self.recovered: #если не восстанавливалась
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
            #self.die()
class Zeus(Prototype):
    def __init__(self):        
        self.name = "Zeus"        
        self.element = "air"
        self.level = 9
        self.power = 3
        self.cast = False
        self.health = 24
        self.info = "Owner receives 1 air element for each enemy creature, killed by Zeus. CAST: Strikes Lighting into choosen creature. Costs 1 Air and inflicts 8 damage. Cannot strike creatures of level 7 and highter."
        self.image = pygame.image.load('misc/cards/air/zeus.gif')
        Prototype.__init__(self)
    def attack(self):
        if self.moves_alive:
            attack_position = self.get_attack_position()
            kill = globals.cardboxes[attack_position].card.damage(self.power, self)
            if kill:
                self.parent.player.air_mana += 1
        else:
            return
class Gargoyle(Prototype):
    def __init__(self):        
        self.name = "Gargoyle"        
        self.element = "air"
        self.info = "Suffers no damage from Earth and Air spells. CAST: Casts Petrification on self, as effect turns to stone. In stone form Gargoyle reduces damage done to it by 2 . Owner loses 3 Air and 1 Earth."
        self.level = 5
        self.power = 4
        self.cast = True
        self.health = 15
        self.image = pygame.image.load('misc/cards/air/gargoyle.gif')
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
        if self.parent.player.air_mana >= 3 and self.parent.player.earth_mana:
            self.play_cast_sound()
            self.parent.player.air_mana -= 3
            self.parent.player.earth_mana -= 1
            self.used_cast = True
            self.stone = True
    def turn(self):
        Prototype.turn(self)
        self.stone = False
class Manticore(Prototype):
    def __init__(self):        
        self.name = "Manticore"        
        self.element = "air"
        self.info = "Attacks casters with additional 3 damage. Only suffers 50% damage from spells. CAST: Casts Memory Loss. Target enemy creature permanently loses ability to cast. Costs 2 Air."
        self.level = 7
        self.power = 5
        self.cast = True
        self.focus_cast = True
        self.health = 19
        self.image = pygame.image.load('misc/cards/air/manticore.gif')
        Prototype.__init__(self)
    def attack(self):
        attack_position = self.get_attack_position()
        if globals.cardboxes[attack_position].card.name != 'player': #if card exist
            if globals.cardboxes[attack_position].card.cast:
                globals.cardboxes[attack_position].card.damage(self.power + 3, self)
            else:
                globals.cardboxes[attack_position].card.damage(self.power, self)
        else:
            globals.cardboxes[attack_position].card.damage(self.power, self)
    def cast_action(self):
        if self.parent.player.air_mana >= 2: #if player have mana for cast
            Prototype.cast_action(self) #activating focus-cast
            for card in self.get_enemy_cards():
                if card.cast: #if it`s caster
                    card.light_switch(True) #enable lighting
    def focus_cast_action(self, target):
        if target.name != 'player': #if it is real card
            if target.parent.player.id != self.parent.player.id: #if it is enemy`s card
                if target.cast: #if it is caster
                    target.cast = False #target now can`t cast
                    self.used_cast = True #This means, that this card cast already
                    globals.cast_focus = False #focus-cast off
                    self.parent.player.air_mana -= 2 #decrease player`s mana. It is payment for this action.
                    self.play_cast_sound() #play cast sound
                    for card in self.get_enemy_cards(): #disable lighting
                        card.light_switch(False)
                else:
                    return
            else:
                return
        else:
            return
class Titan(Prototype):
    def __init__(self):        
        self.name = "Titan"        
        self.element = "air"
        self.level = 11
        self.power = 7
        self.cast = True
        self.info = "When summoned, enemy loses 3 Air. Titan`s attack is increased by 1 for each Air creature in play. CAST: Casts Thunder Fist. All enemy Earth creatures suffer 3 damage. Owner loses 1 Air."
        self.health = 28
        self.image = pygame.image.load('misc/cards/air/titan.gif')
        Prototype.__init__(self)
    def summon(self):
        Prototype.summon(self)
        self.parent.player.enemy.air_mana -= 3
        if self.parent.player.enemy.air_mana < 0:
            self.parent.player.enemy.air_mana = 0
    def cast_action(self):
        self.play_cast_sound()
        if self.parent.player.air_mana:
            self.parent.player.air_mana -= 1
            for enemy_card in self.get_enemy_cards():
                if enemy_card.element == "earth":
                    enemy_card.damage(3, self)
#    def enemy_die(self): #Перепутал способность
#        Prototype.enemy_die(self)
#        self.power+=1
#        self.update()
class Satyr(Prototype):
    def __init__(self):        
        self.name = "Satyr"        
        self.element = "earth"
        self.level = 2
        self.power = 3
        self.cast = True
        self.info = "Increases Earth by 1 every turn. CAST: Once Satyr casts Dissolve, it dies and creature in the opposed slot suffers 5 damage. If there`s no creature, damage dealt to enemy player."
        self.health = 10
        self.image = pygame.image.load('misc/cards/earth/satyr.gif')
        Prototype.__init__(self)
    def turn(self):
        Prototype.turn(self)
        self.parent.player.earth_mana += 1
    def cast_action(self):
        self.play_cast_sound()
        if self.parent.position < 5:
            attack_position = self.parent.position + 5 #Id - блока, куда атаковать
        else:
            attack_position = self.parent.position-5
        globals.cardboxes[attack_position].card.damage(5, self)
        self.die()
class Golem(Prototype):
    def __init__(self):        
        self.name = "Golem"        
        self.element = "earth"
        self.level = 5
        self.power = 4
        self.cast = False
        self.health = 15
        self.info = "Regenerates 3 health every turn. While owner's Earth less than 3, it suffers 3 damage instead."
        self.image = pygame.image.load('misc/cards/earth/golem.gif')
        Prototype.__init__(self)
    def turn(self):
        Prototype.turn(self)
        if self.parent.player.earth_mana < 3:
            self.damage(3, self)
        else:
            self.heal(3, self.max_health)
class Dryad(Prototype):
    def __init__(self):        
        self.name = "Dryad"        
        self.element = "earth"
        self.level = 4
        self.power = 4
        self.cast = False
        self.health = 12
        self.info = "Adjacent owner creatures attack increases by 1, and if it`s Earth creature, by 2 whenever anyone casts Earth spell of summons Earth creature."
        self.image = pygame.image.load('misc/cards/earth/dryad.gif')
        Prototype.__init__(self)
    def additional_turn_action(self):F
        ids = self.get_adjacent_position()
        if ids:
            for id in ids:
                globals.cardboxes[id].card.set_power( globals.cardboxes[id].card.power + 1)
    def summon(self):
        Prototype.summon(self)
        self.additional_turn_action()
class ForestSpirit(Prototype):
    def __init__(self):        
        self.name = "ForestSpirit"        
        self.element = "earth"
        self.level = 3
        self.info = "Daamge from all non-magical attacks and abilities equal to 1. CAST: Casts Youth of Forest, increasing owner player`s health by 5. Costs two Earth elements."
        self.power = 2
        self.cast = True
        self.health = 3
        self.image = pygame.image.load('misc/cards/earth/forest_spirit.gif')
        Prototype.__init__(self)
    def damage(self, damage, enemy, cast=False):
        self.health -= 1
        self.update()
        if self.health <= 0:
            self.die()
            return 1
        return 0
    def cast_action(self):
        if self.parent.player.earth_mana >= 2:
            self.parent.player.earth_mana -= 2
            self.used_cast = True
            self.play_cast_sound()
            self.parent.player.heal(5)
class Centaur(Prototype):
    def __init__(self):        
        self.name = "Centaur"        
        self.element = "earth"
        self.level = 6
        self.info = "Attacks the same turn he was summoned(No summon sickness). CAST: Strikes magic arrow into enemy player, dealing 3 damage. Costs 1 Earth."
        self.power = 5
        self.cast = True
        self.health = 14
        self.image = pygame.image.load('misc/cards/earth/centaur.gif')
        Prototype.__init__(self)
        self.moves_alive = 1
    def cast_action(self):
        if self.parent.player.earth_mana:
            self.play_cast_sound()
            self.parent.player.enemy.damage(3, self)
            self.parent.player.earth_mana -= 1
            self.used_cast = True
class Elemental(Prototype):
    def __init__(self):        
        self.name = "Elemental"
        self.element = "earth"        
        self.level = 13
        self.power = 1
        self.cast = False
        self.info = "Attack equal to owner`s Earth. Increases Earth by 2 every turn. Fire spells deal additional 10 damage. CAST: Casts Stone Skin onto owner`s creature. That creature gain 1 point of defence from all attacks greater than 1."
        self.health = 45
        self.image = pygame.image.load('misc/cards/earth/elemental.gif')
        Prototype.__init__(self)
    def summon(self):
        Prototype.summon(self)
        self.set_power(self.parent.player.earth_mana - self.level)
    def turn(self):
        Prototype.turn(self)
        self.parent.player.earth_mana += 2
        self.set_power(self.parent.player.earth_mana)
class Ent(Prototype):
    def __init__(self):        
        self.name = "Ent"
        self.element = "earth"        
        self.level = 7
        self.power = 3
        self.info = "Attacks opposed unit and enemy player at the same time. Casts Entangle Roots, damaging each enemy unit for 1 and losing 2 points of own health."
        self.cast = True
        self.health = 22
        self.image = pygame.image.load('misc/cards/earth/ent.gif')
        Prototype.__init__(self)
    def attack(self):
        e_card = globals.cardboxes[self.get_attack_position()].card
        Prototype.attack(self)
        if self.moves_alive:
            if e_card.name != 'player':
                self.parent.player.enemy.damage(self.power, self)
        e_card = None
    def cast_action(self):
        for card in self.get_enemy_cards():
            card.damage(1, self)
        self.used_cast = True
        self.damage(2, self)
class Echidna(Prototype):
    def __init__(self):        
        self.name = "Echidna"
        self.element = "earth"        
        self.level = 10
        self.power = 7
        self.cast = False
        self.health = 26
        self.poisoned = []
        self.info = "When attacks, poisons her target. This target will lose 2 health every turn. In the beginning og owner`s turn, Echidna hits all poisoned creatures for 1."
        self.image = pygame.image.load('misc/cards/earth/echidna.gif')
        Prototype.__init__(self)
    def attack(self):
        Prototype.attack(self)
        if not globals.cardboxes(self.get_attack_position()).card in self.poisoned:
            self.poisoned.append(globals.cardboxes(self.get_attack_position()).card)
class EchidnaPoison(Magic):
    pass
class Priest(Prototype):
    def __init__(self):        
        self.name = "Priest"        
        self.element = "life"
        self.level = 4
        self.cast = False
        self.power = 1
        self.health = 9
        self.info = "Increases owner`s Life by 2 every turn, decreasing Death by the same amount. Decreases owner`s Life by 3 every time owner casts Death spells."
        self.image = pygame.image.load('misc/cards/life/priest.gif')
        Prototype.__init__(self)
    def turn(self):
        Prototype.turn(self)
        if self.parent.player.death_mana >= 2:
            self.parent.player.death_mana -= 2
            self.parent.player.life_mana += 2
class Paladin(Prototype):
    def __init__(self):        
        self.name = "Paladin"
        self.element = "life"
        self.info = "Brings 300% of damage to undead creatures. CAST: Casts Exorcism. Destroys any undead, but suffers 10 damage himself. Owner also loses 2 Life as a cost of this holy casting."
        self.cast = True
        self.focus_cast = True
        self.level = 8
        #self.level = 1
        self.power = 4
        self.health = 20
        self.image = pygame.image.load('misc/cards/life/paladin.gif')
        Prototype.__init__(self)
    def cast_action(self):
        if self.parent.player.life_mana >= 2: #если хватает маны, то активируем фокус
            Prototype.cast_action(self)
            for card in self.get_enemy_cards():
                if card.element == "death":
                    card.light_switch(True)
    def focus_cast_action(self, target):
        if target.name != "player": #если это реальная карта
            if target.parent.player.id != self.parent.player.id: #если это чужая карта
                if target.element == "death":
                    #действие
                    self.used_cast = True
                    globals.cast_focus = False
                    target.die()
                    self.damage(10, self)
                    self.parent.player.life_mana -= 2
                    self.play_cast_sound()
                    for card in self.get_enemy_cards(): #отключаем подсветку
                        card.light_switch(False)
                else:
                    return #Если паладин не может подействовать на эту карту
            else:
                return #если своя карта
        else:
            return #если тут вообще нет карты
class Pegasus(Prototype):
    def __init__(self):        
        self.name = "Pegasus"
        self.element = "life"        
        self.level = 6
        self.power = 6
        self.health = 15
        self.info = "When summoned, each owner`s creature is healed for 3. Also, it destroys harmful spell effects from each of them. CAST: Holy Strike deals 5 damage to a target creature. If it is undead creature, Pegasus also suffer 3 damage homself. Costs 2 Life."
        self.cast = True
        self.focus_cast = True
        self.image = pygame.image.load('misc/cards/life/pegasus.gif')
        Prototype.__init__(self)
    def summon(self):
        Prototype.summon(self)
        for card in self.get_self_cards():
            card.heal(3, card.max_health)
    def cast_action(self):
        if self.parent.player.life_mana >= 2: # если хватает маны
            Prototype.cast_action(self) #включаем фокус-каст
            for card in self.get_enemy_cards(): #включаем подсветку
                card.light_switch(True)
    def focus_cast_action(self, target):
        if target.name != "player": #если мы кликнули по карте, а не пустому боксу
            if target.parent.player.id != self.parent.player.id: #если карта чужая( Убивать своих не хорошо)
                if target.element == "death": #если стихия карты - смерть
                    target.damage(5, self) #наносим урон ей
                    self.damage(3, self) # и себе
                else: #если любой другой стихии
                    target.damage(5, self) #наносим урон ей
                self.used_cast = True #отмечаем, что заклинание уже использовано
                globals.cast_focus = False #отключаем фокус-каст
                self.parent.player.life_mana -= 2 # отнимаем ману
                self.play_cast_sound() #играем звук
                for card in self.get_enemy_cards(): #отключаем подсветку
                    card.light_switch(False)
            else:
                return
        else:
            return
class Unicorn(Prototype):
    def __init__(self):        
        self.name = "Unicorn"
        self.element = "life"        
        self.level = 9
        self.power = 8
        self.cast = False
        self.info = "Unicorn reduces damage from spells to owner's creatures by 50%. Cures poison from owner's creatures. Casts Unicorn Aura. This Aura destroys useful spell effects from enemy creatures. Costs 2 Life."
        self.health = 25
        self.image = pygame.image.load('misc/cards/life/unicorn.gif')
        Prototype.__init__(self)
class Apostate(Prototype):
    def __init__(self):        
        self.name = "Apostate"
        self.element = "life"        
        self.level = 5
        self.info = "Steals 2 owner's Life and gives owner 1 Death in the beginning of owner's turn. Serves Death. Once cast, Apostate permanently turns into a Banshee. Banshee restores only 1/2 of normal health."
        self.cast = True
        self.power = 4
        self.health = 14
        self.image = pygame.image.load('misc/cards/life/apostate.gif')
        Prototype.__init__(self)
    def turn(self):
        Prototype.turn(self)
        if self.parent.player.life_mana >= 2:
            self.parent.player.life_mana -= 2
        else:
            self.parent.player.life_mana = 0
        self.parent.player.death_mana += 1
    def cast_action(self):
        card = Banshee()
        card.parent = self.parent
        card.field = True
        card.health = card.health / 2
        self.parent.card = card
        self.kill()
        if self.parent.player.id == 1:
            globals.ccards_1.add(self.parent.card)
        else:
            globals.ccards_2.add(self.parent.card)
class MagicHealer(Prototype):
    def __init__(self):        
        self.name = "MagicHealer"
        self.info = "Whenever owner player loses health, Magic Healer health player by this amount, losing hit points equally."
        self.element = "life"        
        self.level = 3
        self.power = 2
        self.cast = False
        self.health = 10
        self.security_slots = []
        self.image = pygame.image.load('misc/cards/life/magic_healer.gif')
        Prototype.__init__(self)
    def summon(self):
        for cardbox in self.get_self_cardboxes():
            if cardbox.card.name == "player":
                cardbox.card = MagicHealerChakra(self)
                cardbox.card.parent = cardbox
                self.security_slots.append(cardbox)
    def card_summoned(self, card):
        if card.parent.player.id == self.parent.player.id:
            for slot in self.security_slots:
                if slot.position == card.parent.position:
                    self.security_slots.remove(slot)
    def card_died(self, card):
        if card.parent.player.id == self.parent.player.id:
            card.parent.card = MagicHealerChakra(self)
            self.security_slots.append(cardbox)
    def die(self):
        for slot in self.security_slots:
            slot.card.die()
        self.security_slots = []
        Prototype.die(self)
class MagicHealerChakra(Prototype):
    def __init__(self, owner):
        self.name = "player"
        self.level = 0
        self.element = "life"
        self.power = 0
        self.health = 10
        self.owner = owner
        self.image = pygame.image.load('misc/cards/life/magic_healer.gif')
        Prototype.__init__(self)
    def die(self):
        self.parent.card = self.parent.player
        del self
    def attack(self):
        return
    def damage(self, damage, enemy, cast=False):
        self.owner.damage(damage, enemy, cast)
class Chimera(Prototype):
    def __init__(self):        
        self.name = "Chimera"
        self.element = "life"
        self.info = "When Chimera is on a field, every spell casting costs 50% less for the owner. Whenever you summon creature, you gain health equal to this creature's level."
        self.level = 11
        self.power = 11
        self.cast = False
        self.health = 30
        self.image = pygame.image.load('misc/cards/life/chimera.gif')
        Prototype.__init__(self)
    def card_summoned(self, card):
        if self.parent.player.id == card.parent.player.id: #if it`s my card
            if card != self:
                self.parent.player.heal(card.level)
class Zombie(Prototype):
    def __init__(self):        
        self.name = "Zombie"        
        self.element = "death"
        self.level = 4
        self.power = 3
        self.health = 11
        self.info = "Eats enemies corpses - every time if kills enemy creature, totally health and his health increases by 3."
        self.cast = False
        self.image = pygame.image.load('misc/cards/death/zombie.gif')
        Prototype.__init__(self)
    def enemy_die(self):
        self.max_health += 3
        self.health = self.max_health
        self.update()
class Ghost(Prototype):
    def __init__(self):        
        self.name = "Ghost"
        self.element = "death"
        self.info = "Whenever attacked by a creature, suffers 50% less damage, and owner suffers other 50% damage. When suffers from spell, Ghost recieves 200% of normal damage. Casts Bloody Ritual. As a result, owner loses 5 health, but receives one Death."
        self.level = 3
        self.cast = True
        self.power = 3
        self.health = 13
        self.image = pygame.image.load('misc/cards/death/ghost.gif')
        Prototype.__init__(self)
    def damage(self, damage, enemy, cast = False):
        if not cast:
            Prototype.damage(self, int(ceil(damage / floor(2))), enemy)
            self.parent.player.damage(int(ceil(damage / floor(2))), enemy)
        else:
            Prototype.damage(self, damage * 2, enemy, True)
    def cast_action(self):
        self.parent.player.death_mana += 1
        self.parent.player.health -= 5
        self.used_cast = True
        self.play_cast_sound()
class Vampire(Prototype):
    def __init__(self):        
        self.name = "Vampire"
        self.element = "death"        
        self.level = 9
        self.power = 6
        self.health = 22
        self.cast = False
        self.info = "When attacks living creature, restores health equal to 50% of damage dealt. Maximum 30 health."
        self.image = pygame.image.load('misc/cards/death/vampire.gif')
        Prototype.__init__(self)
    def attack(self):
        attack_position = self.get_attack_position()
        if globals.cardboxes[attack_position].card.name != "player":
            if globals.cardboxes[attack_position].card.element != "death":
                self.health(ceil(float(self.power / 2)), 30)
        globals.cardboxes[attack_position].card.damage(self.power, self)
class Werewolf(Prototype):
    def __init__(self):        
        self.name = "Werewolf"
        self.cast = True
        self.element = "death"
        self.level = 6
        self.power = 6
        self.info = "When dies, becomes a ghost. CAST: Casts Blood Rage on self. Strikes twice as hard this turn, but owner loses 3 Death points on casting."
        self.health = 16
        self.image = pygame.image.load('misc/cards/death/werewolf.gif')
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
            globals.ccards_1.add(self.parent.card)
        else:
            globals.ccards_2.add(self.parent.card)
    def cast_action(self):
        if self.parent.player.death_mana >= 3:
            self.used_cast = True
            self.parent.player.death_mana -= 3
            self.power *= 2
class Banshee(Prototype):
    def __init__(self):
        #self.field = field
        self.name = "Banshee"        
        self.element = "death"
        self.info = "When summoned, deals 8 damage to enemy. Once it attacks enemy player, dies and enemy player suffers 10 points of extra damage. If Banshee dies from other creature or spell, enemy player doesn't suffer."
        self.level = 7
        self.cast = False
        self.power = 5
        self.health = 12
        self.image = pygame.image.load('misc/cards/death/banshee.gif')
        Prototype.__init__(self)
    def attack(self):
        if self.moves_alive:
            if globals.cardboxes[self.get_attack_position()].card.name == "player":
                globals.cardboxes[self.get_attack_position()].card.damage(self.power + 10, self)
                self.die()
            else:
                Prototype.attack(self)
    def summon(self):
        Prototype.summon(self)
        self.parent.player.enemy.damage(8, self)
class GrimReaper(Prototype):
    def __init__(self):                
        self.name = "GrimReaper"
        self.info = "Whenever creature dies, increases owner`s Death by one. CAST: Consumes target enemy creature of level 3 or less. Owner player loses 3 Death elements."
        self.element = "death"
        self.level = 12
        self.power = 8
        self.cast = True
        self.focus_cast = True
        self.health = 22
        self.image = pygame.image.load('misc/cards/death/grim_reaper.gif')
        Prototype.__init__(self)
    def cast_action(self):
        if self.parent.player.death_mana >= 3:
            Prototype.cast_action(self)
            for card in self.get_enemy_cards():
                if card.level <= 3:
                    card.light_switch(True)
    def focus_cast_action(self, target):
        if target.name != 'player': #if it is real card!
            if self.parent.player.id != target.parent.player.id:
                self.play_cast_sound()
                self.parent.player.death_mana -= 3
                target.die()
                self.used_cast = True
                globals.cast_focus = False
                for card in self.get_enemy_cards():
                    card.light_switch(False)
        else:
            return
class Darklord(Prototype):
    def __init__(self):        
        self.name = "Darklord"
        self.element = "death"
        self.info = "Whenever creature dies, Darklord heals owner for 3 and regenerates self for 2. Steal Spell steals all spell effects from any enemy creature, DarkLord receives these spells. Owner loses 1 Death."
        self.level = 8
        self.power = 4
        self.cast = False
        self.health = 14
        self.image = pygame.image.load('misc/cards/death/darklord.gif')
        Prototype.__init__(self)
    def card_died(self, card):
        self.heal(2, self.max_health)
        self.parent.player.heal(3)
class Lich(Prototype):
    def __init__(self):        
        self.name = "Lich"
        self.element = "death"        
        self.level = 10
        self.info = "When summoned,deals 10 damage to creature in the opposite slot and two adjacent slots. Attacks Life units with additionial 5 damage. CAST:Casts Death Bolt, hitting enemy player with 7 of damage. Owner loses 5 Death. If owner`s Death becomes zero, he suffers 10 damage himself."
        self.cast = False
        self.power = 7
        self.health = 18
        self.image = pygame.image.load('misc/cards/death/lich.gif')
        Prototype.__init__(self)
    def summon(self):
        Prototype.summon(self)
        attack_position = self.get_attack_position()
        globals.cardboxes[attack_position].card.damage(10, self)
        for adjacent_pos in self.get_attack_adjacent_position(attack_position):
            globals.cardboxes[adjacent_pos].card.damage(10, self)
    def attack(self):
        if self.moves_alive:
            attack_position = self.get_attack_position()
            if globals.cardboxes[attack_position].card.element == "life":
                globals.cardboxes[attack_position].card.damage(self.power + 5, self)
            else:
                globals.cardboxes[attack_position].card.damage(self.power, self)
        else:
            return
#МАГИЯ
#**************************************************************************************************************
#--------------------------------------------------------------------------------------------------------------
#1728378w7dsfhdshuifedhsghfgfhdsghjsdgfhdsgdfyugdhsghfgdhsghjlfdsghgsdujhadhujgghsdgfs
#_____________________________________________________________________________________________________________
class Magic(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.type = "magic_card"
        self.magic = True
        #self.image = ""
        self.field = False
        self.image = self.image.convert_alpha()
        self.surface_backup = self.image.copy()
        self.font = pygame.font.Font(None, 19)
        self.cards = []
        if self.element == "death" or self.element == "fire" or self.element == "earth":
            self.font_color = (255, 255, 255)
        else:
            self.font_color = (0, 0, 0)
        try:
            self.info
        except AttributeError:
            self.info = ""
    def cast(self):
        pass
    def unset(self, card):
        self.cards.remove(card)
    def set(self, card):
        self.cards.append(card)
    def get_enemy_cards(self):
        cards = []
        if self.player.id == 1:
            for cardbox in globals.cardboxes[5:10]:
                if cardbox.card.name != "player": #если есть карта
                    cards.append(cardbox.card)
        else:
            for cardbox in globals.cardboxes[0:5]:
                if cardbox.card.name != "player":
                    cards.append(cardbox.card)
        return cards
    def get_self_cards(self):
        cards = []
        if self.player.id == 1:
            for cardbox in globals.cardboxes[0:5]:
                if cardbox.card.name != "player": #если есть карта
                    cards.append(cardbox.card)
        else:
            for cardbox in globals.cardboxes[5:10]:
                if cardbox.card.name != "player":
                    cards.append(cardbox.card)
        return cards
    def periodical_cast(self):
        pass
    def update(self): #Field - True если рисовать на поле, false - если рисовать в таблице выбора
        text_level = globals.font.render(str(self.level), True, self.font_color)
        self.image = self.surface_backup.copy()
        self.image.blit(text_level, (85, 0))
        if not self.field: #Рисование в колоде
            self.parent = globals.background
            if globals.cardofelementsshower.first_part:
                xshift = 389 + self.position_in_deck * self.image.get_size()[0] + globals.cardofelementsshower.shift * self.position_in_deck
            else:
                xshift = 389 + (self.position_in_deck - 1) * self.image.get_size()[0] + globals.cardofelementsshower.shift * (self.position_in_deck - 1)
            yshift = 436
            self.parent.blit(self.image, (xshift, yshift))
            self.rect = self.image.get_rect()
            self.rect = self.rect.move(xshift, yshift)
        else:
            self.parent.image.blit(self.image, (0, 0))
class Poison(Magic):
    def __init__(self):
        self.element = "water"
        self.name = "Poison"
        self.level = 3
        self.image = pygame.image.load('misc/cards/water/poison.gif')
        self.info = "Poisons all enemy units so that they lose health every turn, also hits them with 1 damage. Posion doesn`t affect undead."
        Magic.__init__(self)
        #Каждый ход отнимает у карты противника по 1 здоровью. Не действует на класс смерти
    def cast(self):
        self.cards = self.get_enemy_cards() #берем "слепок" вражеских карт, которые будем травить
        for card in self.cards:
            card.spells.append(self) #говорим карте чтобы она начала креститься
        globals.magic_cards.add(self) #добавляем периодизацию        
    def periodical_cast(self):
        if self.cards: #если еще остались карты, на которые надо действовать
            if self.player.id != globals.player.id: #если начался вражеский ход
                for card in self.cards:
                    card.damage(1, self) #раним карту
        else: #если кпд магии будет 0
            self.kill() #прекращаем действие магии
        #P.S. неувязочка в алгоритме таки. Карта выкидывается из группы, только если карта её убьет. Если карту убьет другая карта, то эта карта останется в памяти магии , что заставит её работать с КПД 0
        #Возможное решение: {{Вроде FIXED}}
        #Прописать в прототип боевой карты массив, в котором будут храниться спеллы, наложенные на карту. После своей смерти, карта разошлет магическим обработчикам сообщения о своей смерти и они смогут очиститься.
class SeaJustice(Magic):
    def __init__(self):
        self.element = "water"
        self.name = "SeaJustice"
        self.level = 3
        self.info = "It`s magic card called SeaJustice. Try It!"
        self.image = pygame.image.load('misc/cards/water/sea_justice.gif')
        Magic.__init__(self)
        #Атакует каждую карту противника с силой равной силе карты-1
    def cast(self):
        #работает единожды, поэтому нет нужды добавлять в группу и создавать ф-ию периодического каста.
        enemy_cards = self.get_enemy_cards() #берем список вражеских карт
        for card in enemy_cards:
            card.damage(card.power, self)
class Paralyze(Magic):
    def __init__(self):
        self.element = "water"
        self.name = "Paralyze"
        self.level = 10
        self.image = pygame.image.load('misc/cards/water/paralyze.gif')
        self.info = "Vasya nakakal v shtani!"
        Magic.__init__(self)
        #противник пропускает ход
    def cast(self):
        globals.magic_cards.add(self) #добавляем периодизацию
    def periodical_cast(self):
        if self.player.id != globals.player.id:
            player.finish_turn()
            self.kill()
class AcidStorm(Magic):
    def __init__(self):
        self.element = "water"
        self.name = "AcidStorm"
        self.level = 9
        self.image = pygame.image.load('misc/cards/water/acid_storm.gif')
        self.info = "Each creature suffers up to 16 points of damage. If a player has Poseidon on a field, his creatures left unaffected. Amazingly poisonous magic storm, has no mercy to both friends and foes."
        Magic.__init__(self)
    def cast(self):
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
            card.damage(16, self)
        #предварительный перевод
        #каждое существо на поле получает 16 повреждения. Если игрок(какой ? ) имеет посейдона на поле, то его карты остаются нетронутыми.
class IceBolt(Magic):
    def __init__(self):
        self.element = "water"
        self.name = "IceBolt"
        self.level = 7
        self.image = pygame.image.load('misc/cards/water/ice_bolt.gif')
        self.info = "Inflicts 10 + Water/2 damage to enemy player. Caster suffers 6 damage as a side effect. Large bolt of Ice, fired at a great speed. Superior efficiency"
        Magic.__init__(self)
    def cast(self):
        self.player.enemy.damage((self.player.water_mana + self.level) / 2, self)
        self.player.damage(6, self)
        self.player.water_mana = 0
        #наносится урон 10+Water/2 вражескому игроку . Игроку, кто кастовал урон 6.
class Armageddon(Magic):
    def __init__(self):
        self.element = "fire"
        self.name = "Armageddon"
        self.level = 11
        self.image = pygame.image.load('misc/cards/fire/armageddon.gif')
        self.info = "All units on a field suffer 25 damage. Each player suffers 25 damage. The ultimate spell of the game. The strongest and most harmful. Beware, it's far too powerful!"
        Magic.__init__(self)
    def cast(self):
        enemy_cards = self.get_enemy_cards()
        self_cards = self.get_self_cards()
        for card in enemy_cards + self_cards:
            card.damage(25, self)
        self.player.damage(25, self)
        self.player.enemy.damage(25, self)
class Fireball(Magic):
    def __init__(self):
        self.element = "fire"
        self.name = "Fireball"
        self.level = 8
        self.image = pygame.image.load('misc/cards/fire/fireball.gif')
        self.info = "Each enemy creature suffers damage equal to owner's Fire + 3. As easy as it is - a ball of burning fire."
        Magic.__init__(self)
    def cast(self):
        enemy_cards = self.get_enemy_cards()
        for card in enemy_cards:
            card.damage(self.player.fire_mana + self.level + 3, self)
class FireSpikes(Magic):
    def __init__(self):
        self.element = "fire"
        self.name = "FireSpikes"
        self.level = 3
        self.image = pygame.image.load('misc/cards/fire/fire_spikes.gif')
        self.info = "Deals 3 damage to each enemy creature. Cheap and still good. Pure Fire."
        Magic.__init__(self)
    def cast(self):
        for card in self.get_enemy_cards():
            card.damage(3, self)
class FlamingArrow(Magic):
    def __init__(self):
        self.element = "fire"
        self.name = "FlamingArrow"
        self.level = 4
        self.image = pygame.image.load('misc/cards/fire/flaming_arrow.gif')
        self.info = "If enemy has less Fire than owner does, enemy suffers damage, equal to this difference, multiplied by 2. Otherwise enemy suffers 1 damage. Now this is a smart one - a magic arrow made of pure Fire, never misses your foe."
        Magic.__init__(self)
    def cast(self):
        diff = self.player.fire_mana + self.level - self.player.enemy.fire_mana
        if diff > 0:
            self.player.enemy.damage(diff * 2, self)
        else:
            self.player.enemy.damage(1, self)
class RitualFlame(Magic):
    def __init__(self):
        self.element = "fire"
        self.name = "RitualFlame"
        self.level = 5
        self.image = pygame.image.load('misc/cards/fire/ritual_flame.gif')
        self.info = "Destroys all spell effects from all creatures, both owner's and enemy's. Heals all Fire creatures for 3."
        Magic.__init__(self)
    def cast(self):
        for card in self.get_enemy_cards() + self.get_self_cards():
            for spell in card.spells:
                spell.unset(card)
            card.spells = []
            if card.element == 'fire':
                card.heal(3, card.max_health)
class BlackWind(Magic):
    def __init__(self):
        self.element = "air"
        self.name = "BlackWind"
        self.level = 8
        self.image = pygame.image.load('misc/cards/air/black_wind.gif')
        self.info = "Winds away strongest enemy creature. Perfect against high-level enemy creatures. One of the most useful spells."
        Magic.__init__(self)
    def cast(self):
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
        self.image = pygame.image.load('misc/cards/air/chain_lightning.gif')
        self.info = "First enemy creature suffers damage equal to owner's Air+2. Lightning travels forth and hits each enemy creature, losing 2 damage each time it hits. For example, if owner has 10 Air and enemy has all 5 creatures, they suffer this damage (left to right): 12-10-8-6-4"
        Magic.__init__(self)
    def cast(self):
        air_mana = self.player.air_mana + self.level
        power = air_mana + 2
        for card in self.get_enemy_cards():
            card.damage(power, self)
            power -= 2
class Plague(Magic):
    def __init__(self):
        self.element = "air"
        self.name = "Plague"
        self.level = 12
        self.image = pygame.image.load('misc/cards/air/plague.gif')
        self.info = "Every creature on a field plagued - loses all hit points except one. Ignores all defences and modifiers. None shall escape the Plague! Great lands burnt to dust where the plague passed."
        Magic.__init__(self)
    def cast(self):
        cards = self.get_enemy_cards() + self.get_self_cards()
        for card in cards:
            card.set_health(1)
class Spellbreaker(Magic):
    def __init__(self):
        self.element = "air"
        self.name = "Spellbreaker"
        self.level = 7
        self.image = pygame.image.load('misc/cards/air/spellbreaker.gif')
        self.info = "Owner's creatures become permanently immune to all damaging spells, spell effects, and poison. Remember that your creatures can no longer be affected by Bless, Restructure and other good spell effects."
        Magic.__init__(self)
class AbsoluteDefence(Magic): 
    def __init__(self):
        self.element = "earth"
        self.name = "AbsoluteDefence"
        self.level = 7
        self.image = pygame.image.load('misc/cards/earth/absolute_defence.gif')
        self.info = "Owner's creatures gain protection from all attacks. This defence only lasts one turn and lasts till next owner's turn. It's just like an unpenetrable wall has suddenly appeared. Anyone under your command will survive anything!"
        Magic.__init__(self)
class Earthquake(Magic):
    def __init__(self):
        self.element = "earth"
        self.name = "Earthquake"
        self.level = 10
        self.image = pygame.image.load('misc/cards/earth/earthquake.gif')
        self.info = "Hits each creature for 15 damage. Doesn't affect owner's creatures, if onwer's Earth > 12. Even the earth itself is a powerful weapon."
        Magic.__init__(self)
    def cast(self):
        earth_mana = self.player.earth_mana + self.level
        if earth_mana > 12:
            cards = self.get_enemy_cards()
        else:
            cards = self.get_enemy_cards() + self.get_self_cards()
        for card in cards:
            card.damage(15, self)
class Quicksands(Magic):
    def __init__(self):
        self.element = "earth"
        self.name = "Quicksands"
        self.level = 6
        self.image = pygame.image.load('misc/cards/earth/quicksands.gif')
        self.info = "Kills all enemy creatures of level less than 5. Only the skilled one can survive the swamp's most dangerous weapon."
        Magic.__init__(self)
    def cast(self):
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
        self.image = pygame.image.load('misc/cards/earth/restructure.gif')
        self.info = "All onwer's creatures gain +3 health to their maximum, healing for 6 in the same time. Scatter to pieces, connect once again. Now you are stronger, none shall remain!"
        Magic.__init__(self)
    def cast(self):
        for card in self.get_self_cards():
            card.max_health += 3
            card.heal(6, card.max_health)
class Revival(Magic):
    def __init__(self):
        self.element = "earth"
        self.name = "Revival"
        self.level = 5
        self.image = pygame.image.load('misc/cards/earth/revival.gif')
        self.info = "Heals all friendly creatures for 4. Gives owner 2 health for each of his creatures on a field. Heal me! Heal me!"
        Magic.__init__(self)
    def cast(self):
        for card in self.get_self_cards():
            card.heal(4, card.max_health)
            self.player.heal(2)
class Bless(Magic): 
    def __init__(self):
        self.element = "life"
        self.name = "Bless"
        self.level = 5
        self.image = pygame.image.load('misc/cards/life/bless.gif')
        self.info = "All owner's creatures Blessed: receive +1 to attack, restore 1 point of health every time they are hit. Undead creatures cannot be blessed and suffer 10 damage instead. Your army's now under God's protection, and your enemy is doomed forever!"
        Magic.__init__(self)
    def cast(self):
        cards = self.get_self_cards()
        for card in cards:
            if card.element != 'death':
                card.set_power(card.power + 1)
                self.cards.append(card)
            else:
                card.damage(10, self)
    def periodical_cast(self):
        if self.cards: #if has cards
            if self.player.id != globals.player.id: #if enemy turn started
                for card in self.cards:
                    card.heal(1, card.max_health)
        else:
            self.kill()
class GodsWrath(Magic):
    def __init__(self):
        self.element = "life"
        self.name = "GodsWrath"
        self.level = 10
        self.image = pygame.image.load('misc/cards/life/gods_wrath.gif')
        self.info = "All undead on a field are destroyed. Owner receives 3 Life and 1 health for each destroyed creature. The great day of $The Lord ^is near and coming quickly. That day will be a day of $Wrath, ^a day of distress and anguish."
        Magic.__init__(self)
    def cast(self):
        cards = self.get_enemy_cards() + self.get_self_cards()
        for card in cards:
            if card.element == "death":
                card.die()
                self.player.life_mana += 3
                self.player.heal(1)
class LifeSacrifice(Magic):
    def __init__(self):
        self.element = "life"
        self.name = "LifeSacrifice"
        self.level = 8
        self.image = pygame.image.load('misc/cards/life/life_sacrifice.gif')
        self.info = "Owner loses health equal to his $Life. ^Enemy suffers damage, double of this amount. Sacrificing is the true loving act."
        Magic.__init__(self)
    def cast(self):
        power = self.player.life_mana + self.level
        self.player.damage(power, self)
        self.player.enemy.damage(power * 2, self)
class Purify(Magic):
    def __init__(self):
        self.element = "life"
        self.name = "Purify"
        self.level = 7
        self.image = pygame.image.load('misc/cards/life/purify.gif')
        self.info = "If owner has Life creatures in play, heals owner for 5 and steals 4 health from each enemy creature, giving them to opposed owner's creature. Only pure souls can use God's blessings."
        Magic.__init__(self)
    def cast(self):
        has_life = False
        for card in self.get_self_cards():
            if card.element == 'life':
                has_life = True
        if has_life:
            self.player.heal(5)
            for e_card in self.get_enemy_cards():
                opp_card = globals.cardboxes[e_card.get_attack_position()].card
                if opp_card.name != 'player': #if card in opposed slot exist
                    e_card.damage(4, self)
                    opp_card.heal(4, opp_card.max_health)
                else:
                    e_card.damage(4, self)
        else:
            return

class Rejuvenation(Magic):
    def __init__(self):
        self.element = "life"
        self.name = "Rejuvenation"
        self.level = 6
        self.image = pygame.image.load('misc/cards/life/rejuvenation.gif')
        self.info = "Heals owner equal to his Life*3. Owner loses all Life elements. Blessed creatures heal for 3. Now you live again, mortal. Life is the most precious, be careful next time!"
        Magic.__init__(self)
    def cast(self):
        life_mana = globals.player.life_mana + self.level
        globals.player.heal(life_mana * 3)
        for card in self.get_self_cards():
            card.heal(3, card.max_health)
        globals.player.life_mana = 0
class ChaosVortex(Magic):
    def __init__(self):
        self.element = "death"
        self.name = "ChaosVortex"
        self.level = 13
        self.image = pygame.image.load('misc/cards/death/chaos_vortex.gif')
        self.info = "Banishes each creature into hell. Each banished creature gives caster 1 Death. Whenever one unfolds Chaos, no mortal can stand its fearful ugly nature."
        Magic.__init__(self)
    def cast(self):
        cards = self.get_enemy_cards() + self.get_self_cards()
        self.player.death_mana += len(cards)
        for card in cards:
            card.die()
class CoverOfDarkness(Magic):
    def __init__(self):
        self.element = "death"
        self.name = "CoverOfDarkness"
        self.level = 11
        self.image = pygame.image.load('misc/cards/death/cover_of_darkness.gif')
        self.info = "All living creatures suffer 13 damage. All undead creatures heal for 5. The Lord of Chaos most useful tool. Your army of darkness shall reign forever."
        Magic.__init__(self)
    def cast(self):
        cards = self.get_enemy_cards() + self.get_self_cards()
        for card in cards:
            if card.element == "death":
                card.heal(5, card.max_health)
            else:
                card.damage(13, self)
class Curse(Magic): 
    def __init__(self):
        self.element = "death"
        self.name = "Curse"
        self.level = 4
        self.image = pygame.image.load('misc/cards/death/curse.gif')
        self.info = "Reduces all enemy elements by 1. Curse and Doom are now your enemy's only guests."
        Magic.__init__(self)
    def cast(self):
        if globals.player.enemy.water_mana:
            globals.player.enemy.water_mana -= 1
        if globals.player.enemy.fire_mana:
            globals.player.enemy.fire_mana -= 1
        if globals.player.enemy.air_mana:
            globals.player.enemy.air_mana -= 1
        if globals.player.enemy.earth_mana:
            globals.player.enemy.earth_mana -= 1
        if globals.player.enemy.life_mana:
            globals.player.enemy.life_mana -= 1
        if globals.player.enemy.death_mana:
            globals.player.enemy.death_mana -= 1
class StealLife(Magic):
    def __init__(self):
        self.element = "death"
        self.name = "StealLife"
        self.level = 6
        self.image = pygame.image.load('misc/cards/death/steal_life.gif')
        self.info = "If owner's Death less than 8, steals 5 health from enemy player. Otherwise steals Death + 5. Death's cold vampiric touch. So painful and surreal.."
        Magic.__init__(self)
    def cast(self):
        death_mana = globals.player.death_mana + self.level
        if death_mana < 8:
            globals.player.enemy.damage(5, self)
            globals.player.heal(5)
        else:
            globals.player.enemy.damage(death_mana + 5, self)
            globals.player.heal(death_mana + 5)
class TotalWeakness(Magic):
    def __init__(self):
        self.element = "death"
        self.name = "TotalWeakness"
        self.level = 8
        self.image = pygame.image.load('misc/cards/death/total_weakness.gif')
        self.info = " Every enemy creature suffers effect of Weakness: its attack decreased by 50% (rounded down). Make the strongest the weakest, and then assasinate him."
        Magic.__init__(self)
    def cast(self):
        cards = self.get_enemy_cards()
        for card in cards:
            card.default_power = int(floor(card.power / 2.0))
            card.set_power(int(floor(card.power / 2.0)))