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
## Description :  Initial code file for RTU Master communication to WBEC
#
## Author      :  Sven Ebenfeld
#
## Date        :  2021.09.14
#
##################################################################################################

import serial
import fcntl
import os
import struct
import termios
import array
import modbus_tk
import modbus_tk.defines as cst
import modbus_tk.modbus as modbus
#import modbus_tk.modbus_rtu as modbus_rtu
from modbus_tk import modbus_rtu

# RS485 ioctls define
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
#end of rs485_enable():


if __name__ == '__main__':

    logger = modbus_tk.utils.create_logger("console")

    rs485_enable()

    #set modbus master
    master = modbus_rtu.RtuMaster(
           serial.Serial(port= '/dev/ttySC0',
           baudrate=19200,
           bytesize=8,
           parity='E',
           stopbits=1,
           xonxoff=0)
       )

    master.set_timeout(5.0)
    master.set_verbose(True)
    logger.info("connected")

    logger.info(master.execute(1, cst.READ_HOLDING_REGISTERS, 0, 4))

    #send some queries
    #logger.info(master.execute(1, cst.READ_COILS, 0, 10))
    #logger.info(master.execute(1, cst.READ_DISCRETE_INPUTS, 0, 8))
    #logger.info(master.execute(1, cst.READ_INPUT_REGISTERS, 100, 3))
    #logger.info(master.execute(1, cst.READ_HOLDING_REGISTERS, 100, 12))
    #logger.info(master.execute(1, cst.WRITE_SINGLE_COIL, 7, output_value=1))
    #logger.info(master.execute(1, cst.WRITE_SINGLE_REGISTER, 100, output_value=54))
    #logger.info(master.execute(1, cst.WRITE_MULTIPLE_COILS, 0, output_value=[1, 1, 0, 1, 1, 0, 1, 1]))
    #logger.info(master.execute(1, cst.WRITE_MULTIPLE_REGISTERS, 100, output_value=xrange(12)))

#end of if __name__ == '__main__':

