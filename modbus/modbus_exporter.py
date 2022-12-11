from itertools import count
from pyModbusTCP.client import ModbusClient
from pyModbusTCP.utils import decode_ieee, word_list_to_long, get_2comp

from prometheus_client import start_http_server
from prometheus_client.core import GaugeMetricFamily, REGISTRY
import time
import datetime

import yaml
from yaml.loader import SafeLoader

old_value = 0


def read_float32(client, fct_code, start_adress):
    if fct_code == 1:
        return decode_ieee(word_list_to_long(client.read_coils(start_adress, 2))[0])
    if fct_code == 2:
        return decode_ieee(word_list_to_long(client.read_discrete_inputs(start_adress, 2))[0])
    if fct_code == 3:
        return decode_ieee(word_list_to_long(client.read_holding_registers(start_adress, 2))[0])
    if fct_code == 4:
        return decode_ieee(word_list_to_long(client.read_input_registers(start_adress, 2))[0])
    else:
        print("Error fonction code")
        return           


def read_uint32(client, fct_code, start_adress):
    if fct_code == 1:
        return word_list_to_long(client.read_coils(start_adress, 2))[0]
    if fct_code == 2:
        return word_list_to_long(client.read_discrete_inputs(start_adress, 2))[0]
    if fct_code == 3:
        return word_list_to_long(client.read_holding_registers(start_adress, 2))[0]
    if fct_code == 4:
        return word_list_to_long(client.read_input_registers(start_adress, 2))[0]
    else:
        print("Error fonction code")
        return     


def read_uint16(client, fct_code, start_adress):
    if fct_code == 1:
        return client.read_coils(start_adress, 1)[0]
    if fct_code == 2:
        return client.read_discrete_inputs(start_adress, 1)[0]
    if fct_code == 3:
        return client.read_holding_registers(start_adress, 1)[0]
    if fct_code == 4:
        return client.read_input_registers(start_adress, 1)[0]
    else:
        print("Error fonction code")
        return     


def read_int16(client, fct_code, start_adress):
    if fct_code == 1:
        return get_2comp(client.read_coils(start_adress, 1)[0])
    if fct_code == 2:
        return get_2comp(client.read_discrete_inputs(start_adress, 1)[0])
    if fct_code == 3:
        return get_2comp(client.read_holding_registers(start_adress, 1)[0])
    if fct_code == 4:
        return get_2comp(client.read_input_registers(start_adress, 1)[0])
    else:
        print("Error fonction code")
        return   

def read_float64(client, fct_code, start_adress):
    if fct_code == 1:
        return decode_ieee(word_list_to_long(client.read_coils(start_adress, 4), long_long=True)[0], double=True)
    if fct_code == 2:
        return decode_ieee(word_list_to_long(client.read_discrete_inputs(start_adress, 4), long_long=True)[0], double=True)
    if fct_code == 3:
        return decode_ieee(word_list_to_long(client.read_holding_registers(start_adress, 4), long_long=True)[0], double=True)
    if fct_code == 4:
        return decode_ieee(word_list_to_long(client.read_input_registers(start_adress, 4), long_long=True)[0], double=True)
    else:
        print("Error fonction code")
        return               


def read_data(client, fct_code, start_adress, type):
    if type == "float32":
        return read_float32(client, fct_code, start_adress)
    if type == "uint32":
        return read_uint32(client, fct_code, start_adress)
    if type == "float64":
        return read_float64(client, fct_code, start_adress)        
    if type == "uint16":
        return read_uint16(client, fct_code, start_adress)  
    if type == "int16":
        return read_int16(client, fct_code, start_adress)  
    

class Counter:

    def __init__(self, name, type, host, port, unit_id, fct_code, address, out_type, factor):     

        self.name = name
        self.type = type
        self.counter_value = 0
        self.host = host
        self.port = port
        self.unit_id = unit_id
        self.fct_code = fct_code
        self.address = address
        self.out_type = out_type
        self.factor = factor

        client = ModbusClient(host=host, port=port, timeout=2.0, unit_id=unit_id)
        if client.open():
            self.total_value = read_data(client, fct_code, address, out_type) * factor
        client.close()
        self.old_value = self.total_value


    def get_value(self):

        client = ModbusClient(host=self.host, port=self.port, timeout=2.0, unit_id=self.unit_id)
        if client.open():
            self.total_value = read_data(client, self.fct_code, self.address, self.out_type) * self.factor
        client.close()
        self.counter_value += self.total_value - self.old_value
        self.old_value = self.total_value


    def reset_counter(self):
        self.counter_value = 0    
        

# Counters configurations

with open('modbus.yml') as f:
    config = yaml.load(f, Loader=SafeLoader)
    
counters = []    
for counter in config["counters"]:    
    counters.append(Counter(counter["name"], counter["type"], counter["host"], counter["port"], counter["unit"], counter["fct_code"], counter["address"], counter["out_type"], counter["factor"]))

# Resets

ACTUAL_DAY = datetime.datetime.now().day
def verify_date():
    global ACTUAL_DAY

    if datetime.datetime.now().day != ACTUAL_DAY:
        for counter in counters:
            counter.reset_counter()
        ACTUAL_DAY = datetime.datetime.now().day

# Prometheus generate metrics

class CustomCollector(object):
    def collect(self):

        c = GaugeMetricFamily('modbusTCP_values', 'Données des capteurs modbusTCP', labels=['name', 'type'])

        config = {}
        with open('modbus.yml') as f:
            config = yaml.load(f, Loader=SafeLoader)
                
        nbr_error = 0

        for device in config["devices"]:

            client = ModbusClient(host=device["host"], port=device["port"], timeout=2.0, unit_id=device["unit"])

            if client.open():

                for gauge in device["gauges"]:

                    try:
                        value = read_data(client, gauge["fct_code"], gauge["address"], gauge["type"]) * gauge["factor"]

                        print("[Info] - Scraped from device: {} gauge: {} value: {}".format(device["name"], gauge["name"], value))
                        c.add_metric([device["name"], gauge["name"]], value)
                        time.sleep(0.01)

                    except:
                        print("[Error] - Can't scrap device: {} gauge: {}".format(device["name"], gauge["name"]))
                        nbr_error += 1    

                client.close()
            else:
               print("[Error] - Unable to connect to the device host: {} port: {}".format(device["host"], device["port"])) 
               nbr_error += 1 

        if nbr_error > 0:
            print("[Warning] - Number of errors : {}".format(nbr_error))
            
        c.add_metric(["Errors", "count"], nbr_error)  

        # Counters scraping

        for counter in counters:
            counter.get_value()
            c.add_metric([counter.name, counter.type], counter.counter_value)

        verify_date()  

        yield c



if __name__ == "__main__":
    print("[Info] - Hosting metrics at port: 9400")

    start_http_server(9400)
    REGISTRY.register(CustomCollector())

    while True:
        time.sleep(1)

