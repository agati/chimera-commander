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
# ****************************************************************
# Copyright (C) 2015 Salvador S. Agati <salvadoragati@gmail.com> *
# #grant #2015/06983-1, São Paulo Research Foundation (FAPESP).  *
# Opinions, assumptions and conclusions or recommendations       *
# expressed in this material by Salvador Sergi Agati are his     *
# responsibility and do not necessarily reflect the              *
# views of FAPESP.
# start:11/09/2015 - last update: 07/10/2015                                              *
# *****************************************************************

import os

from chimera_commander.dome import DomeFan
from chimera_commander.instruments.skdrv import SKDrv


class SKDomeFan(DomeFan, SKDrv):
    def controller_menu(self):


        """
        # -choose controller (ip)

        :return: ip
        """
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
            print""
            print "1-Check rotation"
            print "2-Run Forward"
            print "3-Stop"
            print "4-Run Reverse"
            print "5-Timer"
            print "6-Automatic Start by Temperature Treshold"
            print "7-Controller Menu"

            action = raw_input("Choice (1/2/3/4/5/6/7):")
            if action == '1':
                os.system('cls' if os.name == 'nt' else 'clear')
                print " ip: ", ip
                sk.check_rotation()

            if action == '2':
                os.system('cls' if os.name == 'nt' else 'clear')
                print " ip: ", ip
                sk.forward()

            if action == '3':
                os.system('cls' if os.name == 'nt' else 'clear')
                print " ip: ", ip
                sk.stop()

            if action == '4':
                os.system('cls' if os.name == 'nt' else 'clear')
                print " ip: ", ip
                sk.reverse()

            if action == '5':
                os.system('cls' if os.name == 'nt' else 'clear')
                print " ip: ", ip
                sk.timer()

            if action == '6':
                os.system('cls' if os.name == 'nt' else 'clear')
                print " ip: ", ip
                sk.treshold()

            if action == '7':
                return

    def __init__(self):

        self.__delta_time__ = '00:00:00'  # 'hh:mm:ss'
        self.__local_time__ = '00:00:00'  # 'hh:mm:ss'
        self.__start_time__ = '00:00:00'  # 'hh:mm:ss'
        self.__end_time__ = '00:00:00'  # 'hh:mm:ss'
        self.__elapsed_time__ = '00:00:00'  # 'hh:mm:ss'
        self.__temperature_threshold__ = 0.0  # Celsius degrees

        return

    def __start__(self):
        """




        :return:
        """

    def get_model(self):
        """
        gets the fan drive model
        """
        model = self.get_order_number()
        return model

    def get_fan_number(self):
        """
        gets the controller ip
        """
        ip = self.get_ip()
        return ip

    def get_frequency(self):
        """
        gets the fan rotation
        """
        rotation = self.check_rotation()  # rpm
        return rotation

    def set_frequency(self, frequency):
        """
        Sets the frequency (rotation in rpm) of the fan motor.
        """

        if frequency < self.min_speed:
            return False
        if frequency > self.max_speed:
            return False
        if self.write_parm('01.21', frequency):
            return True
        else:
            return False

    def get_timer(self):
        """
        Gets and returns the start and end time previously defined
        returns a list with 2 values: start_time and end_time
        """
        return [self.__start_time__, self.__end_time__]

    def set_timer(self, timer):
        """
        Sets the start_time and end_time of the timer
        todo:check if end_time>start_time date and if delta time is in valid range
        """
        self.__start_time__ = timer[0]
        self.__end_time__ = timer[1]
        return True

    def set_trigger_temp(self, temp):
        """
        Sets a threshold temperature value that turns a fan motor on.
        todo:check if the temperature and the delta_time are in their respective valid ranges
        """
        self.__temperature_threshold__ = temp[0]
        self.__delta_time__ = temp[1]
        return True

    def is_on(self):
        if self.check_rotation() > 0:
            return True
        else:
            return False

    def power_on(self):
        if self.check_basic() and not self.is_on():  # basics ok and no yet on
            if self.forward():
                time.sleep(1)  # waits 1 second before checking that the motor fan is running
                if self.is_on():
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False

    def power_off(self):

        # first verifies that the drive is enable
        if self.read_parm('06.43') == 1:  # fan is able to accept remote commands
            if self.stop():  # sent the stop command
                # time.sleep(2)  # waits 2 seconds before to check if the fan is off
                if not self.is_on():  # fan stopped.
                    return True
                else:
                    return False
            else:  # error on sending the stop command to the fan
                return False
        else:  # fan isn't able to accept remote commands
            return False


    # this is the main loop routine of the Commander SK Control Manager

    while 1:
        data = 0
        os.system('cls' if os.name == 'nt' else 'clear')
        ip = controller_menu()
        if ip == '': exit()
        sk = SKDrv()
        sk.host = ip

        try:
            sk.connect()

            # check the basic parameters
            changes = sk.check_basic()
            if len(changes) > 0:
                print "Changes on basic parameters detected!:", changes
                key = raw_input("Continue anyway? (y/n)")
                if key != "y":
                    sk.close()
                    del sk
                    exit()

            # the controller is well configured. Starting the command menu
            command = command_menu(ip, sk)




        except Exception:
            print"failed to connect to ip:", ip
            sk.close()
            del sk
            any_key = raw_input("Press [ENTER] to continue...")



