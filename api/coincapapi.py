import requests
import json
import time
from datetime import datetime
# # url = "https://api.coincap.io/v2/candles?exchange=poloniex&interval=h8&baseId=ethereum&quoteId=united-states-dollar"
# url = "https://api.coincap.io/v2/candles?exchange=bitstamp&interval=m15&baseId=ethereum&quoteId=united-states-dollar&start=1565280000000&end=1565336472965"
# payload = {}
# headers = {}

# print(time.time())
# response = requests.request("GET", url, headers=headers, data=payload)

# with open("result.json", "w") as f:
#     json.dump(response.json(), f)
# # print(response.text)

def unix_to_regular(unix_time):
    regular_time = time.localtime(float(unix_time/1000))
    regular_time = time.strftime('%Y-%m-%d %H:%M:%S',regular_time)
    return regular_time

def regular_to_unix(regular_time):
    unix_time = datetime.strptime(regular_time,'%Y-%m-%d %H:%M:%S').timetuple()
    unix_time = int(time.mktime(unix_time)*1000)
    return unix_time
print(unix_to_regular(1528410925000))
print(regular_to_unix('2018-06-08 06:35:25'))