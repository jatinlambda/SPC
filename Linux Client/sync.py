#! /usr/bin/python3
import requests
import getpass
import os
import hashlib
import json
import sqlite3
import os.path as osp


server_ip='http://127.0.0.1:8000/'
observing_root='./'
username=None
password=None
    
def filehash(filepath):
    blocksize = 64*1024
    sha = hashlib.sha256()
    with open(filepath, 'rb') as fp:
        while True:
            data = fp.read(blocksize)
            if not data:
                break
            sha.update(data)
    return sha.hexdigest() 

def main():
	mydb = sqlite3.connect("Files.db")
	cur = mydb.cursor()
	cur.execute('''SELECT * FROM Server_ip''')
	for row in cur:
	    print("Server_ip is set to "+row[0])
	    server_ip=row[0]


	cur.execute('''SELECT * FROM Root''')
	for row in cur:
	    print("Observing "+row[0] +" directory")
	    observing_root=row[0]


	cur.execute('''SELECT * FROM User''')
	for row in cur:
	    username=row[0]
	    password=row[1]

	list_of_files=[]
	list_of_dbfiles=[]

	for root, dirs, files in os.walk(observing_root):
		for fpath in [osp.join(root, f) for f in files]:
			name = osp.relpath(fpath, observing_root)
			list_of_files.append(name)

		for fpath in [osp.join(root, f) for f in dirs]:
			if not os.listdir(fpath):
				name = osp.relpath(fpath, observing_root)
				list_of_files.append(name)

		# for pair in list_of_files:
		# 	print(pair)

	cur.execute('''SELECT * FROM Files''')
	for row in cur:
		list_of_dbfiles.append(row[0])

	# print(list_of_dbfiles)
	# print(list_of_files)

	for file in list_of_dbfiles:
		if file not in list_of_files:
			cur.execute('''DELETE FROM Files WHERE filepath="'''+file+'"')
			print(file +' (deleted)')

	for file in list_of_files:
		if file not in list_of_dbfiles:
			if os.path.isdir(observing_root+file):
				sha256 = None
				stamp = None
			else:
				sha256 = filehash(observing_root+file)      ##### check
				stamp = os.path.getmtime(observing_root+file)
			cur.execute("INSERT INTO Files (filepath, sha256, stamp) VALUES (?,?,?)",[file,sha256,str(stamp)])
			print(file +' (added)')

	for file in list_of_files:
		if file in list_of_dbfiles:
			if os.path.isdir(observing_root+file):
				continue
			else:
				stamp = os.path.getmtime(observing_root+file)
				cur.execute('''SELECT * FROM Files WHERE filepath="'''+ file +'"')
				dbstamp=None
				for row in cur:
					dbstamp=row[2]
				if dbstamp<stamp:
					sha256 = filehash(observing_root+file)      
					cur.execute("UPDATE Files SET stamp='"+str(stamp)+"' , sha256='"+sha256+"' WHERE filepath='"+file+"'")
					print(file +' (modified)')
				# else:
				# 	print(file +' (no need to update database)')

	# URL_login = server_ip+'accounts/login/'
	URL_login = server_ip+'api-auth/login/'
	client = requests.session()

	# Retrieve the CSRF token first
	client.get(URL_login)  # sets cookie
	if 'csrftoken' in client.cookies:
	    csrftoken = client.cookies['csrftoken']

	# login_data = dict(username=input('Username: '), password=getpass.getpass(), csrfmiddlewaretoken=csrftoken, next='/')
	login_data = dict(username=username, password=password, csrfmiddlewaretoken=csrftoken, next='')
	r = client.post(URL_login, data=login_data, headers=dict(Referer=URL_login))

	# print(r.text)
	# print(r.headers)
	def detailurl(path):
	    if path[-1]=='/':
	        return server_ip+'api/file/'+path
	    else:
	        return server_ip+'api/file/'+path+'/'

	def getlist():
	    r=client.get(server_ip+'api/file/')
	    a=r.json()
	    for entry in a:
	        print(entry['path'])
	    print()

	def getdetail(path):
	    URL_detail=detailurl(path)
	    r=client.get(URL_detail)
	    if r.status_code ==200:
	        a=r.json()
	        print('sha256:  '+a['sha256'])
	        # print('data:  '+a['docfile'])
	        with open('received_'+path+'.png','wb') as file:
	        	data=str.encode(a['docfile'])
	        	# print(type(data))
	        	file.write(data)

	    print(r.status_code)

	def updatefile(path):
	    URL_update = detailurl(path)
	    exists = os.path.isfile(observing_root+path)

	    if exists:
	        r=client.get(server_ip)
	        if 'csrftoken' in client.cookies:
	            csrftoken = client.cookies['csrftoken']
	        sha = filehash(observing_root+path)
	        data = dict(path = path, owner='jatin',sha256 = sha, docfile= open(observing_root+path,'rb') , csrfmiddlewaretoken=csrftoken)
	        # print(data)
	        r = client.put(URL_update, data=data, headers={"Referer": server_ip,"X-CSRFToken" : csrftoken})
	        # print(r.text)
	        if r.status_code == 500:
	            print('This file already exists on the server, try updating instead or delete this first!')
	        print(sha, path)
	        print(r.status_code)
	    else:
	        print('File does not exist!')


	def uploadfile(path):
	    URL_create=server_ip + 'api/file/'
	    exists = os.path.isfile(observing_root+path)
	    if exists:
	        client.get(server_ip)
	        if 'csrftoken' in client.cookies:
	            csrftoken = client.cookies['csrftoken']
	        sha = filehash(observing_root+path)
	        file = open(observing_root+path,'rb')
	        # with open("myfile", "rb") as f:
	        #     byte = f.read(1)
	        #     while byte:
	    
	        #         byte = f.read(1)
	        docfile=file.read() 
	        # data = dict(docfile = open(observing_root+path,'rb'))
	        data = dict(path = path, sha256 = sha, docfile=docfile , csrfmiddlewaretoken=csrftoken,  next='')
	        r = client.post(URL_create, data=data, headers=dict(Referer=server_ip))
	        if r.status_code == 500:
	            print('This file already exists on the server, try updating instead or delete this first!')
	        print(r.status_code)
	        print(sha,path)
	        # print(r.text)
	        # print(r.headers)
	    else:
	        print('File does not exist!')

	def deletefile(path):
	    URL_delete=detailurl(path)
	    r=client.get(server_ip)
	  
	    if 'csrftoken' in client.cookies:
	        csrftoken = client.cookies['csrftoken']
	    # sha = filehash(observing_root+path)
	    # file = open(observing_root+path,'rb')
	    # docfile=file.read() 
	    # data = dict(docfile = open(observing_root+path,'rb'))
	    data = dict(path = path, csrfmiddlewaretoken=csrftoken,  next='')
	    r = client.delete(URL_delete, data=data, headers={"Referer": server_ip, "X-CSRFToken" : csrftoken})
	    if r.status_code == 404:
	        print('This file does not exist on the server!')
	    else:
	        print('Successfully deleted '+path)
	    print(r.status_code)

	while True:
	    foo=input('Ready for duty: ')
	    if foo == 'list':
	        getlist()

	    elif foo == 'detail':
	        path = input('Input file path: ')
	        getdetail(path)

	    elif foo=='upload':
	        path = input('Input file path: ')
	        uploadfile(path)

	    elif foo=='update':
	        path = input('Input file path: ')
	        updatefile(path)

	    elif foo=='delete':
	        path = input('Input file path: ')
	        deletefile(path)

	    else:
	        print('Invalid Argument!')
	        print("Type 'help' for help")
	mydb.commit()
	mydb.close()


if __name__ == '__main__':
    main()