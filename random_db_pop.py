#!/usr/bin/env python3
#sqlite random db population

import random
import sqlite3
from sqlite3 import Error
conn = sqlite3.connect('rand_db_pop.db')
c = conn.cursor()
c.execute('''CREATE TABLE stocks (id text, date text, trans text, symbol text, qty real, price real)''')

def insert_row(db_row_data):
    try:
        c.execute(db_row_data)
    except:
        raise
    conn.commit()

def rand_row():
    tid = ''.join(random.SystemRandom().sample('abcdef0123456789', 12))
    date_str = '2018-{}-{}'.format(random.randint(1, 12), random.randint(1, 20))
    actn = random.choice(['BUY','SELL'])
    stock_name = random.choice(['PYPL','GOOG','MSFT','APPL','RAYT','FRYS','FOXC','BFFT'])
    action_string = [tid,date_str,actn,stock_name,random.randint(1,500),float('{}.{}'.format(random.randint(10,400), random.randint(00,99)))]
    return str(action_string).strip('[]').replace(' ','')

if __name__ == '__main__':
    #valuex = "INSERT INTO stocks VALUES ('2006-01-05','BUY','RHAT',100,35.14)"
    for _ in range(1,50):
        rand_data = "INSERT INTO stocks VALUES ({})".format(rand_row())
        insert_row(rand_data)
    c.execute("SELECT * FROM stocks")
    print(str(c.fetchall()).replace('),',')\n'))
    conn.close()
