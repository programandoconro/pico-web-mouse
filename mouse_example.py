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
#
# MIT license; Copyright (c) 2023-2024 Angus Gratton
import time
import lib.usb.device
from lib.usb.device.mouse import MouseInterface


def mouse_example():
    m = MouseInterface()

    # Note: builtin_driver=True means that if there's a USB-CDC REPL
    # available then it will appear as well as the HID device.
    lib.usb.device.get().init(m, builtin_driver=False)

    # wait for host to enumerate as a HID device...
    while not m.is_open():
        print("NOT OPEN")
        time.sleep(1)

    time.sleep(1)

    print("Moving...")
    m.move_by(-100, 0)
    m.move_by(-100, 0)
    time.sleep(5)

    print("Clicking...")
    m.click_right(True)
    time.sleep(2)
    m.click_right(False)

    print("Done!")


mouse_example()
