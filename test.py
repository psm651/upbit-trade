import pyupbit

access = "aQuzJPeK4X9npocwuD8QXa7ApwL5jgxSioq0O3x6"
secret = "KGE3D0lQQG8wL5OR3HI5BiSCnSuhyNfxZof0IN7j"
upbit = pyupbit.Upbit(access, secret)

#df = pyupbit.get_ohlcv(ticker, interval="day", count=1)
#print(df.index[0])
print(upbit.get_balance("TON"))
#print(upbit.get_balance("KRW-BTC"))
