#!/usr/bin/env python
from slack_sdk import Slack
import json

f = open('secret.json')
secrets = json.load(f)
f.close()

API_TOKEN = secrets["API_TOKEN"]
CHANNEL_ID = secrets["CHANNEL_ID"]
BOT_NAME = 'stundenfiles'




bot = Slack(API_TOKEN, BOT_NAME)
bot.post_message("Hello World", CHANNEL_ID)


