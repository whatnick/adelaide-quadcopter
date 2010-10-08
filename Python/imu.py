#! /usr/bin/env python
"""
Scan for serial ports
set up IMU on first one found (windows)
read 9 params + hardware time off IMU
and then setting a pair of motors
after read a pitch,yaw roll angle
"""

import serial
import struct
import time
from numpy import array
from pylab import plot,show,figure
from motor_driver import motor_driver
class imu:
    def __init__(self):
        avl = self.scan()
        if(len(avl)>0):
            self.serialport = serial.Serial('COM17') 
            self.serialport.setBaudrate(115200)
            self.serialport.setTimeout(10)

    def scan(self):
        """scan for available ports. return a list of tuples (num, name)"""
        available = []
        for i in range(256):
            try:
                s = serial.Serial(i)
                available.append( (i, s.portstr))
                s.close()   # explicit close 'cause of delayed GC in java
            except serial.SerialException:
                pass
        return available

    def readimu(self):
        self.serialport.write('\xCB')
        a=self.serialport.read(43)
        return struct.unpack('>fffffffffL', a[1:41])
    
    def stop(self):
        self.serialport.close()
