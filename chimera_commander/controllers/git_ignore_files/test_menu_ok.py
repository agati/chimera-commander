#! /usr/bin/env python
# -*- coding: iso-8859-1 -*-
# chimera - observatory automation system
# Copyright (C) 2006-2015  P. Henrique Silva <henrique@astro.ufsc.br>
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
# **********************************************************************#
# This program is intended to be used with the Emerson Commander SK    #
# order number SKBD200110 start: 23/07/2015 - last update:03/0811/2015 #
#**********************************************************************#



import os

from chimera_commander.instruments.skdrv import SKDrv


def controller_menu():
    # -choose controller (ip)
    os.system('cls' if os.name == 'nt' else 'clear')

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
        ip = ''

        return ip


def command_menu(ip, sk):
    os.system('cls' if os.name == 'nt' else 'clear')
    while 1:
        print "***************************************"
        print "***  Commander SK Command Menu   ******"
        print "***************************************"
        print " ip: ", ip
        print "1-Remote Reset ('10.33', 1) e ('10.33', 0)"
        print "2-Check Basics "
        print "3-Check Rotation ('05.04')"
        print "4-Enable Control Word ('06.43',1), ('06.42',128), ('06.42',129)"
        print "5-Run Forward ('06.42' , 131)"
        print "6-Stop ('06.42' , 129)"
        print "7-Run Reverse ('06.42' , 137)"
        print "8-Disable Control Word ('06.42',129), ('06.42',128), ('06.43',0)"
        print "9-Controller Menu"

        action = raw_input("Choice (1/2/3/4/5/6/7/8/9):")
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
            sk.reverse()

        if action == '8':
            os.system('cls' if os.name == 'nt' else 'clear')
            print " ip: ", ip
            sk.disableCW()

        if action == '9':
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
        print "The controller is well configured. Starting the command menu..."
        #the controller is well configured. Starting the command menu
        command = command_menu(ip, sk)




    except Exception:
        print"failed to connect to ip:", ip
        sk.close()
        del sk
        any_key = raw_input("Press [ENTER] to continue...")



