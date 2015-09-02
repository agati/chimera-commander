#! /usr/bin/env python
# -*- coding: iso-8859-1 -*-
# chimera - observatory automation system
# Copyright (C) 2006-2015  P. Henrique Silva <henrique@astro.ufsc.br>
# Copyright (C) 2015  Salvador Sergi Agati <salvadoragati@gmail.com>
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301, USA.
# *****************************************************************************************
# processo nº 2015/06983-1 Fundação de Amparo à Pesquisa do Estado de São Paulo (FAPESP). *
# As opiniões, hipóteses e # conclusões ou recomendações expressas neste material são    *
# de responsabilidade do(s) autor(es) e não necessariamente refletem a visão da FAPESP.  *
#grant #2015/06983-1, São Paulo Research Foundation (FAPESP).                            *
#Opinions, assumptions and conclusions or recommendations expressed in this material are *
#responsibility of the (s) author (s) and do not necessarily reflect the views of FAPESP.*
#*****************************************************************************************
# *******************************************************************
# This driver is intended to be used with the Emerson Commander SK  *
# order number SKBD200110 -  salvadoragati@gmail.com                *
# start:15/06/2015 - last update: 19/08/2015                        *
#********************************************************************
#The initial menu is configured to manage two controllers:
#
#1-IP:192.168.30.104 - Eastern fan system
#2-IP:192.168.30.105 - Western fan system



import os

from chimera_commander.instruments.skdrv import SKDrv


def controller_menu():
    """
    Here i where you choose the controller to be managed.
    You can add as many controllers as you need in the following menu.
    """
    os.system('cls' if os.name == 'nt' else 'clear')
    ip = ''


    print "***************************************"
    print "*** Commander SK Controller Menu ******"
    print "***************************************"

    print"Choose the controller number :"
    print""
    print "1-IP:192.168.30.104 - Eastern"
    print "2-IP:192.168.30.105 - Western"
    print "3-Exit"
    key = raw_input("Choice (1/2/3):")
    if key == '1':
        ip = '192.168.30.104'
        return ip
    if key == '2':
        ip = '192.168.30.105'
        return ip
    if key == '3':
        return ip


def command_menu(ip, sk):
    os.system('cls' if os.name == 'nt' else 'clear')
    while 1:
        print "***************************************"
        print "***  Commander SK Command Menu   ******"
        print "***************************************"
        print " ip: ", ip
        print "1-Remote Reset"
        print "2-Check Basics "
        print "3-Check Rotation"
        print "4-Enable Remote Control"
        print "5-Run Forward"
        print "6-Stop"
        print "7-Disable Remote Control"
        print "8-Controller Menu"

        action = raw_input("Choice (1/2/3/4/5/6/7/8):")
        if action == '1':
            os.system('cls' if os.name == 'nt' else 'clear')
            print " ip: ", ip
            sk.reset()

        if action == '2':
            os.system('cls' if os.name == 'nt' else 'clear')
            print " ip: ", ip
            sk.check_basic()

        if action == '3':
            os.system('cls' if os.name == 'nt' else 'clear')
            print " ip: ", ip
            sk.check_rotation()

        if action == '4':
            os.system('cls' if os.name == 'nt' else 'clear')
            print " ip: ", ip
            sk.enableCW()

        if action == '5':
            os.system('cls' if os.name == 'nt' else 'clear')
            print " ip: ", ip
            sk.forward()

        if action == '6':
            os.system('cls' if os.name == 'nt' else 'clear')
            print " ip: ", ip
            sk.stop()

        if action == '7':
            os.system('cls' if os.name == 'nt' else 'clear')
            print " ip: ", ip
            sk.disableCW()

        if action == '8':
            return


# end of auxiliary functions
#**************************************************************


#this is the main loop routine of the Commander SK Control Manager

while 1:
    data = 0
    os.system('cls' if os.name == 'nt' else 'clear')
    ip = controller_menu()
    if ip == '': exit()
    sk = SKDrv()
    sk.host = ip

    try:
        sk.connect()

        #check the basic parameters
        changes = sk.check_basic()
        if len(changes) > 0:
            print "Changes on basic parameters detected!:", changes
            key = raw_input("Continue anyway? (y/n)")
            if key != "y":
                sk.close()
                del sk
                exit()
        print "Basic parameters correctly configured. Starting remote configs..."
        remote_setup = sk.setup()
        if remote_setup == True:
            print "Remote parameters correctly configured. Starting the command menu..."
            command = command_menu(ip, sk)
        else:
            print"Can not set up the driver for remote control..."
            key = raw_input("Continue anyway? (y/n)")
            if key != "y":
                sk.close()
                del sk
                exit()

            command = command_menu(ip, sk)


    except Exception:
        print"Failed to connect to ip:", ip
        sk.close()
        del sk
        any_key = raw_input("Press [ENTER] to continue...")



