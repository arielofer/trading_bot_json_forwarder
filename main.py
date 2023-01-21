import json
from time import sleep
from urllib.error import HTTPError
from authenticate import gmail_authenticate
from searcher import search_messages
from reader import read_message
from deleter import delete_messages
from requests import post


def main():
    our_bot_url = "https://app.3commas.io/trade_signal/trading_view"
    query = "from:TradingView subject:alert()"

    while True:
        # get the Gmail API service
        service = gmail_authenticate()
        print("[INFO]: success - connected to gmail")

        # get emails that match the query you specify
        print(f"[INFO] searching for messages with following query: {query}")
        result = search_messages(service, query)
        print(f"found {len(result)} results!")

        if len(result):
            for msg in result:
                read_message(service, msg)

                alert_json = ""

                try:
                    with open("alert_json.txt", "rt") as f:
                        alert_json = f.read()

                    print("[INFO]: sending the command")
                    response = post(
                        url=our_bot_url,
                        json=json.loads(" ".join(alert_json.split())))

                    if response.status_code == 200:
                        print("[INFO]: message sent successfully ")

                        # clean the text file
                        with open("alert_json.txt", "wt") as f:
                            f.write("")

                        # # delete the message
                        print("[INFO]: going to deletion phase")
                        delete_messages(service, msg)
                    else:
                        print("[ERROR]: the message wasn't sent properly"
                              " check the reciever url inserted is correct")
                except json.JSONDecodeError as err:
                    print("[ERROR]: couldn't load the alert json:")
                    print(err)
                except HTTPError as err:
                    print("problem connecting to the mail server:")
                    print(err)

        sleep(60.0)
