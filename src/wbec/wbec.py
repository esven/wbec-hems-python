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
## Description :  Representation of WBEC in Python
#
## Author      :  Sven Ebenfeld
#
## Date        :  2021.09.17
#
##################################################################################################

from enum import Enum
from array import array

class ChargingState(Enum):
    DEFAULT = 1
    A1 = 2
    A2 = 3
    B1 = 4
    B2 = 5
    C1 = 6
    C2 = 7
    DERATING = 8
    E = 9
    F = 10
    ERR = 11

class LockState(Enum):
    LOCKED = 0
    UNLOCKED = 1

class StandbyFunction(Enum):
    ENABLED = 0
    DISABLED = 4

class Wbec:
    def __init__(self, name, busId, minCurrent= 6, maxCurrent = 6, layout = 0x108):
        self.name = name
        self.busId = busId
        self.minCurrent = minCurrent
        self.maxCurrent = maxCurrent
        self.layout = layout

        self.chargingState = ChargingState.DEFAULT
        self.l1Current = 0.0
        self.l2Current = 0.0
        self.l3Current = 0.0
        self.pcbTemperature = 0.0
        self.l1Voltage = 0
        self.l2Voltage = 0
        self.l3Voltage = 0
        self.externLockState = LockState.UNLOCKED
        self.power = 0
        self.energySincePowerOn = 0
        self.energySinceInstallation = 0
        self.logistic = ""
        self.hardwareVariant = 0
        self.applicationSoftware = 0
        self.diagnosticData = array('H')
        for x in range(18):
            self.diagnosticData.append(0)
        self.errorMemory = array('h')
        for x in range(319):
            self.errorMemory.append(0)
        self.masterWatchdogTimeout = 15000
        self.standByFunction = StandbyFunction.ENABLED
        self.remoteLock = LockState.UNLOCKED
        self.maximumCurrentCommand = 0
        self.failsafeCurrent = 0