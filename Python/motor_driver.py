import serial
import struct
import time
from numpy import array
from pylab import plot,show,figure
from imu import imu


class motor_driver:
    def __init__(self,port=0,protocol="hl"):
        self.serialport = serial.Serial(port,baudrate=115200, timeout=1) 
        self.protocol = protocol
        
    '''
    Set a given speed on a give motor
    stop all motors first
    '''
        
    def setSpeed(self,motor,speedint):
        #self.stop(protocol)
        protocol = self.protocol
        if(protocol=="hl"):
            self.serialport.write(str(motor))
            self.stop()
            h_str = ''
            for i in range(speedint):
                h_str = h_str + 'h'
            self.serialport.write(h_str)
        if(protocol=="abs"):
            self.serialport.write(struct.pack('B',250+motor))
            #line1 = self.serialport.readline()
            self.serialport.write(struct.pack('B',speedint))
            #line2 = self.serialport.readline()
            #print line1,line2
            
    
    '''
    Stop all motors
    '''
    def stop(self):
        protocol = self.protocol
        if(protocol=="hl"):
            self.serialport.write(str(0))
        if(protocol=="abs"):
            self.serialport.write(struct.pack('B',0))
            #line = self.serialport.readline()
            #print line
