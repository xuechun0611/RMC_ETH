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
            if change > 0.01:
                robot.send(f'行情提醒\n{now}\nETH近5分钟价格变化比例为{round(100*change,2)}%\n最高价：{high}\n最低价：{low}')
                time_stamps = []
                time_price_dict = dict()
            change_ratio = round(change*100,5)
            return time_stamps,time_price_dict,change_ratio
            break

# def hundred_point_reminder(price):



def get_tick():
    tick_json = getETHticker()
    data = tick_json['data'][0]
    timestamp = int(data['ts'])/1000
    trade_time = datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S.%f")
    last_price = float(data['last'])
    return trade_time,last_price

def hundred_check(last_price,hundred_record):
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    fraction = last_price//100
    remainder = last_price%100
    if remainder<1 or abs(remainder-100)<1:
        if hundred_record == True:
            robot.send(f'行情提醒\n{now}\n当前ETH价格为:{last_price}')
            hundred_record = False
        return hundred_record
    elif remainder>5 or abs(remainder-100)<5:
        hundred_record =True
    return hundred_record

time_stamps = []
time_price_dict = dict()
hundred_record = True

robot_id = '9b6d23422bf3aab35a20040a87cf08b402bed8ef3cc189c1137de13fa6bb0eaf'
robot = DingDingRobot(robot_id)
while True:
    trade_time,last_price = get_tick()
    if trade_time not in time_stamps:
        time_stamps.append(trade_time)
        time_price_dict[trade_time] = last_price
    time_stamps,time_price_dict,change_ratio = change_reminder(time_stamps,time_price_dict)
    hundred_record = hundred_check(last_price,hundred_record)
    print('ETH行情')
    print(trade_time.split('.')[0])
    print(f'最新价：{last_price}')
    print(f'5min变化率：{change_ratio}%')
    print('\n')
    time.sleep(1)





