from asyncio import create_task, gather, run, sleep as async_sleep
import microcontroller
import socketpool
import wifi

from adafruit_httpserver import Server, Request, Response, Websocket, GET


pool = socketpool.SocketPool(wifi.radio)
server = Server(pool, debug=True)


websocket: Websocket = None

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Pico Web Mouse</title>
  </head>
  <body>
    <h1>Pico Web Mouse</h1>
    <div class="frame" id="frame"></div>
  </body>
</html>

<style>
  body {
    background-color: black;
    color: whitesmoke;
    display: flex;
    justify-content: center;
    align-items: center;
    flex-direction: column;
  }
  .frame {
    border: solid 1px whitesmoke;
    height: 70vh;
    width: 90%;
  }
</style>

<script>
  console.log("Attempting to connect to server");

  const url = `ws://${window.location.host}/connect-websocket`;
  const webSocket = new WebSocket(url);

  webSocket.addEventListener("open", () => {
    console.log("Connected to server");
    webSocket.send("Hello from client");
  });

  webSocket.addEventListener("close", () => {
    console.log("Connection closed");
  });

  webSocket.addEventListener("error", (error) => {
    console.log("WebSocket error:", error);
  });

  webSocket.addEventListener("message", (event) => {
    console.log("Message from server:", event.data);
  });

  const frame = document.getElementById("frame");

  const prevPos = { prevX: undefined, prevY: undefined };
  frame.addEventListener("touchmove", ({ touches }) => {
    const { clientX, clientY } = touches[0];
    const newX = Math.trunc(clientX);
    const newY = Math.trunc(clientY);
    const { prevX, prevY } = prevPos;
    if (prevX !== newX && prevY !== newY) {
      webSocket.send(`${newX} ${newY}`);
      prevPos.prevX = newX;
      prevPos.prevY = newY;
    }
  });
</script>

"""


@server.route("/", GET)
def client(request: Request):
    return Response(request, HTML_TEMPLATE, content_type="text/html")


@server.route("/connect-websocket", GET)
def connect_client(request: Request):
    global websocket  # pylint: disable=global-statement

    if websocket is not None:
        websocket.close()  # Close any existing connection

    websocket = Websocket(request)

    return websocket


server.start(str(wifi.radio.ipv4_address))


async def handle_http_requests():
    while True:
        server.poll()

        await async_sleep(0)


async def handle_websocket_requests():
    while True:
        if websocket is not None:
            if (data := websocket.receive(fail_silently=True)) is not None:
                print(data)

        await async_sleep(0)


async def send_websocket_messages():
    while True:
        if websocket is not None:
            cpu_temp = round(microcontroller.cpu.temperature, 2)
            websocket.send_message(str(cpu_temp), fail_silently=True)

        await async_sleep(1)


async def main():
    await gather(
        create_task(handle_http_requests()),
        create_task(handle_websocket_requests()),
        create_task(send_websocket_messages()),
    )


run(main())
