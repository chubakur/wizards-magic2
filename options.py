#Wizards Magic
#Copyright (C) 2011-2014  https://code.google.com/p/wizards-magic/
#This program is free software; you can redistribute it and/or
#modify it under the terms of the GNU General Public License
#as published by the Free Software Foundation; either version 2
#of the License, or (at your option) any later version.

#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.

#You should have received a copy of the GNU General Public License
#along with this program; if not, write to the Free Software
#Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
try:
    import pygame
    #from pygame.locals import *
    from widgets import TxtInput, CheckBox
    import menu
    yes_pygame = True
except ImportError:
    yes_pygame = False
import wzglobals
import ConfigParser
import os.path
def launcher():
    #Something ,what we need to change after reset configuration
    try:
        wzglobals.bg_sound.stop()
    except AttributeError:
        wzglobals.bg_sound = pygame.mixer.Sound(wzglobals.current_folder+'/misc/sounds/11_the_march_of_the_goblins__tobias_steinmann.ogg')
    if wzglobals.music == "Y":
        wzglobals.bg_sound.play(-1)
def save():
    config = ConfigParser.RawConfigParser()
    config.add_section('WizardsMagic')
    for item in wzglobals.menu_group:
        if item.type=='txtinput':
            config.set('WizardsMagic', item.key, item.text)
        if item.type=='checkbox':
            config.set('WizardsMagic', item.key, (item.value and 'Y' or 'N'))
    config.set('WizardsMagic','language',wzglobals.language)
    configfile=open(wzglobals.current_folder + '/wizardsmagic.cfg', 'wb')
    config.write(configfile)
    configfile.close()
    read_configuration()
    launcher()
    menu.menu_main()

def cancel():
    menu.menu_main()

def read_configuration():
    config = ConfigParser.ConfigParser()
    config.read(wzglobals.current_folder + '/wizardsmagic.cfg')

    try:
        wzglobals.music = config.get('WizardsMagic', 'music')
        wzglobals.music = wzglobals.music.upper()
        if not wzglobals.music in "YN":
            wzglobals.music = "Y"
    except:
        wzglobals.music = "Y"
    try:
        wzglobals.sound = config.get('WizardsMagic', 'sound')
        wzglobals.sound = wzglobals.sound.upper()
        if not wzglobals.sound in "YN":
            wzglobals.sound = "Y"
    except:
        wzglobals.sound = "Y"
    #try:
    #    wzglobals.ai = config.get('WizardsMagic', 'ai')
    #    wzglobals.ai = wzglobals.ai.upper()
    #    if not wzglobals.ai in "YN":
    #        wzglobals.ai = "Y"
    #except:
    #    wzglobals.ai = "Y"
    try:
        wzglobals.nick = config.get('WizardsMagic', 'nick')
    except:
        wzglobals.nick = "myname"
    try:
        wzglobals.server = config.get('WizardsMagic', 'server')
    except:
        wzglobals.server = "127.0.0.1"
    try:
        wzglobals.port = config.getint('WizardsMagic', 'port')
        if wzglobals.port<=0 or wzglobals.port>65535:
            wzglobals.port = 7712
        wzglobals.port = str(wzglobals.port)
    except:
        wzglobals.port = "7712"
    try:
        wzglobals.animation = config.get('WizardsMagic', 'animation')
        wzglobals.animation = wzglobals.animation.upper()
        if not wzglobals.animation in "YN":
            wzglobals.animation = "Y"
    except:
        wzglobals.animation = "Y"
    try:
        wzglobals.language
    except:
        try:
            wzglobals.language = config.get('WizardsMagic', 'language')
            wzglobals.language = wzglobals.language.lower()
            if not wzglobals.language in ['ru','en','de']:
                wzglobals.language = 'en'
        except:
            wzglobals.language = 'en'
def options_main():
    ''' display options menu '''

    wzglobals.menu_group.empty()
    wzglobals.background = pygame.image.load(wzglobals.current_folder + '/misc/menu_bg.jpg').convert_alpha()
    wzglobals.background_backup = wzglobals.background.copy()
    wzglobals.menu_bg = pygame.image.load(wzglobals.current_folder + '/misc/menu_selections_bg.jpg').convert_alpha()
    menupos = wzglobals.menu_bg.get_rect()
    menupos.centerx = wzglobals.background.get_rect().centerx -2 # '-2' hack due lazy designer :)
    menupos.centery = wzglobals.background.get_rect().centery -1 # '-1' hack due lazy designer :)
    wzglobals.background.blit(wzglobals.menu_bg, menupos)

    #Configuration file:
    #create default configuration file
    if not os.path.isfile(wzglobals.current_folder + '/wizardsmagic.cfg'):
        config = ConfigParser.RawConfigParser()
        config.add_section('WizardsMagic')
        config.set('WizardsMagic', 'music', 'Y')
        config.set('WizardsMagic', 'sound', 'Y')
        config.set('WizardsMagic', 'nick', 'myname')
        config.set('WizardsMagic', 'server', '127.0.0.1')
        config.set('WizardsMagic', 'port', '7712')
        config.set('WizardsMagic', 'language', 'en')
        #config.set('WizardsMagic', 'ai', 'Y')
        config.set('WizardsMagic', 'animation', 'Y')
        configfile = open(wzglobals.current_folder + '/wizardsmagic.cfg', 'wb')
        config.write(configfile)
        configfile.close()

    #read configuration file
    read_configuration()
    CheckBox(2,"MUSIC:", (wzglobals.music == 'Y'), key="music")
    CheckBox(1,"SOUNDS:", (wzglobals.sound == 'Y'), key="sound")
    CheckBox(0, "ANIMATION:", (wzglobals.animation == 'Y'), key='animation')
    TxtInput(3,"NICK:", wzglobals.nick, 8, key="nick")
    TxtInput(4,"SERVER:", wzglobals.server, 15, key="server")
    TxtInput(5,"PORT:", wzglobals.port, 5, key="port")
    menu.MenuButton(5, "Select language", "menu_select_language()")
    menu.MenuButton(-1, "SAVE", "options.save()", loc=(70, menupos.height-50))
    menu.MenuButton(-1, "CANCEL", "options.cancel()", loc=(160, menupos.height-50))
    wzglobals.menu_group.update()

