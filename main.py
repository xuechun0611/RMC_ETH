from api import getETHticker
from datetime import datetime
from dingding_robot import DingDingRobot
import time
import pandas as pd

def change_reminder(time_stamps, time_price_dict):
    while True:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        max_time = datetime.strptime(max(time_stamps), "%Y-%m-%d %H:%M:%S.%f")
        min_time = datetime.strptime(min(time_stamps), "%Y-%m-%d %H:%M:%S.%f")
        time_delta = (max_time - min_time).total_seconds()
        if time_delta > 300.0:
            min_time = min(time_stamps)
            time_stamps.remove(min_time)
            del time_price_dict[min_time]
            continue
        else:
            prices = time_price_dict.values()
            last_price = list(prices)[-1]
            avg_price = sum(time_price_dict.values()) / len(time_price_dict.values())
            high = max(prices)
            low = min(prices)
            change = (high - low) / avg_price
            if change > 0.006:
                robot.send(
                    f"关键行情提醒\n{now}\nETH近5分钟价格变化比例为{round(100*change,2)}%\n最高价：{high}\n最低价：{low}\n最新价：{last_price}"
                )
                time_stamps = []
                time_price_dict = dict()
            change_ratio = round(change * 100, 5)
            return time_stamps, time_price_dict, change_ratio
            break


# def hundred_point_reminder(price):


def get_tick():
    tick_json = getETHticker()
    data = tick_json["data"][0]
    timestamp = int(data["ts"]) / 1000
    trade_time = datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S.%f")
    last_price = float(data["last"])
    return trade_time, last_price


def hundred_check(last_price, hundred_record):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    fraction = last_price // 100
    remainder = last_price % 100
    if remainder < 1 or abs(remainder - 100) < 1:
        if hundred_record == True:
            robot.send(f"行情提醒\n{now}\n当前ETH价格为:{last_price}")
            hundred_record = False
        return hundred_record
    elif remainder > 5 or abs(remainder - 100) > 5:
        hundred_record = True
    return hundred_record

def notification_time_ls(freq):
    time_ls = pd.date_range('00:00:00', '23:59:59',freq=freq).strftime('%H:%M:%S').to_list()
    return time_ls

def regular_notification(notification_time_ls,next_notification,last_price):
    now = datetime.now().strftime("%H:%M:%S")
    if next_notification == '' or now>next_notification:
        next_notification_ls = [i for i in notification_time_ls if i>now]
        if len(next_notification_ls) != 0:
            next_notification = next_notification_ls[0]
        else:
            next_notification = '00:00:00'
        robot.send(f"行情提醒\n{now}\n当前ETH价格为:{last_price}")
    return next_notification





time_stamps = []
time_price_dict = dict()
hundred_record = True
notification_time_ls = notification_time_ls('15min')
next_notification = ''

robot_id = "9b6d23422bf3aab35a20040a87cf08b402bed8ef3cc189c1137de13fa6bb0eaf"
robot = DingDingRobot(robot_id)

while True:
    try:
        trade_time, last_price = get_tick()
        if trade_time not in time_stamps:
            time_stamps.append(trade_time)
            time_price_dict[trade_time] = last_price
        time_stamps, time_price_dict, change_ratio = change_reminder(
            time_stamps, time_price_dict
        )
        hundred_record = hundred_check(last_price, hundred_record)
        next_notification = regular_notification(notification_time_ls,next_notification,last_price)

        print("ETH行情")
        print(trade_time.split(".")[0])
        print(f"最新价：{last_price}")
        print(f"5min变化率：{change_ratio}%")
        print("\n")
        time.sleep(1)
    except Exception as e:
        robot.send(f'ERROR:ETH实时行情系统出错\n' +
                   f'错误信息: {str(e)}')

