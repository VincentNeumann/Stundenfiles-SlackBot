import json
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError


class Slack:
    def __init__(self, token, botname):
        self.botname = botname
        self.client = WebClient(token)
        # users = self.slack.api_call("users.list")
        # for user in users["members"]:
        #     if user["name"] == self.botname:
        #         self.userid = user["id"]

    def create_field(self, title, value, short):
        print("not implementet")
        field = {
            "title": title,
            "value": value,
            "short": short
        }
        return field

    def create_attachment(self, fallback, title, title_link, fields, image_url):
        print("not implementet")
        attachment = {
            "fallback" : fallback,
            "title": title,
            "title_link": title_link,
            "fields": fields,
            "image_url": image_url,
            "color": "#1F9CD5"
        }

        return json.dumps([attachment])

    def post_message(self, message, channel):
        # auth_test = client.auth_test()
        # bot_user_id = auth_test["user_id"]
        # print(f"App's bot user: {bot_user_id}")
        try:
            result = self.client.chat_postMessage(
                channel=channel,
                text=message
                # You could also use a blocks[] array to send richer content
            )
            # Print result, which includes information about the message (like TS)
        except SlackApiError as e:
            print(f"Error: {e}")
        return result
    
    def post_attachment(self, attachment, channel):
        print("not implementet")