import sqlite3

conn=sqlite3.connect("ipl.db")
cur=conn.cursor()


cur.execute('''WITH A
     AS
        (SELECT player_id AS oldid1, player_name
         FROM PLAYER
        ),
     B
     AS
        (SELECT COUNT(runs_scored) as count1, striker AS oldid
         FROM BALL_BY_BALL
         WHERE runs_scored=6
         
         GROUP BY striker
         
        ),
     C
     AS
        (SElECT COUNT(ball_id) as count2, striker AS newid
         FROM BALL_BY_BALL
         GROUP BY striker
        ),
     D
     AS
        (SElECT C.newid as id1, IFNULL(B.count1,0) as c1, C.count2 as c2
         FROM C
         LEFT JOIN B ON C.newid=B.oldid
        )
     
     SELECT D.id1 , A.player_name, D.c1, D.c2, 1.0*(D.c1)/D.c2
     FROM D
     INNER JOIN A ON A.oldid1 = D.id1
     ORDER BY 5 DESC 
     ;''')
for row in cur:
    print(str(row[0])+","+row[1]+","+str(row[2])+","+str(row[3])+","+str(row[4]))

