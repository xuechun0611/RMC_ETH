# 资产
# for line in csv
#  if postion != empty:
#       check 达到收益率/强平
#       更新资产
#  else:
#       check MA 30 和价格低差异
#       if yes/no:
#           下单/开空
#           放在position

# symbol|trade_dt|trade_time|open_price|high_price|low_price|close_price
# |mean_price|volume|amount|trade_num|take_volume|take_amount
import os
import sys
import pandas as pd
import json

df = pd.read_csv("full_data.csv", sep="|")
position = []
history = []
volume_sum = []
amount_sum = []
ma30 = 0

# 参数
n = 0.05
single_bet = 100
lever = 20
total = 10000
expected_benefit = 0.5

# 只跑前lines行数据
lines = 50000
count = 0


def json_translate(
    price,
    amount,
    volume,
    lever,
    force_price,
    force=None,
    deal_price=None,
    time=None,
    total=None,
    ma30=None,
    start_time=None,
):
    return {
        "price": price,
        "amount/USDT": amount,
        "volume": volume,
        "lever": lever,
        "force": False,
        "force_price": force_price,
        "deal_price": deal_price,
        "time": time,
        "total": total,
        "ma30": ma30,
        "start_time": start_time,
    }


for row in df.iterrows():
    ma30 = row[1]["open_price"]
    count += 1
    if count == lines:
        break
    volume_sum.append(row[1]["volume"])
    amount_sum.append(row[1]["amount"])
    if row[0] >= 450:
        ma30 = sum(amount_sum) / sum(volume_sum)
        volume_sum.pop(0)
        amount_sum.pop(0)

    # 下单
    if row[1]["close_price"] - ma30 >= n * ma30 and position == []:
        # 开空
        j = json_translate(
            row[1]["close_price"],
            single_bet,
            -1 * single_bet * lever / row[1]["close_price"],
            lever,
            row[1]["close_price"]
            + single_bet / (single_bet * lever / row[1]["close_price"]),
            ma30=ma30,
            start_time=row[1]["trade_time"],
        )
        position.append(j)
        total -= single_bet
    elif ma30 - row[1]["close_price"] >= n * ma30 and position == []:
        # 开多
        j = json_translate(
            row[1]["close_price"],
            1 * single_bet,
            1 * single_bet * lever / row[1]["close_price"],
            lever,
            row[1]["close_price"]
            - single_bet / (single_bet * lever / row[1]["close_price"]),
            ma30=ma30,
            start_time=row[1]["trade_time"],
        )
        position.append(j)
        total -= single_bet

    if position != []:
        # check 强平
        if (
            row[1]["high_price"] >= position[0]["force_price"]
            and row[1]["low_price"] <= position[0]["force_price"]
        ):
            bad_move = position.pop(0)
            bad_move["deal_price"] = (row[1]["high_price"], row[1]["low_price"])
            bad_move["force"] = True
            bad_move["time"] = row[1]["trade_time"]
            bad_move["total"] = total
            history.append(bad_move)
            continue
        # check 收益
        benefit = (row[1]["close_price"] - position[0]["price"]) * position[0]["volume"]
        transaction_fee = benefit * 0.001
        if benefit >= expected_benefit * position[0]["amount/USDT"]:
            achieved = position.pop(0)
            achieved["deal_price"] = row[1]["close_price"]
            achieved["time"] = row[1]["trade_time"]
            # bad_move["force"] = False
            total += benefit - transaction_fee + single_bet
            achieved["total"] = total
            history.append(achieved)
    if total <= 0:
        break


with open("result.json", "w", encoding="utf-8") as f:
    json.dump(history, f, ensure_ascii=False, indent=4)

print(total)
print(history)
