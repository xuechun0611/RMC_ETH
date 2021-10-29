from api import getETHticker 
from datetime import datetime
from dingding_robot import DingDingRobot
import time

def change_reminder(time_stamps,time_price_dict):
    while True:
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        max_time = datetime.strptime(max(time_stamps),"%Y-%m-%d %H:%M:%S.%f")
        min_time = datetime.strptime(min(time_stamps),"%Y-%m-%d %H:%M:%S.%f")
        time_delta = (max_time - min_time).total_seconds()
        if time_delta>300.0:
            min_time = min(time_stamps)
            time_stamps.remove(min_time)
            del time_price_dict[min_time]
            continue
        else:
            prices = time_price_dict.values()
            avg_price = sum(time_price_dict.values())/len(time_price_dict.values())
            high = max(prices)
            low = min(prices)
            change = (high - low)/avg_price
            print(change*100)
            if change > 0.01:
                robot.send(f'行情提醒\n{now}\nETH近5分钟价格变化比例为{round(100*change,2)}%\n最高价：{high}\n最低价：{low}')
                time_stamps = []
                time_price_dict = dict()
            return time_stamps,time_price_dict
            break

# def hundred_point_reminder(price):


def get_tick():
    tick_json = getETHticker()
    data = tick_json['data'][0]
    timestamp = int(data['ts'])/1000
    trade_time = datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S.%f")
    last_price = float(data['last'])
    return trade_time,last_price



time_stamps = []
time_price_dict = dict()

robot_id = '9b6d23422bf3aab35a20040a87cf08b402bed8ef3cc189c1137de13fa6bb0eaf'
robot = DingDingRobot(robot_id)
while True:
    trade_time,last_price = get_tick()
    if trade_time not in time_stamps:
        time_stamps.append(trade_time)
        time_price_dict[trade_time] = last_price

    time_stamps,time_price_dict = change_reminder(time_stamps,time_price_dict)
    time.sleep(1)





