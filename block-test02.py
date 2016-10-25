# https://github.com/octopusengine/simpleBitcoinMachine
# ing.Jan Copak - Czechrepublic / Prague
# octopusengine.eu | newreality.eu
#--------------------------------------------

#block-test01 - 2016-09 - main idea
#block-test02 - 2016-10 - "better" HTMLParser

# is last transaction from blockchain.info today? yes > action
#--------------------------------------------
#toto: https://github.com/blockchain/receive-payments-demos/blob/master/python/receive_demo/views.py 
#--------------------------------------------
import urllib
import time
import urllib2 #course
import json    #=
from HTMLParser import HTMLParser

#my wallet address:
wallAdr="11r118H2Qv4oHfjFuJnuU8GZHGNqwEH9e"
arrLines = []
transactions = []

# create a subclass and override the handler methods
class MyHTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        ## print "Encountered a start tag:", tag
        if (tag =="span"):
           arrLines.append(tag)   

    def handle_endtag(self, tag):
        ## print "Encountered an end tag :", tag
        nic=True

    def handle_data(self, data):
        ## print ":", data
        arrLines.append(data)
        #if (data =="Total: "): print ": >>> ", data

parser = MyHTMLParser() #test: parser.feed('<html><head><title>Test</title></head><body><h1>Parse me!</h1></body></html>')

#---server time--- and parameters...
print "octopusengine/api --- server time:"

tim = urllib2.urlopen("http://www.octopusengine.eu/api/datetime.php").read()
print "datetime >>>"
print str(tim)

#---bitstamp course---
print "bitcoin: bitstamp ---"

bcfile = urllib2.urlopen("https://www.bitstamp.net/api/ticker/").read()
print "ticker >>>"

jObj = json.loads(bcfile)
jObj = json.loads(urllib2.urlopen("https://www.bitstamp.net/api/ticker/").read())
    
lastNum =int(float(jObj["last"]))
print lastNum
#----------------------
resource = urllib.urlopen("https://blockchain.info/unspent?active="+wallAdr+"&format=html")
blockData = resource.read()
# print blockData
tempData = parser.feed(blockData)
# print tempData
# tempLines = tempData.readlines()

print "myWallet Address: "+wallAdr   
print "-------------------------------------"
i=0
for line in arrLines:
    if line=="Unspent Outputs ":
       print arrLines[i]
       print arrLines[i+1]
       
    if line=="Total: ":
       print arrLines[i]
       print arrLines[i+2]
    if line=="span":
       #print i 
       #print arrLines[i]
       try:
           testNum= int(arrLines[i+1][0])
           #print "span >>> "+arrLines[i+1]
           transactions.append(arrLines[i+1])
       except:    
           noNum=True       
    i=i+1
print "-------------------------------------"
print "transactions"
for line in transactions:
    print line
print "-------------------------------------"    
print "last transaction"
#print transactions[1] #datedime
#print transactions[2] #BTC

timDate=tim[:10]
traDate=transactions[1][:10]
try:    
  value=float(transactions[2][:-4])
  print str(value)+" BTC"
  print str(value*lastNum)+" USD"
except:    
  print "value Err" 

#print timDate
if (timDate==traDate):
    print "today is OK"
#--------------------------------------------/end 
