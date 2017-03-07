#var/lib/mpd/playlists
# simple library for raspberry pi + serialdisplay (arduino)
# 2016/05
# 2016/10 - GPIO Jmp
# octopusengine.eu
# ------------------------------
import sys, os, subprocess, time, datetime
import serial
import urllib2 #course
import json
from socket import gethostname, gethostbyname #getIp
from time import sleep

from simpleBitcoinMachine.octopusEngineHWlib import *

#my wallet address:
wallAdr="11r118H2Qv4oHfjFuJnuU8GZHGNqwEH9e"
urlJson = "https://blockchain.info/address/"+wallAdr+"?format=json"

urlIoT="http://www.sentu.cz/api/led2.php"

def netLed(jak):
   if jak:
     urlLed = urlIoT+ "?light2=on"
   else:
     urlLed = urlIoT+ "?light2=off"
   print urlLed

   try:
      response = urllib2.urlopen(urlLed)
      #netKod = response.read()
      response.close()
   except:
     #doinfoQ("urlLog.Err",5)
     nic=True

urlAdd="http://www.sentu.cz/acoma/write?data.php"
def netLog(typ,device,val):
   try:
    urlLog = urlAdd+ "?type="+typ+"&value="+str(val)+"&notice="+device
   except:
     #doinfoQ("urlLog.Err",5)
     nic=True
   try:
     #print urlLog
     response = urllib2.urlopen(urlLog)
     netKod = response.read()
     response.close()
   except:
     print "netLog.Err"

def displayInit(nextionBool):
 if nextionBool:
   neXtxt("d0","start")
   time.sleep(0.05)
   #co="draw 0,0,50,50,RED"
   #neXcmd(co)
   #time.sleep(0.05)
   ###co="fill 95,15,215,185,WHITE"
 else:
   s.write("C") #clear
   time.sleep(3)
   #sdRQC(0,"today BITCOIN graph",7)
   #s.write("h35")
   s.write("W0")
   s.write("h200")

#---------------------------------------------------------------
def displayQR(nextionBool,qrGet):
  global s
  os.system('qrencode -o qrcode.png '+qrGet)
  os.system('qrencode -t ASCII -o qrcode.txt '+qrGet)

  neXcmd("baud=115200")
  time.sleep(1)
  s = serial.Serial(port='/dev/ttyAMA0',baudrate=115200,
            timeout=3.0, xonxoff=False, rtscts=False,
            writeTimeout=3.0, dsrdtr=False, interCharTimeout=None)

  co="fill 133,25,218,160,WHITE"
  neXcmd(co)
  neXcmd(co)

  time.sleep(1)  #nestihalo..

  f = open('qrcode.txt')
  lines = f.readlines()
  #print "number of lines QR: "+ str(len(lines))
  f.close()
  for i in range(3,len(lines)):
    for j in range(3,73):
        point = lines[i][j:j+1]
        if point=="#":
          #print "*",
          if nextionBool:
             co="fill "+str(135+j*2)+","+str(25+i*4)+",3,4,BLACK"
             neXcmd(co)
          else:
             sdPXYC(330-int(j*2.8),int(i*5)-10,2)
        #else:
        #    print " ",

  neXcmd("baud=9600")
  time.sleep(1)
  s = serial.Serial(port='/dev/ttyAMA0',baudrate=9600,
            timeout=3.0, xonxoff=False, rtscts=False,
            writeTimeout=3.0, dsrdtr=False, interCharTimeout=None)

# ------------------------blockchain--------------------------
def getMineOutputAddresOutput(tx,addr):
   for t in tx["out"]:
     if t["addr"]==addr: return t
   return None

def getLastTransaction():
   global transTim,transValue
   print "----------  BTC transaction JSON parser 2016/10 -----------"
   dtime = datetime.datetime.now()
   nowTime = time.mktime(dtime.timetuple())
   #print "nowTime Unix "+str(nowTime)

   jObj = json.loads(urllib2.urlopen(urlJson).read())
   myAddress = jObj["address"]
   txs =jObj["txs"] # block of transactions
   txsNewest = txs[0]
   myAddressOutput = getMineOutputAddresOutput(txsNewest,myAddress)
   transValue = myAddressOutput["value"]

   #print "timeUnx: "+str(txs[0]["time"])
   #print "TX Hash: %s" % txs[0]['hash']
   #print "TX Volume: %s satoshi" % myAddressOutput['value']
   txsTime = txs[0]["time"]
   transTim = datetime.datetime.fromtimestamp(int(txsTime)).strftime('%Y-%m-%d %H:%M:%S')
   print "TX Timestamp: %s Time: %s" % (txsTime, transTim )
   ##print "TX Timestamp: %s Time: %s" % (txs[0]["time"], datetime.datetime.fromtimestamp(int(txs[0]["time"])).strftime('%Y-%m-%d %H:%M:%S'))

   deltaT=int(nowTime)-int(txsTime)
   print "deltaT "+str(deltaT)
   return transValue,transTim,txsTime

#--------------------temp
def getLatestTx(txs):
    latest_time = -1
    latest_tx = None
    for t in txs:
        if t['time'] > latest_time:
            latest_time = t['time']
            latest_tx = t
    return latest_tx
#newest_tx = getLatestTx(address_txs)

urlAdd="http://sentu.cz/acoma/write_data.php"
def netLog(typ,device,value):
   try:
    #urlLog = urlAdd+ "?type="+typ+"&value="+str(value)+"&notice="+device
    urlLog = urlAdd+ "?value="+str(value*10)+"&type="+typ+"&notice="+device
   except:
     #doinfoQ("urlLog.Err",5)
     nic=True
   try:
     print urlLog
     response = urllib2.urlopen(urlLog)
     netKod = response.read()
     print netKod
     response.close()
     print "netLog.Ok"

   except:
     print "netLog.Err"


def addLog(txtLog):
  print "LOG:"+txtLog
  fw = open("log.txt","a")
  fw.write(txtLog+"\n")
  fw.close()

#-------------------------end --------------
