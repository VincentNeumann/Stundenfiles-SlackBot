import requests
import json
from datetime import datetime, timedelta
from slack import Slack

BOT_NAME = 'stundenfiles'
URL="https://mcdn-a.akamaihd.net"
#https://mcdn-a.akamaihd.net/br/hf/7t/b1/b1_20230213T010000+0100.mp4


def construct_filename(prefix, directory, time):
    formatet_time = time.strftime("%Y:%m:%dT%H0000+0100.mp4")
    filename = prefix + "_"  + str(formatet_time).replace(":","")
    return URL + directory + filename

def file_exists(url):
    res = requests.get(url)
    exists = False
    if (res.status_code == 200):
        exists = True
    else:
        exists = False
    return exists

def get_token():
    f = open('secret.json')
    secrets = json.load(f)
    token = secrets["API_TOKEN"]
    f.close()
    return token

def get_channel():
    f = open('secret.json')
    secrets = json.load(f)
    channel = secrets["CHANNEL_ID"]
    f.close()
    return channel

def get_stations():
    f = open('stations.json')
    stations = json.load(f)
    f.close()
    return stations["stations"]

if __name__ == "__main__":
    token = get_token()
    channel = get_channel()
    stations = get_stations()

    slack_bot = Slack(token, BOT_NAME)
    
    for station in stations:
        last_hour = datetime.now() - timedelta(hours=1)
        filename = construct_filename(station["prefix"], station["dir"], last_hour)
        message = ""
        if file_exists(filename):
            message = f'>SUCCESS: For {station["name"]} the Stundenfile was found: \n>{filename}'
        else:
            message = f'>*FAILURE*: For {station["name"]} the Stundenfile was not found: \n>{filename}'
        slack_bot.post_message(message, channel)    
        


