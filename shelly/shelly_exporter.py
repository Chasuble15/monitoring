from prometheus_client import start_http_server
from prometheus_client.core import GaugeMetricFamily, REGISTRY
import time
import json
import requests
import yaml
from yaml.loader import SafeLoader



def get_devices_from_API(device_id, auth_key, host):
    
    data = {
        #'id': 'c45bbe6beaea',
        'id': device_id,
        'auth_key': auth_key,
    }

    response = requests.post(host +'device/status', data=data)

    if response.status_code == 200:
        return response.text
        
    print("Error status code :", response.status_code)
    return



class CustomCollector(object):
    def collect(self):
        c = GaugeMetricFamily('shelly_values', 'Données des capteurs Shelly', labels=['label', 'type', 'account', 'device_name'])

        # Open the file and load the file
        config = {}
        with open('shelly.yml') as f:
            config = yaml.load(f, Loader=SafeLoader)


        for account in config["accounts"]:

            for device_config in account["devices"]:

                try:    
                    device_data = json.loads(get_devices_from_API(device_config["id"], account["auth_key"], account["host_name"]))
                    emeters = device_data["data"]["device_status"]["emeters"]

                    for i, value in enumerate(device_config["emeters"]):
                        for label in emeters[i].items():
                            c.add_metric([value["name"], label[0], account["account_name"], device_config["name"]], label[1])

                except:
                    print("Erreur")   
        yield c




if __name__ == "__main__":
    start_http_server(9300)
    REGISTRY.register(CustomCollector())

    print("Prometheus metrics available on port 9300 /metrics")

    while True:
        time.sleep(1)