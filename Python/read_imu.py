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
#from motor_driver import motor_driver

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

            
if __name__=='__main__':
    imu_reader = imu()
    rpy_list = list()
    t_list = list()
    v_list = list()
    a_list = list()
    m_list = list()
    
    mdrv = motor_driver(14,"abs")
    time.sleep(5)


    
    mdrv.stop()
    mdrv.setSpeed(3,40)
    time.sleep(1)
    ph=20
    for i in range(40):
        #imu_data = imu_reader.readimu()
        #rpy_list.append(imu_data)
        #value=imu_data[4]
        #print imu_data
        #small test about sensor
        #t_list.append(time.time())
        #print value
        #a_list.append(value)
        
       # if (i == 100):
        m_list.append(0.1)
        mdrv.setSpeed(3,ph)
        time.sleep(0.5)
        ph=ph+1
        print ph
     #       time.sleep(5)
     #   else :
#  m_list.append(0)

      #  if (i==300):
      #      m_list.append(0.2)
      #      mdrv.setSpeed(1,40)
        #if (i== 500):
        #    m_list.append(0.2)
        #    mdrv.setSpeed(3,75)
        #if (i== 700):
        #    m_list.append(0.2)
        #    mdrv.setSpeed(3,5)
        #if (i== 900):
        #    m_list.append(0.5)
        #   mdrv.setSpeed(3,5)
            #time.sleep(1)
            #mdrv.setSpeed(3,1)
            
            #mdrv.stop()
            #print value
        #else :


        
            #m_list.append(0)

   
        
    imu_reader.stop()
    #figure(33)
    #plot(a_list)
    #plot(m_list)
    log_file = open("data_50.txt","w")
    r_array = array(rpy_list)
    for line in rpy_list:
        log_file.write(str(line)+"\n")

    #mdrv.stop()
    #mdrv.serialport.close()
    #imu_reader.serialport.close()
    
    log_file.flush()
    log_file.close()
    #print rpy_list
    #print t_list
    
    #figure(1)
    #plot(r_array[:,9],r_array[:,0:3])
    #figure(2)
    #plot(r_array[:,9],r_array[:,3:6])
    #figure(3)
    #plot(r_array[:,9],r_array[:,6:9])
    #show()
    
    mdrv.stop()
    mdrv.serialport.close()
    imu_reader.serialport.close()
    
#    show()
    
