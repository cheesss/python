import pybithumb
import datetime
import time

with open("bithumb_api.txt") as f:
    lines = f.readlines()
    key = lines[0].strip()
    secret = lines[1].strip()
    bithumb = pybithumb.Bithumb(key, secret)

#돌파전략 목표가 설정하기
def get_target_price(ticker):
    df = pybithumb.get_ohlcv(ticker)
    yesterday = df.iloc[-2]

    today_open = yesterday['close']
    yesterday_high = yesterday['high']
    yesterday_low = yesterday['low']
    target = today_open + (yesterday_high - yesterday_low) * 0.5
    return target

def buy_crypto_currency(ticker):
    if current_price > target_price:
        krw = bithumb.get_balance(ticker)[2]
        orderbook = pybithumb.get_orderbook(ticker)
        sell_price = orderbook['asks'][0]['price']
        unit = krw / float(sell_price)
        bithumb.buy_market_order(ticker, unit)

def sell_crypto_currency(ticker):
    unit = bithumb.get_balance(ticker)[0]
    bithumb.sell_market_order(ticker, unit)

def get_yesterday_ma5(ticker):
    df = pybithumb.get_ohlcv(ticker)
    close = df['close']
    ma = close.rolling(window=5).mean()
    return ma[-2]

# 자정에 목표가 갱신하기
now = datetime.datetime.now()
mid = datetime.datetime(now.year, now.month, now.day) + datetime.timedelta(1)
ma5 = get_yesterday_ma5("BTC")
target_price = get_target_price("BTC")



while True:
    try:
        now = datetime.datetime.now()
        if mid < now < mid + datetime.timedelta(seconds=10):
            target_price = get_target_price("BTC")
            mid = datetime.datetime(now.year, now.month, now.day) + datetime.timedelta(1)
            ma5 = get_yesterday_ma5("BTC")
            sell_crypto_currency("BTC")

        current_price = pybithumb.get_current_price("BTC")
        if (current_price > target_price) and (current_price > ma5):
            buy_crypto_currency("BTC")
    except:
        print("에러 발생")
    time.sleep(1)


import pybithumb
df = pybithumb.get_ohlcv("BTC")
df['range'] = (df['high'] - df['low']) * 0.5
df['target'] = df['open'] + df['range'].shift(1)
df.to_excel("btc.xlsx")



import pybithumb
import numpy as np

df = pybithumb.get_ohlcv("BTC")

df['ma5'] = df['close'].rolling(window=5).mean().shift(1)
df['range'] = (df['high'] - df['low']) * 0.5
df['target'] = df['open'] + df['range'].shift(1)
df['bull'] = df['open'] > df['ma5']

fee = 0.0032
df['ror'] = np.where((df['high'] > df['target']) & df['bull'],
                  df['close'] / df['target'] - fee,
                  1)

df['hpr'] = df['ror'].cumprod()
df['dd'] = (df['hpr'].cummax() - df['hpr']) / df['hpr'].cummax() * 100
print("MDD: ", df['dd'].max())
print("HPR: ", df['hpr'][-2])
df.to_excel("larry_ma.xlsx")