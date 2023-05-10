import requests
import json
from datetime import datetime, timedelta, timezone, tzinfo
from slack_sdk import WebClient
#import pytz


#BOT_NAME = 'stundenfiles'
URL="https://mcdn-a.akamaihd.net"
#https://mcdn-a.akamaihd.net/br/hf/7t/b1/b1_20230213T010000+0100.mp4


def construct_filename(prefix, directory, time):
    formatet_time = time.strftime("%Y:%m:%dT%H0000+0200.mp4")
    filename = prefix + "_"  + str(formatet_time).replace(":","")
    return URL + directory + filename

def correct_filename(prefix, directory, time):
    formatet_time = time.strftime("%Y:%m:%dT%H0000+0200.mp4")
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

def get_slackmessage(station):
    return station["name"] + " " + station["slackIcon"] + " " 

if __name__ == "__main__":
    token = get_token()
    print(token)
    channel = get_channel()
    stations = get_stations()

    slack_bot = WebClient(token = token)
    
    for station in stations:
        #now = datetime.datetime.now(pytz.timezone("Europe/Berlin"))
        last_hour = datetime.now() - timedelta(hours=1)
        filename = construct_filename(station["prefix"], station["dir"], last_hour)
        message = ""
        if not file_exists(filename):
            message = f'>*FAILURE*: For {get_slackmessage(station)} the Stundenfile was not found: \n>{filename}'
        #elif file_exists(filename) != construct_filename(filename):
        #    message = f'>*FAILURE*: For {station["name"]} the Stundenfile is not valid: \n>{filename}'
            slack_bot.chat_postMessage(channel = channel, text = message)
            print(message)