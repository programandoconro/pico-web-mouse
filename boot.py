# boot.py -- run on boot-up
from credentials import SSID, PW, SSID_FALLBACK, PW_FALLBACK


def do_connect(ssid, pw):
    import network
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect(ssid, pw)


    if sta_if.isconnected():
        from machine import Pin
        led = Pin('LED', Pin.OUT)
        led.value(1)
        print('Connected! Network config:', sta_if.ifconfig())
        return
    else:
        print("NOT CONNECTED")
        #do_connect(SSID_FALLBACK, PW_FALLBACK)
    
print("Connecting to your wifi...")
do_connect(SSID, PW)
