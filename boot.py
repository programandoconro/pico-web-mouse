# boot.py -- run on boot-up
from credentials import SSID, PW


def do_connect():
    import network
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect(SSID, PW)
        #while not sta_if.isconnected():
        #   pass
    if sta_if.isconnected():
        print('Connected! Network config:', sta_if.ifconfig())
    else:
        print("NOT CONNECTED")
    
print("Connecting to your wifi...")
do_connect()
