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
    time.sleep(60)
    time2,price2 = get_tick()
    change = abs((price1-price2)/price1)
    if change>0.01:
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S ')
        robot_id = '9b6d23422bf3aab35a20040a87cf08b402bed8ef3cc189c1137de13fa6bb0eaf'
        robot = DingDingRobot(robot_id)
        response = robot.send(f'行情提醒{now} ETH近一分钟价格变化比例为{change}请注意！')

