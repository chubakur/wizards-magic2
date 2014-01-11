import pygame
import sys
import globals
from pygame.locals import *
import ConfigParser
import os.path
from widgets import TxtInput, CheckBox
import menu
def launcher():
    #Something ,what we need to change after reset configuration
    globals.bg_sound.stop()
    if globals.music == "Y":
        globals.bg_sound.play(-1)
def save():
    config = ConfigParser.RawConfigParser()
    config.add_section('WizardsMagic')
    for item in globals.menu_group:
        if item.type=='txtinput':
            config.set('WizardsMagic', item.key, item.text)
        if item.type=='checkbox':
            config.set('WizardsMagic', item.key, (item.value and 'Y' or 'N'))
    configfile=open('wizardsmagic.cfg', 'wb')
    config.write(configfile)
    configfile.close()
    read_configuration()
    launcher()
    menu.menu_main()

def cancel(): 
    menu.menu_main()

def read_configuration():
    config = ConfigParser.ConfigParser()
    config.read('wizardsmagic.cfg')

    try:
        globals.music = config.get('WizardsMagic', 'music')
        globals.music = globals.music.upper()
        if not globals.music in "YN":
            globals.music = "Y"
    except:
        globals.music = "Y"
    try:
        globals.sound = config.get('WizardsMagic', 'sound')
        globals.sound = globals.sound.upper()
        if not globals.sound in "YN":
            globals.sound = "Y"
    except:
        globals.sound = "Y"
    try:
        globals.nick = config.get('WizardsMagic', 'nick')
    except:
        globals.nick = "myname"
    try:
        globals.server = config.get('WizardsMagic', 'server')
    except:
        globals.server = "127.0.0.1"
    try:
        globals.port = config.getint('WizardsMagic', 'port')
        if globals.port<=0 or globals.port>65535:
            globals.port = 7712
        globals.port = str(globals.port)
    except:
        globals.port = "7712"

def options_main(): 
    ''' display options menu '''

    globals.menu_group.empty()
    globals.background = pygame.image.load('misc/menu_bg.jpg').convert_alpha()
    globals.background_backup = globals.background.copy()
    globals.menu_bg = pygame.image.load('misc/menu_selections_bg.jpg').convert_alpha()
    menupos = globals.menu_bg.get_rect()
    menupos.centerx = globals.background.get_rect().centerx -2 # '-2' hack due lazy designer :)
    menupos.centery = globals.background.get_rect().centery -1 # '-1' hack due lazy designer :)
    globals.background.blit(globals.menu_bg, menupos)

    #Configuration file:
    #create default configuration file
    if not os.path.isfile('wizardsmagic.cfg'):
        config = ConfigParser.RawConfigParser()
        config.add_section('WizardsMagic')
        config.set('WizardsMagic', 'music', 'Y')
        config.set('WizardsMagic', 'sound', 'Y')
        config.set('WizardsMagic', 'nick', 'myname')
        config.set('WizardsMagic', 'server', '127.0.0.1')
        config.set('WizardsMagic', 'port', '7712')
        configfile = open('wizardsmagic.cfg', 'wb')
        config.write(configfile)
        configfile.close()

    #read configuration file
    read_configuration()

    option1 = CheckBox(0,"MUSIC:", (globals.music == 'Y'), key="music")
    option1 = CheckBox(1,"SOUNDS:", (globals.sound == 'Y'), key="sound")
    option2 = TxtInput(2,"NICK:", globals.nick, 8, key="nick")
    option3 = TxtInput(3,"SERVER:", globals.server, 15, key="server")
    option4 = TxtInput(4,"PORT:", globals.port, 5, key="port")
    option5 = menu.MenuButton(-1, "SAVE", "options.save()", loc=(70, menupos.height-50))
    option6 = menu.MenuButton(-1, "CANCEL", "options.cancel()", loc=(160, menupos.height-50))
    globals.menu_group.update()

