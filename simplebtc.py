# https://github.com/octopusengine/simpleBitcoinMachine
# ing.Jan Copak - Czechrepublic / Prague
# octopusengine.org | newreality.eu
#--------------------------------------------
# 0.2 - 2015-12 - main idea + serial display
# 0.316 - 2016-10 - "better" HTMLParser + nextion display
# 0.317 - 2017-02 - JSON HTMLParser + alarm loop / new "design"

# is last transaction from blockchain.info today? (/this minute) yes > action
#--------------------------------------------

ver="ver. 0.317 | 2017/02" #alarm loop

import urllib
import os, time, datetime
import urllib2 #course
import json    #=

from threading import Thread, Event
nexThread = True #running

from octopusEngineHWlib import *
from octopusEngineBTCmachine import *

GPIO.output(RELE1, False)
time.sleep(6)
GPIO.output(RELE1, True) #off
time.sleep(2)

# flash disk and ramdisk:
flashPath = "/home/pi/fd/"
ramdiskPath = "/home/pi/ramdisk/"

# values A-F:
vA = 1.0
vB = 2.0
vC = 3.0
vD = 5.0
vE = 8.0
vF = 10.0

kurzUSD=25
lastNum = 1235
wasJmp = False

netOk = False
nextionBool = True    
arrLines = []
transactions = []

pip1() #initialization.ok > beep 

wasJmp = isJmp1()
jmp1 = "-JMP:"+str(wasJmp)
print jmp1

minMin=800 #for chart: minimum value
kMax = 0
kMin = 999999	
	
kS = 1001# cca aktual
aMin = 1111
aMax = 1299
aPip = 931

dY = 200 #210

def parseVars():
   global newHostname, kS, aMin, aMax, ssid, password
   vars = dict()
   varsNet = dict()   
   with open(flashPath+"config.ini") as f:     
     for line in f:
        #print line       
        eq_index = line.find('=') 
        if eq_index>0:
          var_name = line[:eq_index].strip()
          try:
             if (var_name=="password"):
                value = (line[eq_index + 1:].strip())
             else:
                value = float(line[eq_index + 1:].strip())
          except:
             value = (line[eq_index + 1:].strip()) 
          vars[var_name] = value


   print vars

   try: kS = float(vars["line"])
   except: nic=True
  
   try: aMin = float(vars["min"])
   except: nic=True
  
   try: aMax = float(vars["max"])
   except: nic=True
 
   try: newHostname = str(vars["hostname"])
   except: err=True

   try: noteNet = vars["noteInfo"]
   except: noteNet ="???"

   try: ssid = vars["ssid"]
   except: setupWifi=False
  



#---------------------------------------------------------------------
def nexth(): ##thread
 global nxRead, nexThread
 #nexThread = True
 #nxRead ="99"
 s.flushInput()
 cntx=0
 nacti= 7
 while nexThread:
 #for ii in range (30): 
       
   try:
    hodnota = s.read(nacti) #7
    #print "h."+hodnota
    iok=2 
    for ii in range (nacti):
     #print (hodnota[ii]).encode("hex"),
     if ((hodnota[ii]).encode("hex")=="65"):
      iok = ii # index      
      nexWrite=((hodnota[iok+2]).encode("hex"))
      print ":::::::nex-th:::::::"+nexWrite
      nxRead = nexWrite      
     
   except:
    # print "Err.data"
    nic = True  
   
   time.sleep(0.5)
   cntx=cntx+1


class StoppableThread(Thread):
    """Thread class with a stop() method. The thread itself has to check
    regularly for the stopped() condition."""

    def __init__(self, *args, **kwargs):
        super(StoppableThread, self).__init__(*args, **kwargs)
        self._stop = Event()

    def stop(self):
        self._stop.set()

    def stopped(self):
        return self._stop.isSet()

#----------------------------------------------------------------thread
#exec_command("sudo python nex.py")
##import subprocess
##subprocess.Popen("./nex.py")

thrnx = StoppableThread(target=nexth)
thrnx.start()

def oneTestBlockchain():
	global transData, transValue, transTime, txsTime
	transData=getLastTransaction()
	transValue=transData[0]
	transTime=transData[1]
	txsTime=transData[2]
	
def k2g(k):	
	#y=dY-(k-minMin)/2
	y=dY-(k-minMin)/2
	return y
	
