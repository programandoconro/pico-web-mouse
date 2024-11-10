import json

import usb_hid
from adafruit_hid.mouse import Mouse
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from adafruit_hid.keycode import Keycode


mouse = Mouse(usb_hid.devices)
keyboard = Keyboard(usb_hid.devices)
keyboard_layout_us = KeyboardLayoutUS(keyboard)

class Device:
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
        mouse.move(x, y)

    def click(self, button) -> None:
        if button == "left":
            mouse.click(Mouse.LEFT_BUTTON)
        elif button == "right":
            mouse.click(Mouse.RIGHT_BUTTON)

    def write(self, text: str) -> None:
        keyboard_layout_us.write(text)

    def hit_enter(self) -> None:
        keyboard.press(Keycode.RETURN)
        keyboard.release(Keycode.RETURN)
    
    def handle_events(self, msg: str)-> str:
        try:
            parsed = json.loads(msg)
            type = parsed.get("type")
            value = parsed.get("value")

            if type == "move":
                self.move(coors=value)
            elif type == "click":
                self.click(button=value)
            elif type == "write":
                self.write(text=value)
            elif type == "enter":
                self.hit_enter()
            else:
                print("Unknown message type:", type, value)
            
            return value

        except json.JSONDecodeError:
            return "Failed to decode JSON"
