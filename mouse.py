import usb_hid
from adafruit_hid.mouse import Mouse as AdafruitMouse

m = AdafruitMouse(usb_hid.devices)
class Mouse:
    def __init__(self):
        pass

    def parse_data(self, data: str) -> tuple:
        arr = data.split()
        try:
            x = int(arr[0]) if arr and len(arr) > 0 else None
            y = int(arr[1]) if arr and len(arr) > 1 else None
        except:
            x = 0
            y = 0

        return(x, y)

    def move(self, coors) -> None:
        (x, y) = self.parse_data(coors)
        m.move(x, y)

    def click(self, button) -> None:
        if button == "left":
            m.click(AdafruitMouse.LEFT_BUTTON)
        elif button == "right":
            m.click(AdafruitMouse.RIGHT_BUTTON)
    