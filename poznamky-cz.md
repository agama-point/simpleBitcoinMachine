<h2>Poznámky k dalšímu vývoji:</h2><br />
<br />
Aktuální beta verze (2016/10)<br />
> běží na <b>Raspberry Pi 2</b> <i>půjde na RPi 3, ale nekompatibilita UART... vyřešeno, neaplikováno</i><br />
> generování QR pomocí "standard Linux" <b>qropencode</b> <i>možnost (nikoli nutnost) použít přímo nějakou pythoní knihovnu</i><br />
> zobrazení na <b>sériovém monitoru</b> (Arduino UNO + TTF 320x240 display, zrychleno na 115200 Bd) <i>pátral bych po jiném displeji, přímo SPI.. ? Nebo Nextion  na UARTu (mám zvládnuto, umí dobře i touchscreen..)</i><br />
stávající serial display https://github.com/octopusengine/serial-display
<br />
<hr />
<h2>Aktuální TODO:</h2><br>
<h2></h2>
<h3>A. lepší prasrování blockchainu</h3>

návrhy z FB Bitcoinové komunity:<br>
1) https://coin.cz/ <br>
2) https://blockexplorer.com/api-ref<br>
3) https://github.com/GENERALBYTESCOM/bitrafael_public/blob/master/bitrafael_common/src/com/generalbytes/bitrafael/api/IBitrafaelBitcoinAPI.java<br>




<h3>B. dotáhnout funkční verze a různé periferie</h3>
případná app z mobilu, platební automaty, zámky, IoT...<br />
1) tato betaverze je RPi2, musí být na LAN, akce - cvakne relé.. nebo podobně<br>
2) další verze na WiFi, RPi3 - s vazbou na volbu zboží nebo služen <br>
3) a otevírá se široké pole i pro IoT.. zatím třeba na ESP8266<br>
https://github.com/musdom/BlockThing


<h3>C. velký bussiness</h3> 
co z toho nechat jako open source? krabička? prodej? distribuce? záruka? servis? ...<br />
<br/>
<hr/>
2016/10 - kratičké video, kde je vidět rychlost vykreslení QR na serialdisplay<br/>
https://www.instagram.com/p/BMBZW_qAxMp/?taken-by=octopusengine



<hr>
odkaz na FB první publikování 20. 10. 2016
https://www.facebook.com/photo.php?fbid=1305566566120193&set=gm.584562355062336&type=3&theater<br>
link na blockchain
https://blockchain.info/address/11r118H2Qv4oHfjFuJnuU8GZHGNqwEH9e<br/>
další odkazy
http://docs.electrum.org/en/latest/protocol.html<br/>
http://bitcoin.stackexchange.com/questions/20312/detecting-generation-transactions<br/>
https://blockexplorer.com/api/rawtx/7dea68bf5b470747c1d821ac6e223e0d8ad611f51ddba0de4977834d3aedda02<br/>

http://bitcoin.stackexchange.com/questions/21395/how-can-a-website-detect-when-bitcoins-have-been-deposited<br/>
<br/>
<br/>
<br/>
<br/>

<script type="text/javascript" src="https://ajax.googleapis.com/ajax/libs/jquery/1.8.0/jquery.min.js"></script>
<script type="text/javascript" src="https://blockchain.info/Resources/js/pay-now-button.js"></script>


