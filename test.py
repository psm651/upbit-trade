import pyupbit
import sqlite3

access = "aQuzJPeK4X9npocwuD8QXa7ApwL5jgxSioq0O3x6"
secret = "KGE3D0lQQG8wL5OR3HI5BiSCnSuhyNfxZof0IN7j"
upbit = pyupbit.Upbit(access, secret)

conn = sqlite3.connect("upbit.dbs", isolation_level=None)

# 커서 획득
c = conn.cursor()

c.execute("SELECT * FROM daily_buy_list")
print(c.fetchone())

# 방법 1
#c.execute("SELECT * FROM table1 WHERE id=:id1 OR id=:id2", {"id1": 1, "id2": 4})
c.execute("SELECT * FROM table1")
for row in c.fetchall():
    print(row)

#df = pyupbit.get_ohlcv(ticker, interval="day", count=1)
#print(df.index[0])
#print(upbit.get_balance("TON"))
#print(upbit.get_balance("KRW-BTC"))
