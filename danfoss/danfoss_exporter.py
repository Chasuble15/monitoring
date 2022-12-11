import requests
import json
import time

from prometheus_client import start_http_server
from prometheus_client.core import GaugeMetricFamily, REGISTRY


def get_devices_from_API() -> dict:

    headers = {
        'Authorization': 'Basic T2NlNFFaWjNXemNNTEx1NXp1UUxBQUhCR0R5RnJ6djc6aVpKck9ncmtHOW5BU25ldQ',
        'Accept': 'application/json',
    }

    data = {
        'grant_type': 'client_credentials',
    }

    response = requests.post('https://api.danfoss.com/oauth2/token', headers=headers, data=data)

    if response.status_code == 200:
        json_resp = json.loads(response.text)
        access_token = json_resp['access_token']
        print("Access token :", access_token)

    else:
        print("Error status code :", response.status_code)
        return

    headers = {
        'Accept': 'application/json',
        'Authorization': f'Bearer {access_token}',
    }

    response = requests.get('https://api.danfoss.com/ally/devices', headers=headers)

    if response.status_code == 200:
        return json.loads(response.text)

    else:
        print("Error status code :", response.status_code)
        return


class CustomCollector(object):
    def collect(self):
        c = GaugeMetricFamily('danfoss_values', 'Données des capteurs Danfoss', labels=['name', 'type'])

        data_dict = get_devices_from_API()

        try:
            for device in data_dict["result"]:
                if len(device["status"]) > 1:

                    for statut in device["status"]:
                        if type(statut["value"]) is not str:
                            c.add_metric([device["name"], statut["code"]], statut["value"])

        except:
            print("[Error] - Unable to parse data")
        

        yield c


if __name__ == "__main__":
    print("[Info] - Hosting metrics at port: 9500")
    start_http_server(9500)
    REGISTRY.register(CustomCollector())

    while True:
        time.sleep(1)