def alarmLoop():
	global kS, kMax, kMin
	cntLoop = 0
		
	pip1()	
	neXcmd("page chart") 
	neXcmd("page chart")
	time.sleep(0.3)
	print "parse fd vars: line min max"
	try:
	  parseVars()
	except: nic=True
	
	print "line " + str(kS)
	print "alarm min " + str(aMin)
	print "alerm max" + str(aMax)
	
	
	#neXtxt("tb0","> alarm loop mode:") 
	time.sleep(2)
	
	co="fill "+str(1)+","+str(k2g(kS-50))+",2,2,GRAY" #700
	neXcmd(co) 
	
	co="fill "+str(1)+","+str(k2g(kS+50))+",2,2,GRAY" #800
	neXcmd(co) 
	
	for dX in range(110):
		co="fill "+str(dX*3)+","+str(k2g(kS))+",1,1,GRAY" #900
		neXcmd(co) 
		time.sleep(0.05)		
	
	neXcmd("fill "+str(1)+","+str(k2g(aMin))+",2,2,BLUE") 
	neXcmd("fill "+str(3)+","+str(k2g(aMin))+",2,2,BLUE") 
		
	neXcmd("fill "+str(1)+","+str(k2g(aMax))+",2,2,BLUE") 
	neXcmd("fill "+str(3)+","+str(k2g(aMax))+",2,2,BLUE") 	
	
	#for test in range(5):
	while True:	
		cntLoop = cntLoop+1	
		#neXtxt("tb8",str(cntLoop))	
		
		time.sleep(2)
		bcfile = urllib2.urlopen("https://www.bitstamp.net/api/ticker/").read()
		jObj = json.loads(bcfile)
		lastNum =int(float(jObj["last"])) 
		
		if kMax<lastNum: kMax=lastNum
		if kMin>lastNum: kMin=lastNum
		
		if aMax<lastNum: alarm("alarm max " + str(aMax))
		if aMin>lastNum: alarm("alarm min " + str(aMin))
		if aPip==lastNum: pip1()	
		
		neXtxt("kurz",str(lastNum)) 
		time.sleep(2)
		neXtxt("tb1","min: "+str(kMin)+" < max: "+str(kMax) ) 

		nowTim = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		neXtxt("tb2","date.Time: "+str(nowTim)) 
		time.sleep(2)
		
		co="fill "+str(int(cntLoop/5))+","+str(k2g(lastNum))+",2,2,RED"
		neXcmd(co) 
		

		for okLoop in range(35):
			neXtxt("tb3",str(aMin)+"  < >  "+str(aMax))
			time.sleep(1.3)  
			neXtxt("tb3",str(cntLoop)) 	 
			time.sleep(1.2) 

			nowTim2 = datetime.datetime.now().strftime("%H:%M:%S")
			neXtxt("tb2",str(nowTim2)) 

def alarm(co):
	for okLoop in range(3):
		for okLoop in range(3):
			pip1()
			time.sleep(0.2)
		neXtxt("tb3",co)
		time.sleep(1)  
		neXtxt("tb3"," ") 	 
		time.sleep(1) 
		
	GPIO.output(RELE1, False)
	time.sleep(6)
	GPIO.output(RELE1, True) #off
	time.sleep(1)		


