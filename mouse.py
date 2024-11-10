import usb_hid
from adafruit_hid.mouse import Mouse as AdafruitMouse
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from adafruit_hid.keycode import Keycode

import json


m = AdafruitMouse(usb_hid.devices)
keyboard = Keyboard(usb_hid.devices)
k = KeyboardLayoutUS(keyboard)

class Mouse:
    def __init__(self):
        pass

    def parse_coors(self, data: str) -> tuple:
        arr = data.split()
        try:
            x = int(arr[0]) if arr and len(arr) > 0 else None
            y = int(arr[1]) if arr and len(arr) > 1 else None
        except:
            x = 0
            y = 0

        return(x, y)

    def move(self, coors) -> None:
        (x, y) = self.parse_coors(coors)
        m.move(x, y)

    def click(self, button) -> None:
        if button == "left":
            m.click(AdafruitMouse.LEFT_BUTTON)
        elif button == "right":
            m.click(AdafruitMouse.RIGHT_BUTTON)

    def write(self, text: str) -> None:
        k.write(text)
    
    def handle_mouse_events(self, msg: str)-> str:
        try:
            parsed = json.loads(msg)
            message_type = parsed.get("type")
            message_value = parsed.get("value")

            if message_type == "move":
                self.move(coors=message_value)
            elif message_type == "click":
                self.click(button=message_value)
            elif message_type == "write":
                self.write(text=message_value)
            else:
                print("Unknown message type:", message_type)
            
            return message_value

        except json.JSONDecodeError:
            return "Failed to decode JSON"
