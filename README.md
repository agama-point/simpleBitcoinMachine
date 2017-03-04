# simpleBitcoinMachine

alfa testing: <b>block-test02.py</b><br />
Paper wallet QR code...<br />
new transaction > action<br />
<br /><br />
<hr />
<pre>
# octopusengine.eu | newreality.eu
#--------------------------------------------

#block-0.2 - 2015-12 - main idea + serial display
#block-0.316 - 2016-10 - "better" HTMLParser + nextion display
#block-0.317 - 2017-02 - JSON HTMLParser + new "design" 

# is last transaction from blockchain.info > action
</pre>

starting:<br>
<code>sudo python simplebtc.py</code><br> 

<b>YES! It works!</b>
<hr />


While opinions on cryptocurrencies are strongly divided, we believe they will find a place in future. As a de-centralised payment instrument, fully computerised currency and store of value.<br /><br />

That’s why we are creating Simple Bitcoin Terminal.<br /><br />

Light, portable, easy to operate – cashier that allows you to accept payments in Bitcoin (and possibly other cryptocurrencies).<br /><br />

Constructed from Raspberry Pi and Nextion touch display. You can adjust it and use flexibly in variety of cases:<br />

– PoS system in shops, restaurants, bars….<br />
– Payment processor for vending and ticket machines<br />
– Part of paid access/service system (unlocking a door, switching a light, AC…)<br />
– Can include BTC chart and alerts<br /><br />
<hr />

More about it:<br />
http://www.octopusengine.org/bitcoin-simple-machine/<br />
<br />
<br />
<hr />
<img src="https://raw.githubusercontent.com/octopusengine/simpleBitcoinMachine/master/images/bm17.JPG" alt="btcmachine.jpg " width="800"><br />
2017/02 - ver. 0.317<br />
<br />

<img src="https://raw.githubusercontent.com/octopusengine/simpleBitcoinMachine/master/images/bm1617.JPG" alt="btcmachine.jpg " width="800"><br />
<br />
<br />




2015/2016 old edition:<br />
<img src="https://raw.githubusercontent.com/octopusengine/simpleBitcoinMachine/master/images/btcmachine.jpg " alt="btcmachine.jpg " width="800">


The new version is using Raspberry Pi and <b>serial display</b> for displaiyng QR code.
>> https://github.com/octopusengine/serial-display
From BITSTAMP.net "gets" current (BTC/USD), recalculate the amount required (USD to BTC), and it generates QR code,
after payment is executed events (relays, ...)<br />
Payment of small amounts => waiting only for new transaction in blockchain...<br />
<b>All this takes a few seconds!</b><br />
<hr />
Next step? LoLin + micropython / or Raspberry Py 3?<br />
blockchain.info better parse or JSON API<br />
>> Final machine for dispensing goods or opening doors ;-) Up2U</br>
<br /><br /><br />
<hr />
<b>simple bitstamp JSON parsser:</b><br />
<pre>
cfile = urllib2.urlopen("https://www.bitstamp.net/api/ticker/").read()
jObj = json.loads(bcfile)
lastNum =int(float(jObj["last"])) 
</pre>
<hr />
<b>QR code:</b><br />
<pre>

</pre>





<br /><br /><br />
What about BTC donation? ;-)<br />
Please support us with BTC if you find the code useful:  <br />
<img src="https://raw.githubusercontent.com/octopusengine/simpleBitcoinMachine/master/images/qg.png" alt="btc "><br />
https://blockchain.info/address/11r118H2Qv4oHfjFuJnuU8GZHGNqwEH9e
<br /><br /><br />

