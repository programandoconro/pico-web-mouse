from asyncio import create_task, gather, run, sleep as async_sleep
import socketpool
import wifi
from adafruit_httpserver import Server, Request, Response, Websocket, GET
from mouse import Mouse
import digitalio
import board

pool = socketpool.SocketPool(wifi.radio)
server = Server(pool, debug=True)

websocket: Websocket = None

m = Mouse()

led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

@server.route("/", GET)
def client(request: Request):
    try:
        with open("/index.html", "r") as file:
            html_content = file.read()
        return Response(request, html_content, content_type="text/html")
    except OSError:
        return Response(request, "File not found", status=404)

@server.route("/connect-websocket", GET)
def connect_client(request: Request):
    global websocket

    if websocket is not None:
        print("CLOSED")
        led.value = False
        websocket.close()

    websocket = Websocket(request)

    return websocket


server.start(str(wifi.radio.ipv4_address))


async def handle_http_requests():
    led.value = True
    while True:
        server.poll()

        await async_sleep(0)


async def handle_websocket_requests():
    while True:
        if websocket is not None:
            if (data := websocket.receive(fail_silently=True)) is not None:
                (x, y) = m.parse_data(data)
                print(x, y)
                m.move(data)

        await async_sleep(0)


async def send_websocket_messages():
  pass


async def main():
    await gather(
        create_task(handle_http_requests()),
        create_task(handle_websocket_requests()),
        create_task(send_websocket_messages()),
    )


run(main())
