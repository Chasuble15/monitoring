import os
import time
from GXDLMSReader import GXDLMSReader
from gurux_dlms.secure import GXDLMSSecureClient
from gurux_common.enums import TraceLevel
from gurux_common.io import Parity, StopBits, BaudRate
from gurux_serial.GXSerial import GXSerial
from gurux_dlms.enums import InterfaceType
import traceback
from gurux_dlms import GXDLMSException, GXDLMSExceptionResponse, GXDLMSConfirmedServiceError
from gurux_dlms.objects.GXDLMSObjectCollection import GXDLMSObjectCollection
from gurux_dlms.enums import ObjectType

from prometheus_client import start_http_server
from prometheus_client.core import GaugeMetricFamily, REGISTRY


def get_values(to_read, port):
    client = GXDLMSSecureClient(True)
    client.useLogicalNameReferencing = False
    client.interfaceType = InterfaceType.HDLC_WITH_MODE_E

    media = GXSerial(None)
    media.port = port
    media.baudRate = BaudRate.BAUD_RATE_300
    media.dataBits = 7
    media.parity = Parity.EVEN
    media.stopbits = StopBits.ONE


    trace = TraceLevel.INFO
    invocationCounter = None

    readObjects = []

    for o in to_read.split(";"):
        tmp = o.split(":")
        if len(tmp) != 2:
            raise ValueError("Invalid Logical name or attribute index.")
        readObjects.append((tmp[0].strip(), int(tmp[1].strip())))

    outputFile = "output.txt"


    try:

        reader = GXDLMSReader(client, media, trace, invocationCounter)
        media.open()
        print("Media open")

        if readObjects:
            read = False
            reader.initializeConnection()
            if outputFile and os.path.exists(outputFile):
                try:
                    c = GXDLMSObjectCollection.load(outputFile)
                    client.objects.extend(c)
                    if client.objects:
                        read = True
                except Exception:
                    read = False
            if not read:
                reader.getAssociationView()
                
            values = {}    
            for k, v in readObjects:
                obj = client.objects.findByLN(ObjectType.NONE, k)
                if obj is None:
                    raise Exception("Unknown logical name:" + k)
                
                val = reader.read(obj, v)
                
                values[f"{k}:{v}"] = val
                
                reader.showValue(v, val)
            if outputFile:
                client.objects.save(outputFile)
                
            return values  
            
        else:
            print("No object to read")
            # reader.readAll(outputFile)

    except (ValueError, GXDLMSException, GXDLMSExceptionResponse, GXDLMSConfirmedServiceError) as ex:
        print(ex)
    except (KeyboardInterrupt, SystemExit, Exception) as ex:
        traceback.print_exc()
        if media:
            media.close()
            reader = None
    finally:
        if reader:
            try:
                reader.close()
            except Exception:
                traceback.print_exc()
        print("Ended. Press any key to continue.")


class CustomCollector(object):
    def collect(self):

        c = GaugeMetricFamily('dlms_values', 'Données du compteur DLMS', labels=['name', 'type'])
        
        energy_address = "1.1.1.8.0.255:2"
        power_address = "1.1.16.7.0.255:2"
        port = "/dev/ttyUSB0"
        
        request_address = ";".join([energy_address, power_address])
        
        
        
        try:
            values = get_values(request_address, port)
            
            
            c.add_metric(["gap", "energy"], values[energy_address] * 60 / 327468)  
            c.add_metric(["gap", "power"], values[power_address] * 60)  
        except:
            
            print("[Error] - Verify the optical head or the addresses")    
        
        yield c
        
if __name__ == '__main__':
    
    print("[Info] - Hosting metrics at port: 9600")

    start_http_server(9600)
    REGISTRY.register(CustomCollector())
        
    # print(get_values("1.1.1.8.0.255:2;1.1.16.7.0.255:2"))
    while True:
        time.sleep(1)



# {'1.1.1.8.0.255:2': 904534303, '1.1.1.8.0.255:3': [0.1, <Unit.ACTIVE_ENERGY: 30>]}