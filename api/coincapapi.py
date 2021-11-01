import requests
import json
import time

# url = "https://api.coincap.io/v2/candles?exchange=poloniex&interval=h8&baseId=ethereum&quoteId=united-states-dollar"
url = "https://api.coincap.io/v2/candles?exchange=bitstamp&interval=m15&baseId=ethereum&quoteId=united-states-dollar&start=1565280000000&end=1565336472965"
payload = {}
headers = {}

print(time.time())
response = requests.request("GET", url, headers=headers, data=payload)

with open("result.json", "w") as f:
    json.dump(response.json(), f)
# print(response.text)