def oneAction():
  global nxRead, nexThread, ctu, valUSD, amount, lastNum	
  global transData, transValue, transTime, txsTime, netOk
  # reset to default values	
  valUSD= 1.1
  transTim = "2016-11-11"
  transValue = 0

  displayInit(nextionBool)
  pip1()
  neXcmd("page intro")
  neXcmd("page intro")

  time.sleep(5)
  GPIO.output(RELE1, True)

  nowTim = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
  addLog("S-"+nowTim+jmp1)
  
  cekej = True
  ccnt=0
  #s2.flushInput()
  #for rx in range (20):
  neXcmd("page select")
  neXcmd("page select")
  print "wait to select"
  nxRead="00"

  while cekej: #---------------------------------cekani na stisk nextion
   ccnt=ccnt+1
   ctu = nxRead
   print "nxRead var ="+ ctu
   neXtxt("d0",str(ccnt) + " >> "+str(ctu))
   if (ctu<>"00"): 
    ##pip(1800,0.05) #ctu
    print "---stisknuto-ok---" + ctu
 
    if (ctu==nx1): 
     valUSD= vA
     netLed(False) ##led red
     cekej=False

    if (ctu==nx2):    
     valUSD= vB
     cekej=False
  
    if (ctu==nx3):
     valUSD= vC
     cekej=False
  
    if (ctu==nx4): 
     valUSD= vD
     netLed(True) ##led green
     cekej=False
  
    if (ctu==nx5):
     valUSD = vE
     cekej=False
  
    if (ctu==nx6):
     valUSD = vF
     cekej=False     
        
    if (ctu==nx7):
      alarmLoop()  
      cekej=False
  
  
   else: 
    #print "---nic----" + ctu
    nic = True
    time.sleep(0.7)
   if ccnt>60: cekej=False

  #nexThread = False
  #chyba-po-cteni-----------------------------------------------------
  pip1()
  neXtxt("ts1",str(valUSD))

  
  if wasJmp:
     print "off-line "
     tim = "2016-11-10 "
     lastNum = 1256
     text="set:off-line"  
     #-alarmLoop()   
  else:
     neXtxt("d0","on-line" )	
     try:  
       tim = urllib2.urlopen("http://www.octopusengine.eu/api/datetime.php").read() 
       bcfile = urllib2.urlopen("https://www.bitstamp.net/api/ticker/").read()
       print "ticker >>>"
       jObj = json.loads(bcfile)
       #jObj = json.loads(urllib2.urlopen("https://www.bitstamp.net/api/ticker/").read())  
       lastNum =int(float(jObj["last"])) 
     
       netLog("S","BTC",lastNum)
     
       #---server time--- and parameters...
       print "octopusengine/api --- server time:" 
       print str(tim) 

       #---bitstamp course---
       print "bitcoin: bitstamp ---"
       print lastNum 
       text=str(lastNum)    
       neXtxt("t2",text) 
       netOk = True
     except:
		 netOk = False
		 print "net.Err"
		 neXtxt("d0","net.Err" )
		 time.sleep(5)
  #amount=0.0123
  amount=round(float(valUSD/lastNum),8)
  amountS=amount*100000000
  print ">>>>>>>>>>", valUSD, lastNum, amount, amountS

  label= "oe" #  "octopusEngine"

  neXcmd("page qr")
  neXcmd("page qr")
  
  if isJmp1(): 
    text="off-line"
       
  else: text="on-line" 
   
  neXtxt("d0",text)
  
  text="$"+str(lastNum)    
  neXtxt("t0",text) 
  kuryCz = lastNum*25
  text="("+str(kuryCz) +" Kc)"   
  neXtxt("t1",text) 
  time.sleep(0.2) 
  
  text="$"+str(valUSD)   
  neXtxt("t3",text) 
  text=str(amount)+"BTC"    
  neXtxt("t5",text) 
  text="> "+str(valUSD*25)+" Kc"    
  neXtxt("t6",text)
  time.sleep(0.2)  
  	  
  #----------------------
  # bitcoin:12A1MyfXbW6RhdRAZEqofac5jCQQjwEPBu?amount=0.0123&message=Payment&label=Satoshi&ex
  # qrGet="bitcoin:"+wallAdr+"?amount="+str(amount)+"&label="+label +"&message=Payment&label="+label #+"&ex"
  # qrGet="bitcoin:"+wallAdr+"?amount="+str(amount)+"&label="+label+"&ex"
  qrGet="bitcoin:"+wallAdr+"?amount="+str(amount) #+"?label="+label +"&message=Payment" #+"&ex"
  print qrGet
  displayQR(nextionBool,qrGet)
  
  cntWait=0
  cntWait2=0
  while (not isJmp1()):
      time.sleep(0.3)
      neXtxt("d0","PAY")  
      time.sleep(0.3)
      neXtxt("d0","   ")
      if (cntWait2%2): 
         neXtxt("t7","than press BUTTON")
      else:       
         neXtxt("t7","sann QR & pay") 
      if (cntWait%2): 
        cntWait2 = cntWait2+1   
      cntWait = cntWait+1   
      
  pip1()   
  time.sleep(1) 
  neXcmd("page blockch") 
  neXcmd("page blockch")
  time.sleep(0.3) 
  
  if netOk:
	 neXtxt("tb9"," ")
  else:	   
     neXtxt("tb9","sorry - off Line or net.Err")  
  
  neXtxt("tb0","Last transaction info:")  
  neXtxt("tb1","$"+str(valUSD)+" | "+str(lastNum)+" USD/BTC" ) 
  txAmount =  "amount: "+str(amountS) + " Satoshi"
  time.sleep(0.5)
  neXtxt("tb2",txAmount)
  neXtxt("tb3"," ") 
  neXtxt("tb4"," ") 
  neXtxt("tb5","Blockchain info testing | "+ver) 
  neXtxt("tb6"," ") 
  neXtxt("tb7"," ") 
  neXtxt("tb8","serverTime:  "+str(tim))
    
 

  nowTim = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
  
  cntTest=1
  for test in range(5):
	 
     oneTestBlockchain()
     neXtxt("tb9","transactionT "+transTime) 
     neXtxt("tn",str(cntTest))     
     time.sleep(5)     
     cntTest=cntTest+1
   
     nowDate=tim[:10]
     #print "transTim "+transTim > 2016-11-09 18:42:14
     traDate=transTim[:10]
      
     time.sleep(0.5)  
     nowTim = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
     dtime = datetime.datetime.now()
     nowTime = time.mktime(dtime.timetuple())
     timDelta= int(nowTime)-int(txsTime) 
     
     neXtxt("tb7","machineTime: "+str(nowTim)) 
     neXtxt("tb9","transactionT "+transTime)  
    
     #if (nowDate==traDate):
     #  print "today is OK"
     #else:
     #  print "today is NOT ok"
 
     txlatVal =  "last trans.val: "+str(transValue) +" "
     neXtxt("tb3",txlatVal)  
     print txlatVal, txAmount 

     txDelta =  "delta value > "+str(transValue-amountS)      
     print txDelta
     neXtxt("tb4",txDelta)  

     time.sleep(1) 
     deltaMin = int(timDelta/60)
     neXtxt("tb6","deltaTime > "+str(timDelta)+ " = "+str(deltaMin)+ " min.")   
  
     #neXtxt("tb8","transactionT "+transTime) 
  
     okTrans=False
     if (deltaMin<2):
       okTrans=True 
       okTxt= ".....OK..... "+ " | "+str(deltaMin)+ " min."
       neXtxt("tb9",okTxt) 
       break    
     else:
		 
	   okTxt= "NO TRANSACTION "+ " | "+str(deltaMin)+ " min."
	   neXtxt("tb9",okTxt) 

  time.sleep(3) 
	 
  for okLoop in range(6):
	neXtxt("tb9",okTxt)
	time.sleep(1)  
	neXtxt("tb9"," ") 	 
	time.sleep(0.5) 
  neXtxt("tb9",okTxt)
  nowTim = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
  addLog("T-"+nowTim+" | "+str(deltaMin)+ " min. | val:"+str(transValue)+" s")	 
  addLog("> K:"+str(lastNum)+", $"+str(valUSD)+", a:"+str(amountS)+" s")	 	    
 
  #time.sleep(3) 
  #while (not isJmp1()): #waiting to press butt
  #    time.sleep(0.5)
  #    print ".",
  if okTrans: 
     pip1()   
     neXcmd("page thanks") 
     neXcmd("page thanks")
     addLog(">> OK > "+str(valUSD*kurzUSD)+" Kc"  )
     netLog("OkKc","BTC",valUSD*kurzUSD)
     
     
     GPIO.output(RELE1, False)
     time.sleep(10)
     GPIO.output(RELE1, True)
     
      
     time.sleep(3)
     neXtxt("tt1","$ "+str(valUSD))     
     time.sleep(3)
          
       
  while (not isJmp1()):
		time.sleep(0.5)
		nowTim = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		neXtxt("tb7","date Time:  "+str(nowTim)) 
		neXtxt("tb8","for next action > press BUTTON ") 
		neXtxt("tt2","next") 
		 
		time.sleep(0.5)
		neXtxt("tt2","prew")
		neXtxt("tb8"," ")   
#=====================================================================================================
try:
	#alarmLoop()
	#thrnx.stop_here
	#try:
	
	#except:
	#	print "FD config err."		
	
	while True:  
	   print "-----------------------------------action"       
	   oneAction()
	
except (KeyboardInterrupt, SystemExit), e:
	print "oops, error", e
	print "trying to gracefully shutdown child thread"
	print "stopped?", thrnx.stopped()
	thrnx.stop()
	print "stopped?", thrnx.stopped()
	thrnx.join()

print "exiting..."
#--------------------------------------------/end	
	
