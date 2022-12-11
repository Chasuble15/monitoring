from pyModbusTCP.client import ModbusClient
import time
from modbus_exporter import read_data

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



if __name__ == "__main__":

    test = Counter("PAC3200_Bureaux", "energy", "192.168.1.133", "502", 1, 3, 801, "float64", 0.001)
    print(test.counter_value)

    time.sleep(1)

    test.get_value()
    print(test.counter_value)

    time.sleep(1)

    test.get_value()
    print(test.counter_value)
    
    time.sleep(1)

    test.get_value()
    print(test.counter_value)

    time.sleep(1)

    test.reset_counter()
    print(test.counter_value)
    
    time.sleep(1)

    test.get_value()
    print(test.counter_value)
    

    time.sleep(1)

    test.get_value()
    print(test.counter_value)
    