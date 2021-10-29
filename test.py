from api import getETHticker 
import datetime
from dingding_robot import DingDingRobot
import time
def get_tick():
    tick_json = getETHticker()
    data = tick_json['data'][0]
    timestamp = int(data['ts'])/1000
    timestamp = time.localtime(timestamp)
    trade_time = time.strftime("%Y-%m-%d %H:%M:%S", timestamp)
    last_price = float(data['last'])
    return trade_time,last_price

while True:
    time1,price1 = get_tick()
    print(time1)
    print(price1)
    time.sleep(1)

# def hundred_point_reminder(price):
#     
#     for i in hundred_point_ls:
#         if price
# hundred_point_reminder(1)