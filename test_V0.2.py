import os
import sys
import pandas as pd
import json
import csv
import pandas as pd


def record_paras(win_num, loss_num, trade_num, total, ma_para, limit, bet_ratio):
    win_rate = win_num / (win_num + loss_num)
    with open("para_record.txt", "a+") as f:
        f.write(f"win rate: {win_rate}\n")
        f.write(f"trade number: {trade_num}\n")
        f.write(f"fianl amount: {total}\n")
        f.write(f"MA para: {ma_para}\n")
        f.write(f"limit para: {limit}\n")
        f.write(f"bet fraction : {bet_ratio}\n")
        f.write("\n")


def data_name(limit, ma_para, bet_ratio):
    return f"ETH_{limit}_{ma_para}_{bet_ratio}.csv"


def init_csv(limit, ma_para, bet_ratio):
    file = data_name(limit, ma_para, bet_ratio)
    df = pd.DataFrame(
        columns=[
            "trade_time1",
            "buy_price",
            "sell_price",
            "loss_price",
            "ma_price",
            "buy_amount",
            "pre_total",
            "current_total",
            "trade_time2",
            "win",
        ]
    )
    df.to_csv(file, index=False)


def record_data(dict, file_name):
    ls = list(dict.values())
    with open(file_name, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(ls)


df = pd.read_csv("full_data.csv", sep="|")

position = []
history = []

long_order = {}
short_order = {}

volume_ls = []
amount_ls = []

win_num = 0
loss_num = 0
trade_num = 0


# 参数
# n = 0.08
# single_bet = 100
# lever = 125
total = 10000
limit = 0.05
long_limit = 1 + limit
short_limit = 1 - limit
bet_ratio = 0.6
ma_para = 450

# 只跑前lines行数据
lines = 5000
count = 0

init_csv(limit, ma_para, bet_ratio)
for min_data in df.iterrows():
    count += 1
    if count == lines:
        break
    min_data = min_data[1]
    trade_time = min_data["trade_time"]
    volume_ls.append(min_data["volume"])
    amount_ls.append(min_data["amount"])
    if len(volume_ls) > ma_para:

        ma_price = sum(amount_ls) / sum(volume_ls)
        volume_ls.pop(0)
        amount_ls.pop(0)

        # 多单处理
        # print(ma_price)
        # continue
        if long_order == {}:
            if (
                min_data["mean_price"] < short_limit * ma_price
                and min_data["low_price"] < 0.99 * min_data["mean_price"]
            ):
                # 止盈价
                buy_price = 0.99 * min_data["mean_price"]
                sell_price = buy_price * 1.0108
                loss_price = buy_price * 0.99
                buy_amount = total * bet_ratio
                pre_total = total
                total = total - buy_amount
                long_order = {
                    "trade_time1": trade_time,
                    "buy_price": buy_price,
                    "sell_price": sell_price,
                    "loss_price": loss_price,
                    "ma_price": ma_price,
                    "buy_amount": buy_amount,
                    "pre_total": pre_total,
                }
                trade_num += 1
                # print('ma: '+str(long_order['ma_price']))
                # print('buy: '+str(long_order['buy_price']))

        elif long_order != {}:
            file_name = data_name(limit, ma_para, bet_ratio)
            if min_data["high_price"] > long_order["sell_price"]:
                win_num += 1
                total = total + 2 * long_order["buy_amount"]
                long_order["current_total"] = total
                long_order["trade_time2"] = trade_time
                long_order["win"] = True
                record_data(long_order, file_name)
                long_order = {}
                print(
                    f"{trade_time}|{win_num/(win_num+loss_num)}|{trade_num}|{total}|win"
                )
            elif min_data["low_price"] < long_order["loss_price"]:
                loss_num += 1
                long_order["current_total"] = total
                long_order["trade_time2"] = trade_time
                long_order["win"] = False
                record_data(long_order, file_name)
                long_order = {}
                print(
                    f"{trade_time}|{win_num/(win_num+loss_num)}|{trade_num}|{total}|loss"
                )

        # 空单处理
        if short_order == {}:
            if (
                min_data["mean_price"] > long_limit * ma_price
                and min_data["high_price"] > 1.01 * min_data["mean_price"]
            ):
                # 止盈价
                buy_price = min_data["mean_price"] * 1.01
                sell_price = buy_price * 0.9892
                loss_price = buy_price * 1.01
                buy_amount = total * bet_ratio
                pre_total = total
                total = total - buy_amount
                short_order = {
                    "trade_time1": trade_time,
                    "buy_price": buy_price,
                    "sell_price": sell_price,
                    "loss_price": loss_price,
                    "ma_price": ma_price,
                    "buy_amount": buy_amount,
                    "pre_total": pre_total,
                }
                # print('ma: '+str(short_order['ma_price']))
                # print('buy: '+str(short_order['buy_price']))
                trade_num += 1

        elif short_order != {}:
            file_name = data_name(limit, ma_para, bet_ratio)
            if min_data["low_price"] < short_order["sell_price"]:

                win_num += 1
                total = total + short_order["buy_amount"] * 2
                short_order["current_total"] = total
                short_order["trade_time2"] = trade_time
                short_order["win"] = True
                record_data(short_order, file_name)
                short_order = {}
                print(
                    f"{trade_time}|{win_num/(win_num+loss_num)}|{trade_num}|{total}|win"
                )
            elif min_data["high_price"] > short_order["loss_price"]:
                loss_num += 1
                short_order["current_total"] = total
                short_order["trade_time2"] = trade_time
                short_order["win"] = False
                record_data(short_order, file_name)
                short_order = {}
                print(
                    f"{trade_time}|{win_num/(win_num+loss_num)}|{trade_num}|{total}|loss"
                )


# record_paras(win_num, loss_num, trade_num, total, ma_para, limit, bet_ratio)
