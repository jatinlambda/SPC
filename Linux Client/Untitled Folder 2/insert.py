import sqlite3
import csv

conn=sqlite3.connect("ipl.db")
cur=conn.cursor()


f1=open('player.csv','r')
f2=open('team.csv','r')
f3=open('match.csv','r')
f4=open('player_match.csv','r')
f5=open('ball_by_ball.csv','r')

next(f1, None)
next(f2, None)
next(f3, None)
next(f4, None)
next(f5, None)
reader1 = csv.reader(f1)
reader2 = csv.reader(f2)
reader3 = csv.reader(f3)
reader4 = csv.reader(f4)
reader5 = csv.reader(f5)

for row in reader1:
    cur.execute("INSERT INTO PLAYER  VALUES (?,?,?,?,?,?)", row)
for row in reader2:
    cur.execute('''INSERT INTO TEAM VALUES (?,?)''', row)
for row in reader3:
    cur.execute('''INSERT INTO MATCH  VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''', row)
for row in reader4:
    cur.execute('''INSERT INTO PLAYER_MATCH  VALUES (?,?,?,?,?,?,?)''', row)
for row in reader5:
    cur.execute('''INSERT INTO BALL_BY_BALL  VALUES (?,?,?,?,?,?,?,?,?,?,?)''', row)
conn.commit()
conn.close()