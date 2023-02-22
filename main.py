import requests
import json
from datetime import datetime, timedelta

x = requests.get('https://mcdn-a.akamaihd.net/br/hf/7t/b1/')

#bayern1 testen

URL="https://mcdn-a.akamaihd.net/br/hf/7t/"
#https://mcdn-a.akamaihd.net/br/hf/7t/b1/b1_20230213T010000+0100.mp4
#b1_YYYYMMDDTHH0000+0100.mp4

def checkStation1hourago(station):
    now = datetime.now() - timedelta(hours=1)
    current_time = now.strftime("%Y:%m:%dT%H0000+0100.mp4")

    filename = ""
    filename = station + "/" + station + "_" 
    filename = filename + str(current_time).replace(":","")

    print(URL + filename)
    x = requests.get(URL + filename)

    if (x.status_code == 200):
        #success
        print("success")
    else:
        print("error")
        #slack nachricht

checkStation1hourago("b1")
checkStation1hourago("b3")
# print(x.content)

