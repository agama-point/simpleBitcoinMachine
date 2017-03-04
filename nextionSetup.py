import random, sys, os, time, datetime
import serial, pygame
from time import sleep
import subprocess

# timeout=1.0, bylo 3 ---9600 / 115200
s = serial.Serial(port='/dev/ttyAMA0',baudrate=115200,                                                   
            timeout=1.0,
            xonxoff=False, rtscts=False, 
            writeTimeout=3.0,
            dsrdtr=False, interCharTimeout=None)
    #bytesize=serial.SEVENBITS,    # 7 bitu dat
    #parity=serial.PARITY_NONE,    # bez paritniho bitu
    #stopbits=serial.STOPBITS_TWO, # 2 stop bity


#---nextion 2015/12-
  #simple label (similar arduino test)
def neXcmd(co):
    #s.write("t0.txt=")
    #s.write(chr(0x22))    
    s.write(co)
    #s.write(chr(0x22))
    s.write(chr(0xff))
    s.write(chr(0xff))
    s.write(chr(0xff))
    #s.write("\n")
    #displLab("testLAB raspi 2 " + ver)
    #def n(co):
    #hh.dispWrite(chr(co))
    time.sleep(0.0005)

def neXtxt(kam,label):
    #s.write("t0.txt=")
    s.write(kam)
    s.write(".txt=")
    s.write(chr(0x22))
    #s.write("testLAB2")
    s.write(label)
    s.write(chr(0x22))
    s.write(chr(0xff))
    s.write(chr(0xff))
    s.write(chr(0xff))
    #s.write("\n")
    #displLab("testLAB raspi 2 " + ver)
    #def n(co):
    #hh.dispWrite(chr(co))
    time.sleep(0.05)
    
    
    
    
print "nextion baud rate setup"
text="123abc"    
neXtxt("t0",text)
time.sleep(0.05) 
co="draw 0,0,50,50,RED"
neXcmd(co) 
time.sleep(0.05)   
###co="fill 95,15,215,185,WHITE"
co="bauds=9600"
neXcmd(co) 

print "ok"





    
