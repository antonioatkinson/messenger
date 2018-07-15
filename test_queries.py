import psycopg2 as p
import select
from multiprocessing import Process
import sys
import threading
import time

conn = p.connect("dbname=messaging user='postgres' password='' host='localhost' port=5433")
# cur = con.cursor()

import psycopg2.extensions

def func1():
    # conn = psycopg2.connect(DSN)
    conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)

    curs = conn.cursor()
    curs.execute("LISTEN test_table;")

    print "Waiting for notifications on channel 'test'"
    while 1:
        # if select.select([conn],[],[],5) == ([],[],[]):
        #     print "Timeout"
        # else:
        #     conn.poll()
        #     while conn.notifies:
        #         notify = conn.notifies.pop(0)
        #         print "Got NOTIFY:", notify.pid, notify.channel, notify.payload
        #         arr = curs.execute("SELECT * FROM test_table")
        #         print curs.fetchall()
        #         print "message: ", notify.payload

        if select.select([conn],[],[],5) != ([],[],[]):
            conn.poll()
            while conn.notifies:
                notify = conn.notifies.pop(0)
                print "Got NOTIFY:", notify.pid, notify.channel, notify.payload
                arr = curs.execute("SELECT * FROM test_table")
                print curs.fetchall()
                print "message: ", notify.payload

# now threading1 runs regardless of user input
threading1 = threading.Thread(target=func1)
threading1.daemon = True
threading1.start()

conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)

cur = conn.cursor()

while 1:
    var = raw_input("Enter your message: ")
    print (var)
    cur.execute("INSERT INTO test_table(message) VALUES (%s);",
                        [var])
    conn.commit()
    cur.execute("NOTIFY test_table, %s;",
                        [var])
