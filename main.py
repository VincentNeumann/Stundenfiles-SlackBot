import requests
import json
import pytz
from datetime import datetime, timedelta
from slack_sdk import WebClient


#BOT_NAME = 'stundenfiles'
URL="https://mcdn-a.akamaihd.net"
#https://mcdn-a.akamaihd.net/br/hf/7t/b1/b1_20230213T010000+0100.mp4


def construct_filename(prefix, directory, time):
    utc_dif = get_utc_dif(time)
    formatet_time = time.strftime("%Y:%m:%dT%H0000+" + utc_dif + ".mp4")
    filename = prefix + "_"  + str(formatet_time).replace(":","")
    return URL + directory + filename

def get_utc_dif(time):
    german_timezone = pytz.timezone('Europe/Berlin')
    offset = german_timezone.utcoffset(time)
    offset_string =  "0" + str(offset.seconds // 3600) + "00"
    return offset_string


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
    channel = get_channel()
    stations = get_stations()

    slack_bot = WebClient(token = token)
    failed = False
    for station in stations:
        #now = datetime.datetime.now(pytz.timezone("Europe/Berlin"))
        last_hour = datetime.now() - timedelta(hours=1)
        filename = construct_filename(station["prefix"], station["dir"], last_hour)
        
        message = ""
        if not file_exists(filename):

            message = '>*FAILURE*: For {0} the Stundenfile was not found: \n>{1}'.format(get_slackmessage(station), filename)
            slack_bot.chat_postMessage(channel = channel, text = message)
            failed = True
            print(message)

    if not failed:
        message = '>*SUCCESS*: All Stundenfiles found'
        slack_bot.chat_postMessage(channel = channel, text = message)
