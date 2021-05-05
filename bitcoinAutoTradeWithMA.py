import time
import pyupbit
import datetime
import requests

r = open('tokens.txt', mode='rt', encoding='utf-8')
tokens = r.readlines()
r.close
access = str(tokens[0]).strip()
secret = str(tokens[1]).strip()
myToken = str(tokens[2]).strip()


def post_message(token, channel, text):
    """슬랙 메시지 전송"""
    reponse = requests.post("https://slack.com/api/chat.postMessage",
            headers={"Authorization": "Bearer "+token},
            data={"channel" : channel,"text" : text}
    )

def get_target_price(ticker, k):
    """변동성 돌파 전략으로 매수 목표가 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=2)
    target_price = df.iloc[0]['close'] + (df.iloc[0]['high'] - df.iloc[0]['low']) * k
    return target_price

def get_start_time(ticker):
    """시작 시간 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=1)
    start_time = df.index[0]
    return start_time

def get_daily_ma(ticker, day):
    """일별 이동 평균선 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=day)
    daily_ma = df['close'].rolling(day).mean().iloc[-1]
    return daily_ma

def get_balance(ticker):
    """잔고 조회"""
    balances = upbit.get_balances()
    for b in balances:
        if b['currency'] == ticker:
            if b['balance'] is not None:
                return float(b['balance'])
            else:
                return 0

def get_current_price(ticker):
    """현재가 조회"""
    return pyupbit.get_orderbook(tickers=ticker)[0]["orderbook_units"][0]["ask_price"]

# 로그인
upbit = pyupbit.Upbit(access, secret)
print("autotrade start")
post_message(myToken,"#coin", "Auto-Trade START")
coin_list = pyupbit.get_tickers(fiat="KRW")

# 자동매매 시작
while True:
    for coin in coin_list:
        try:
            now = datetime.datetime.now()
            start_time = get_start_time(coin)
            end_time = start_time + datetime.timedelta(days=1)
    
            #하루단위
            if start_time < now < end_time - datetime.timedelta(seconds=10):
                target_price = get_target_price(coin, 0.5)
                daily_ma = get_daily_ma(coin, 10)
                current_price = get_current_price(coin)
                if target_price < current_price and daily_ma < current_price:
                    krw = get_balance("KRW")
                    if krw > 5100:
                        buy_result = upbit.buy_market_order(coin, krw*0.9995)
                        post_message(myToken, "#coin", coin + "buy : "+str(buy_result))
            else:
                sell_coin = get_balance(coin)
                if sell_coin > 0.00008:
                    sell_result = upbit.sell_market_order(coin, sell_coin*0.9995)
                    post_message(myToken, "#coin", coin + " sell : "+str(buy_result))
            time.sleep(1)
        except Exception as e:
            print(e)
            post_message(myToken, "#coin", 'error error error!!!')
            time.sleep(5)
