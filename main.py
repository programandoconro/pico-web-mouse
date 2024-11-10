# Creates a websocket server to virtually mouse control remotely
# It also allows clicking, tapping and writing
# Websocket based on adafruit websocket example https://docs.circuitpython.org/projects/httpserver/en/latest/examples.html#websockets

from adafruit_httpserver import Server, Request, Response, Websocket, GET
from asyncio import create_task, gather, run, sleep as async_sleep
import socketpool
import digitalio
import board
import wifi

from device import Device

pool = socketpool.SocketPool(wifi.radio)
server = Server(pool)

websocket: Websocket = None

device = Device()

led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

@server.route("/", GET)
def client(request: Request):
    try:
        with open("/index.html", "r") as file:
            html_content = file.read()
        led.value = True
        return Response(request, html_content, content_type="text/html")
    except OSError:
        led.value = False
        return Response(request, "File not found", status=404)

@server.route("/websocket", GET)
def connect_client(request: Request):
    global websocket

    if websocket is not None:
        websocket.close()

    websocket = Websocket(request)

    return websocket


server.start(str(wifi.radio.ipv4_address), 80)

async def handle_http_requests():
    while True:
        server.poll()

        await async_sleep(0)


async def handle_websocket_requests():
    global websocket

    while True:
        if websocket is not None:
            try:
                data = websocket.receive(fail_silently=True)
                
                if data is not None:
                    device.handle_events(msg=data)
                    
            except (IndexError, OSError) as e:
                print(f"WebSocket error: {e}")
                websocket.close()  # Ensure the WebSocket is closed if an error occurs
                websocket = None  # Reset the WebSocket variable to None
                
        await async_sleep(0)


async def main():
    await gather(
        create_task(handle_http_requests()),
        create_task(handle_websocket_requests()),
    )


run(main())
