# pico-web-mouse

## A remote virtual mouse controlled from your phone

A web app the allows you to remotely control your computer's mouse from you phone as a virtual mouse. You connect a Raspberry Pico W to your computer, it will serve a websocket server for real time interaction. Go to the server's ip in your phon and move with touch events. Your computer will move the cursor from your phone.

It is a websocket server with the Raspberry Pico W that allows you to control your mouse from a web app. You can connect the Raspberry to your target device, then connect to the server using your phone, and move in the web site as a virtual mouse connected to your real device.

Built using Adafruit Circuitpython for the Websocket server and the HID functionality.

## How to use

1. Install circuitpython into your Raspberry Pico W micro-controller.
2. Add a `settings.toml` file with your wifi's credentials:

```
CIRCUITPY_WIFI_SSID = "ssid"
CIRCUITPY_WIFI_PASSWORD = "password"

```

3. Upload the files in this repo to you Pico.
4. Run `main.py` and find your device's ip running the server on port 5000.
5. Now that you know the ip, you can connect to your target device. Go to the ip in your phone and control the devices's mouse.

### TODO: add video demonstration
