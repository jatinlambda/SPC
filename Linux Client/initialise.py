import sqlite3
import getpass


if __name__ == "__main__":

    mydb = sqlite3.connect("Files.db")
    cur = mydb.cursor()

    cur.execute('''CREATE TABLE Files (filepath varchar(200) Primary key,
    sha256 varchar(64), stamp timestamp)''')
    cur.execute('''CREATE TABLE User (name varchar(200) Primary key,
    password varchar(200))''')
    cur.execute('''CREATE TABLE Root (root varchar(200))''')
    cur.execute('''CREATE TABLE Server_ip (server_ip varchar(200))''')
    username = 'jatin'
    password = 'jatin1234'
    # username=input("Enter Username: ")
    # while True:
    #     password=getpass.getpass("Enter Password: ")
    #     confirmpassword=getpass.getpass("Confirm Password: ")
    #     if confirmpassword==password:
    #         break

    root=input("Observing directory path: ")
    if root[-1]!='/':
    	root=root+'/'
    cur.execute("INSERT INTO Root (root) VALUES ('"+root+"')")
    cur.execute("INSERT INTO User  VALUES (?, ?)", (username,password))
    cur.execute("INSERT INTO Server_ip (server_ip) VALUES ('http://127.0.0.1:8000/')")

    # cur.execute('''SELECT * FROM User''')
    # for row in cur:
    #     print(row)
    mydb.commit()
    mydb.close()
