from channels import route
from travel_app.consumers import ws_recieve

channel_routing = [
    route("websocket.receive", ws_recieve)  # we register our message handler
]