import http.server
import json
from prometheus_client import start_http_server
from urllib.parse import urlparse, parse_qs
# from chirpstack_api.as_pb import integration
# from google.protobuf.json_format import Parse
from prometheus_client.core import GaugeMetricFamily, REGISTRY


ACTUAL_DATA = {}

class CustomCollector(object):
    def collect(self):
        c = GaugeMetricFamily('chirpstack_values', 'Données des capteurs LoRa', labels=['name', 'type'])

        for device in ACTUAL_DATA.items():
            for label in device[1].items():
                 c.add_metric([device[0], label[0]], label[1])
        yield c


class ServerHandler(http.server.BaseHTTPRequestHandler):

    json = True

    def do_POST(self):
        self.send_response(200)
        self.end_headers()
        query_args = parse_qs(urlparse(self.path).query)

        content_len = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_len)

        print("EVENT ::::::", query_args["event"][0])

        if query_args["event"][0] == "up":
            self.up(body)

        # elif query_args["event"][0] == "join":
        #     self.join(body)

        else:
            print("handler for event %s is not implemented" % query_args["event"][0])

    def up(self, body):
        global ACTUAL_DATA

        body_json = json.loads(body)
            
        dev_eui = body_json["deviceInfo"]["devEui"]

        ACTUAL_DATA[dev_eui] = body_json["object"]
        print(dev_eui, body_json["object"])

        #up = self.unmarshal(body, integration.UplinkEvent())
        #print("Uplink received from: %s with payload: %s" % (up.dev_eui.hex(), up.data.hex()))

        # 
        # data = json.loads(up.object_json)
        # print(data)

    # def join(self, body):
    #     join = self.unmarshal(body, integration.JoinEvent())
    #     print("Device: %s joined with DevAddr: %s" % (join.dev_eui.hex(), join.dev_addr.hex()))

    # def unmarshal(self, body, pl):
    #     if self.json:
    #         return Parse(body, pl)

    #     pl.ParseFromString(body)
    #     return pl


    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        


if __name__ == "__main__":
    start_http_server(9200)
    REGISTRY.register(CustomCollector())

    server = http.server.HTTPServer(('', 9201), ServerHandler)

    print("Prometheus metrics available on port 9200 /metrics")
    print("Listening chirpstack on port 9201")
    server.serve_forever()