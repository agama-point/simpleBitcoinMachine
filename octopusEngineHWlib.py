# var/lib/mpd/playlists
# simple library for raspberry pi + serialdisplay (arduino) 
# 2016/05
# 2016/10 - GPIO Jmp
# octopusengine.org
# ------------------------------
import sys, os, subprocess, time
from socket import gethostname, gethostbyname #getIp
from time import sleep

#---nextion
nxRead="00"
nx1="03"
nx2="04"
nx3="05"
nx4="06"
nx5="07"
nx6="08"
nx7="13"

import RPi.GPIO as GPIO
#--------- GPIO ------
COVER = 16
TOWER = 26
PIEZ = 20
JMP1 = TOWER
RELE1=18

#  ...
#       -   - GND
#  S 19 -   - 16 COVER
#  T 26 -   - 20 PIEZO
#   GND -   - 21 x
#       -----

# nastaveni pinu - spolecne
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
#GPIO.setup(BTNS1, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(COVER, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(TOWER, GPIO.IN, pull_up_down = GPIO.PUD_UP)

GPIO.setup(RELE1, GPIO.OUT)# beep 
GPIO.setup(PIEZ, GPIO.OUT)# beep 
beep = GPIO.PWM(PIEZ, 1500)   

def isJmp1():
   if not GPIO.input(JMP1): return True
   else: return False     
   
def isJmp2():
   if not GPIO.input(COVER): return True
   else: return False 
   
 #----------------------------------------beep

#pip(1600,0.03) #prvini pip po inicializaci 
#pip3x(2)
 
def pip(f,long):
  print "beep"
  beep.ChangeFrequency(f)
  beep.start(10)
  time.sleep(long)
  beep.stop()
  time.sleep(0.1)
  
def pip1():  
  pip(1600,0.03)
  time.sleep(1)

def pip2():
  print "beep2"
  beep.ChangeFrequency(1200)  #1500
  beep.start(10)
  time.sleep(0.1)
  beep.stop()
  time.sleep(0.8)
  beep.ChangeFrequency(1500)
  beep.start(10)
  time.sleep(0.1)
  beep.stop()
  time.sleep(0.3)


def pip3x(x):
  for num in range(x):
    pip(1800,0.1)
    time.sleep(0.5)

def pipAlarm(x):
  for num in range(x):
    pip(1800,0.15)
    time.sleep(0.8) 
 
 
 
def beep1(): #loop
   for pip in range(50):
    GPIO.output(PIEZ, True)
    sleep(0.0005) 
    GPIO.output(PIEZ, False)
    sleep(0.0005)

def beep0(): #pwm
   p1 = GPIO.PWM(PIEZ, 300)  # channel=12 frequency=400Hz
   p1.start(0.5)
   sleep(0.2)
   p1.stop() 
       


# ======uart tft serial monitor / nextion===== 9600 / 115200
import serial
s = serial.Serial(port='/dev/ttyAMA0',baudrate=9600,                                                   
            timeout=3.0,
            xonxoff=False, rtscts=False, 
            writeTimeout=3.0,
            dsrdtr=False, interCharTimeout=None)
# timeout=1.0, bylo 3 ---9600
# co="bauds=115200"
# neXcmd(co)             
# ===============================================

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
    time.sleep(0.001)

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

# =======serial display ========================================
def sdW(textString):    # simple command write  
  s.write(textString)   # 
  sleep(0.1)

def sdRQC(row,textString,col): # row position + string + color 
  lenLim = 25 #len limit for standard font size
  s.write("W"+str(col)) # set color W or c
  s.write("R"+str(row)) 
  s.write("Q"+textString[:lenLim]+"*")   # Q string *
  sleep(0.1)
  
def sdArrQ(rStart,arrText):  # block of text (several lines) from row position / last set color 
   rr=rStart
   for row in (arrText):
     sdRQC(rr,row,1)
     rr=rr+1  
  
def sdPXYC(px,py,col): # pixel x,y + color  
  s.write("W"+str(col)) # set color W or c
  s.write("P"+str(px)) 
  s.write(","+str(py)) 
  sleep(0.0005)

def sdPXY(px,py): # pixel x,y  
  s.write("P"+str(px)) 
  s.write(","+str(py)) 
  sleep(0.00001)

def sdpXY(px,py): # pixel x,y  
  s.write("p"+str(px)) 
  s.write(","+str(py)) 
  sleep(0.00001)
  
#======get IP ============================
def getIp():
   try:
    arg='ip route list'
    p=subprocess.Popen(arg,shell=True,stdout=subprocess.PIPE)
    data = p.communicate()
    split_data = data[0].split()
    ipaddr = split_data[split_data.index('src')+1]
   except:
     ipaddr ="ip.Err"
   #print "ip: " ip
   return ipaddr

#====== get procesor temp ============================
def getProcTemp():  
   try:
     pytemp = subprocess.check_output(['vcgencmd', 'measure_temp'], universal_newlines=True)
     #ipoutput = subprocess.check_output(['vcgencmd measure_temp'], universal_newlines=True, 'w'))
     #print pytemp 
     eq_index = pytemp.find('=')+1 
     #if eq_index>0:
     var_name = pytemp[:eq_index].strip()
     value = pytemp[eq_index:eq_index+4]
     numvalue=float(value)
   except:
     numvalue = -1
   return numvalue 


# ====== get dallas temp ===============================
#sudo nano /boot/config.txt >> dtoverlay=w1-gpio,gpiopin=4
try:
 import glob 
 os.system('modprobe w1-gpio')
 os.system('modprobe w1-therm')
 
 base_dir = '/sys/bus/w1/devices/'
 device_folder = glob.glob(base_dir + '28*')[0]
 device_file = device_folder + '/w1_slave'

except:
 err=True
 
def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines
 
def getDallTemp(): #get dallas senson temperature
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.1) #0.2 ok
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        #return temp_c, temp_f
        return float(int(temp_c*10))/10

#-------------------------end --------------
