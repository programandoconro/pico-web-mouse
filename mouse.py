import usb_hid
from adafruit_hid.mouse import Mouse as AdafruitMouse

m = AdafruitMouse(usb_hid.devices)
class Mouse:
    def __init__(self):
        pass

    def parse_data(self, data: str) -> tuple:
        arr = data.split()
        try:
            x = int(data[0]) if arr and len(arr) > 0 else None
            y = int(data[1]) if arr and len(arr) > 1 else None
        except:
            x = 0
            y = 0

        return(x, y)

    def move(self, data) -> None:
        (x, y) = self.parse_data(data)
        m.move(x, y)

    