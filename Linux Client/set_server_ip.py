import sqlite3

def set_server_ip():
    mydb = sqlite3.connect("Files.db")
    cur = mydb.cursor()
    Server_ip=input("Type server ip: ")
    cur.execute('''DELETE FROM Server_ip''')
    cur.execute("INSERT INTO Server_ip (server_ip) VALUES ('"+Server_ip+"')")
    cur.execute('''SELECT * FROM Server_ip''')
    for row in cur:
        print("Server_ip is set to "+row[0])
    mydb.commit()
    mydb.close()

if __name__ == "__main__":
	set_server_ip()


