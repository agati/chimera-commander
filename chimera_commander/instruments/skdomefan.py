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
# views of FAPESP.                                               *
# *****************************************************************

from chimera_commander.dome import DomeFan
from chimera_commander.instruments.skdrv import SKDrv


class SKDomeFan(DomeFan, SKDrv):
    __delta_time__ = '00:00:00'  # 'hh:mm:ss'
    __local_time__ = '00:00:00'  # 'hh:mm:ss'
    __start_time__ = '00:00:00'  # 'hh:mm:ss'
    __end_time__ = '00:00:00'  # 'hh:mm:ss'
    __elapsed_time__ = '00:00:00'  # 'hh:mm:ss'
    __temperature_threshold__ = 0.0  # Celsius degrees


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
            self.log.error('Trying to set up a rotation frequency less than the minimum frequency allowed to the ',
                           self.get_fan_number(), ' fan.')
            return False
        if frequency > self.max_speed:
            self.log.error('Trying to set up a  rotation frequency above than the maximum frequency allowed to the ',
                           self.get_fan_number(), ' fan.')
            return False
        if self.write_parm('01.21', frequency):
            self.log.info('Frequency defined to ', frequency, ' rpm to the ', self.get_fan_number(), ' fan.')
            return True
        else:
            self.log.error('Could not write the frequency value of ', frequency, ' to the ', self.get_fan_number(),
                           ' fan.')
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
        if self.check_basic() and not self.is_on():
            self.log.info('Basic config is ok and the fan is not running.')
            if self.enableCW():
                self.log.info('Drive was enabled to accept remote commands.')
                if self.forward():
                    self.log.info('The motor fan run command was sent.')
                    time.sleep(1)  # waits 1 second before checking that the motor fan is running
                    if self.is_on():
                        self.log.info('The ', self.get_fan_number(), ' fan is running forward.')
                        return True
                    else:
                        self.log.error('Error on checking if the ', self.get_fan_number(), ' fan is running forward.')
                        return False
                else:
                    self.log.error('Error on sending the run forward command to the', self.get_fan_number(), 'fan.')
                    return False
            else:
                self.log.error('Error on enabling the drive remote control to the', self.get_fan_number(), 'fan.')
                return False
        else:
            self.log.error('Error on checking that the basic config is ok or on confirming that the ',
                           self.get_fan_number(), ' fan is not running.')
            return False

        return False


    def power_off(self):

        # first verifies that the drive is enable and that the fan is running
        if self.read_parm('06.43') == 1:
            self.log.info(self.get_fan_number(), ' fan is able to accept remote commands.')
            if self.stop():
                self.log.info('The stop command was sent to the ', self.get_fan_number(), ' fan.')
                time.sleep(
                    10)  # waits 10 seconds before to check if the fan is off - Need to verify if time is sufficient
                if not self.is_on():
                    self.log.info('The ', self.get_fan_number(), ' fan stopped.')
                    return True
                else:
                    self.log.error('Error on checking if the ', self.get_fan_number(), ' fan stopped.')
                    return False
            else:
                self.log.error('Error on sending the stop command to the ', self.get_fan_number(), ' fan.')
                return False
        else:
            self.log.error('Error on checking if the ', self.get_fan_number(), ' fan is enable.')
            return False


    def remoteCheck(self):
        """
        self.log.debug('')
        self.log.info('')
        self.log.warning('')
        self.log.error('')

        return 0

        """


