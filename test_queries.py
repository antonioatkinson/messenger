import psycopg2 as p
import select

conn = p.connect("dbname=messaging user='postgres' password='' host='localhost' port=5433")
# cur = con.cursor()

import psycopg2.extensions

# conn = psycopg2.connect(DSN)
conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)

curs = conn.cursor()
curs.execute("LISTEN test_table;")

print "Waiting for notifications on channel 'test'"
while 1:
    if select.select([conn],[],[],5) == ([],[],[]):
        print "Timeout"
    else:
        conn.poll()
        while conn.notifies:
            notify = conn.notifies.pop(0)
            print "Got NOTIFY:", notify.pid, notify.channel, notify.payload
            curs.execute("INSERT INTO test_table(message) VALUES (%s);",
                    [notify.payload])
            # print "message", curs.execute("SELECT * FROM test_table;").fetchall()
