from api import getETHticker 
import datetime
from dingding_robot import DingDingRobot
import time
# def get_tick():
#     tick_json = getETHticker()
#     data = tick_json['data'][0]
#     timestamp = int(data['ts'])/1000
#     timestamp = time.localtime(timestamp)
#     trade_time = time.strftime("%Y-%m-%d %H:%M:%S", timestamp)
#     last_price = float(data['last'])
#     return trade_time,last_price

# while True:
#     time1,price1 = get_tick()
#     print(time1)
#     print(price1)
#     time.sleep(1)

# # def hundred_point_reminder(price):
# #     
# #     for i in hundred_point_ls:
# #         if price
# # hundred_point_reminder(1)


def hundred_check(last_price,hundred_record):
    fraction = last_price//100
    remainder = last_price%100
    if remainder<1 or abs(remainder-100)<1:
        if hundred_record == True:
            # robot.send()
            hundred_record = False
        return hundred_record
    elif remainder>5 or abs(remainder-100)<5:
        hundred_record =True
    return hundred_record
    




hundred_record = True
for last_price in [3990,3995,3999.3,4000.1,4003,4000.2,4006,4000.1]:
    print('-------------------------------')
    print(last_price)
    print(hundred_record)
    hundred_record = hundred_check(last_price,hundred_record)
