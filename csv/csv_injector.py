import requests
import csv
import time

headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
}



# data = 'GOOG,2,2022-11-30T00:00:00+01:00'
# format = "1:label:ticker,2:metric:ask,3:time:rfc3339"
numlines = 1
with open("20221202_083718__nergie active totale import_e tarif_1.csv", 'r') as f:
    numlines = len(f.readlines())

with open("20221202_083718__nergie active totale import_e tarif_1.csv", 'r') as f:
    reader = csv.reader(f, delimiter=';', quotechar='|')
    
    for i, row in enumerate(reader):
        # get only the content
        if i > 1:
            value = row[4].replace(",", ".")    
            
            data = f"{row[0]},{value},{row[6]}"
            format = "1:time:rfc3339,2:metric:compteur,3:label:unit"

            response = requests.post(f'http://192.168.1.143:8428/api/v1/import/csv?format={format}', headers=headers, data=data)
            # print(f"Status code: {response.status_code}")
            
            percent = round(i / numlines * 100, 2)
            print(f"Progression: {percent}%", end="\r")
            
            time.sleep(0.01)
            # if i % 5000 == 0:
            #     time.sleep(6)
            
            