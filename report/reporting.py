import requests
import datetime
import json
from reportgenerator import generate_report

data = {
    "maintitle": "Rapport d'énergie",
    "date": "",
    "tables": [{
        "title": "GAP Engineering",
        "fields": [
            {"label": "Total", "value": 0.001, "pie": False, "query": 'dlms_values{type="energy"}'},
            {"label": "Halle", "value": 0.001, "pie": True, "query": 'calc:halle_energy'},
            {"label": "Bureaux", "value": 0.001, "pie": True, "query": 'modbusTCP_values{name="PAC3200_Bureaux", type="energy"}'}
        ]
    }, {
        "title": "Halle",
        "fields": [
            {"label": "Chargeur véhicule", "value": 0.001, "pie": True, "query": 'modbusTCP_values{name="Chargeur_vehicule", type="energy"}'},
            {"label": "Pompe à chaleur", "value": 0.001, "pie": True, "query": 'modbusTCP_values{name="PAC", type="energy"}'},
            {"label": "Boiler sanitaire", "value": 0.001, "pie": True, "query": 'modbusTCP_values{name="PAC2200_Sanitaire", type="energy"}'},
            {"label": "UPS1", "value": 0.001, "pie": True, "query": 'modbusTCP_values{name="UPS1", type="energy"}'},
            {"label": "UPS2", "value": 0.001, "pie": True, "query": 'modbusTCP_values{name="UPS2", type="energy"}'},
            {"label": "UPS3", "value": 0.001, "pie": True, "query": 'modbusTCP_values{name="UPS3", type="energy"}'},
        ]
    }]
}

def date_to_unix(date):
    # given_date = "8/6/2022, 05:54:8"
    formated_date = datetime.datetime.strptime(date,"%d/%m/%Y, %H:%M:%S")
    return str(round(datetime.datetime.timestamp(formated_date)))


def get_from_range(query, start_time, end_time, step):

    r = requests.get("http://192.168.1.143:9090/api/v1/query_range?query={}&start={}&end={}&step={}".format(
        query, 
        date_to_unix(start_time),
        date_to_unix(end_time),
        step))

    print('Status code:', r.status_code)
    # print(r.text)

    return json.loads(r.text)["data"]["result"][0]["values"]

	
 
def est_croissant(liste):
    for i in range(len(liste)-1):
        if not liste[i] <= liste[i+1]:
            return False
    return True


if __name__ == "__main__":

    start_time = "01/11/2022, 12:00:00"
    end_time = "14/11/2022, 08:00:00"
    step = '10m'
    
    data["date"] = f"{start_time[:10]}  -  {end_time[:10]}"


    for table in data["tables"]:
        for field in table["fields"]:
            
            if "query" in field.keys():
                values = get_from_range(field["query"], start_time, end_time, step)
                energies = [i[1] for i in values]
            
                # verify the reset
            
                if est_croissant(energies):

                    monthly_energy = int(float(energies[-1:][0]) - float(energies[0]))
                    print(monthly_energy)
                    field["value"] = monthly_energy

                # holding the reset
                else:
                    print("Error, a reset has occured during this month")
        
    
    generate_report(data)


