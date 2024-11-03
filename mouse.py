# MicroPython USB Mouse example
#
# To run this example:
#
# 1. Make sure `usb-device-mouse` is installed via: mpremote mip install usb-device-mouse
#
# 2. Run the example via: mpremote run mouse_example.py
#
# 3. mpremote will exit with an error after the previous step, because when the
#    example runs the existing USB device disconnects and then re-enumerates with
#    the mouse interface present. At this point, the example is running.
#
# 4. You should see the mouse move and right click. At this point, the example
#    is finished executing.
#
# To implement a more complex mouse with more buttons or other custom interface
# features, copy the usb-device-mouse/usb/device/mouse.py file into your own
# project and modify MouseInterface.
#mpo
# MIT license; Copyright (c) 2023-2024 Angus Gratton
import time
from lib.usb import device
from lib.usb.device.mouse import MouseInterface


def mouse():
    m = MouseInterface()

    # Note: builtin_driver=True means that if there's a USB-CDC REPL
    # available then it will appear as well as the HID device.
    device.get().init(m, builtin_driver = True)
    # wait for host to enumerate as a HID device...
    while not m.is_open():
        print("WAITING")
        time.sleep_ms(100)

    print("Start...")

    if m.is_open(): 
        print("OPEN")
    else: 
        print("CLOSE")

    time.sleep_ms(100)
    m.move_by(1000, 1000)

mouse()