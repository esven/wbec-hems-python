#################################################################################################
#
# WBEC-HEMS-PYTHON HEMS for Heidelberg Energy Control
# Copyright (C) 2021  Sven Ebenfeld
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
#
## Description :  Initial code file for simulating a WBEC
#
## Author      :  Sven Ebenfeld
#
## Date        :  2021.09.17
#
##################################################################################################

import sys

import serial
import fcntl
import os
import struct
import termios
import array
import time

import modbus_tk
import modbus_tk.defines as cst
import modbus_tk.modbus as modbus
#import modbus_tk.modbus_rtu as modbus_rtu
from modbus_tk import modbus_rtu
from wbec import Wbec
# RS485 ioctls
TIOCGRS485 = 0x542E
TIOCSRS485 = 0x542F
SER_RS485_ENABLED = 0b00000001
SER_RS485_RTS_ON_SEND = 0b00000010
SER_RS485_RTS_AFTER_SEND = 0b00000100
SER_RS485_RX_DURING_TX = 0b00010000
# rs 485 port
ser1 = serial.Serial("/dev/ttySC0",9600)    
ser2 = serial.Serial("/dev/ttySC1",9600)

def rs485_enable():
    buf = array.array('i', [0] * 8) # flags, delaytx, delayrx, padding
    #enable 485 chanel 1
    fcntl.ioctl(ser1, TIOCGRS485, buf)
    buf[0] |=  SER_RS485_ENABLED|SER_RS485_RTS_AFTER_SEND
    buf[1]  = 0
    buf[2]  = 0
    fcntl.ioctl(ser1, TIOCSRS485, buf)

    #enable 485 chanel 2
    fcntl.ioctl(ser2, TIOCGRS485, buf)
    buf[0] |=  SER_RS485_ENABLED|SER_RS485_RTS_AFTER_SEND
    buf[1]  = 0
    buf[2]  = 0
    fcntl.ioctl(ser2, TIOCSRS485, buf)
#end of def rs485_enable():

class WbecModbus:

    def __init__(self, wallbox, rtu_follower):
        self.wallbox = wallbox
        self.rtu_follower = rtu_follower
       

if __name__ == '__main__':
    
    logger = modbus_tk.utils.create_logger("console")

    rs485_enable()
   
    logger = modbus_tk.utils.create_logger(name="console", record_format="%(message)s")

    #Create the server
    server = modbus_rtu.RtuServer(serial.Serial('/dev/ttySC1'))

    try:
        logger.info("running...")
        logger.info("enter 'quit' for closing the server")

        server.start()

        followers = array()
        followers.append(None)

        follower_1 = server.add_slave(1)
        wbmod = WbecModbus(Wbec("Wallbox 1", 1, 6, 16), follower_1)
        followers.insert(1, wbmod)
        follower_1.add_block('0', cst.HOLDING_REGISTERS, 0, 100)
        while True:
            cmd = sys.stdin.readline()
            args = cmd.split(' ')

            if cmd.find('quit') == 0:
                sys.stdout.write('bye-bye\r\n')
                break

            elif args[0] == 'add_follower':
                follower_id = int(args[1])
                server.add_slave(follower_id)
                sys.stdout.write('done: follower %d added\r\n' % (follower_id))

            elif args[0] == 'add_block':
                follower_id = int(args[1])
                name = args[2]
                block_type = int(args[3])
                starting_address = int(args[4])
                length = int(args[5])
                follower = server.get_slave(follower_id)
                follower.add_block(name, block_type, starting_address, length)
                sys.stdout.write('done: block %s added\r\n' % (name))

            elif args[0] == 'set_values':
                follower_id = int(args[1])
                name = args[2]
                address = int(args[3])
                values = []
                for val in args[4:]:
                    values.append(int(val))
                follower = server.get_slave(follower_id)
                follower.set_values(name, address, values)
                values = follower.get_values(name, address, len(values))
                sys.stdout.write('done: values written: %s\r\n' % (str(values)))

            elif args[0] == 'get_values':
                follower_id = int(args[1])
                name = args[2]
                address = int(args[3])
                length = int(args[4])
                follower = server.get_slave(follower_id)
                values = follower.get_values(name, address, length)
                sys.stdout.write('done: values read: %s\r\n' % (str(values)))

            else:
                sys.stdout.write("unknown command %s\r\n" % (args[0]))
    finally:
        server.stop()
    