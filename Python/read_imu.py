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
from pylab import *
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
    pid_list=list()
    angle_list=list ()
    derivative_list=list()
    Magan=list()
    k1=2
    k2=1
    #k2=0.8
    prev_value=0
    #Ki=18
    Ki=16
    mdrv = motor_driver(14,"abs")
    #time.sleep(3)
    run_time = 1500
    th = 95
    
    mdrv.stop()
    mdrv.setSpeed(1,0)
    mdrv.setSpeed(3,0)
    time.sleep(3)
    mdrv.setSpeed(1,0)
    mdrv.setSpeed(3,0)
    time.sleep(3)
    for i in range(run_time):
        imu_data = imu_reader.readimu()
        rpy_list.append(imu_data)
        angle_rate=imu_data[4]        
        value=imu_data[6]
        Mag=imu_data[6]               
        #print imu_data
        #small test about sensor
        t_list.append(time.time())
        print value
        a_list.append(value)

        #prop = k1*(-0.05-value)
        prop = k1*(-0.2-value)
        #derivative = value-prev_value
        derivative=angle_rate
        deriv =  derivative*(1)*k2
        pid_out = (prop+deriv)*Ki

        prev_value = value
        pid_list.append(pid_out)
        derivative_list.append(deriv)
        angle_list.append(angle_rate)
        Magan.append(Mag)
        if (pid_out < 0):
            mdrv.setSpeed(1,40)
            pid_out=pid_out*(-1)
            pid_out=40+pid_out
            if pid_out>th :
               pid_out=th
            mdrv.setSpeed(3,pid_out)
     #       time.sleep(5)
            print value
        else :
            mdrv.setSpeed(3,40)           
            m_list.append(0)
            #pid_out=40+pid_out*1.3
            pid_out=40+pid_out*1
            if pid_out>th :
               pid_out=th
            mdrv.setSpeed(1,pid_out)
            print value
        #if (i==300):
        #    m_list.append(0.2)
        #    mdrv.setSpeed(1,37)
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
    log_file = open("data_90.txt","w")
    r_array = array(rpy_list)
    for line in rpy_list:
        log_file.write(str(line)+"\n")
    mdrv.stop()
    figure(1)
    subplot(311)
    plot(pid_list)
    ylabel("Pid Voltage")
    subplot(312)
    plot(derivative_list)
    ylabel("Derivative")
    #subplot(223)
    #plot(angle_list)
    #ylabel("Angular Rate")
    subplot(313)
    plot(Magan)
    ylabel("Angle Magnitude")

     
    #mdrv.stop()
    mdrv.serialport.close()
    imu_reader.serialport.close()
        
    log_file.flush()
    log_file.close()
    #print rpy_list
    #print t_list

    """
    figure(1)
    plot(r_array[:,9],r_array[:,0:3])
    figure(2)
    plot(r_array[:,9],r_array[:,3:6])
    figure(3)
    plot(r_array[:,9],r_array[:,6:9])
    mdrv.stop()
    mdrv.serialport.close()
    imu_reader.serialport.close()
    show()
    """
    #exit()
    
    
