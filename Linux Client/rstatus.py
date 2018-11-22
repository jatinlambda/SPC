#! /usr/bin/python3
import requests
import getpass
import os, sys
import hashlib
import json
import sqlite3
import os.path as osp
import base64


server_ip='http://192.168.1.105:8000/'
observing_root='./'
username=None
password=None
    
def filehash(filepath):
    file = open(filepath,'rb')
    docfile=file.read()
    docfile=base64.encodestring(docfile)
    sha = hashlib.sha256()
    sha.update(docfile)
    sha=sha.hexdigest()
    return sha

def main():
	mydb = sqlite3.connect("Files.db")
	cur = mydb.cursor()

	cur.execute('''SELECT * FROM Server_ip''')
	for row in cur:
	    # print("Server_ip is set to "+row[0])
	    server_ip=row[0]
	server_ip='http://192.168.1.105:8000/'

	cur.execute('''SELECT * FROM Root''')
	for row in cur:
	    # print("Observing "+row[0] +" directory")
	    observing_root='test0/'


	cur.execute('''SELECT * FROM User''')
	for row in cur:
	    username=row[0]
	    password=row[1]

	# list_of_files=[]
	# list_of_dbfiles=[]

	# for root, dirs, files in os.walk(observing_root):
	# 	for fpath in [osp.join(root, f) for f in files]:
	# 		name = osp.relpath(fpath, observing_root)
	# 		list_of_files.append(name)

	# 	for fpath in [osp.join(root, f) for f in dirs]:
	# 		name = osp.relpath(fpath, observing_root)+'/'
	# 		list_of_files.append(name)

	# cur.execute('''SELECT * FROM Files''')
	# for row in cur:
	# 	list_of_dbfiles.append(row[0])


	# for file in list_of_dbfiles:
	# 	if file not in list_of_files:
	# 		cur.execute('''DELETE FROM Files WHERE filepath="'''+file+'"')
	# 		# print(file +' (deleted)')

	# for file in list_of_files:
	# 	if file not in list_of_dbfiles:
	# 		if os.path.isdir(observing_root+file):
	# 			sha256 = None
	# 			stamp = None
	# 		else:
	# 			sha256 = filehash(observing_root+file)      ##### check
	# 			stamp = os.path.getmtime(observing_root+file)
	# 		cur.execute("INSERT INTO Files (filepath, sha256, stamp) VALUES (?,?,?)",[file,sha256,str(stamp)])
	# 		# print(file +' (added)')

	# for file in list_of_files:
	# 	if file in list_of_dbfiles:
	# 		if os.path.isdir(observing_root+file):
	# 			continue
	# 		else:
	# 			stamp = os.path.getmtime(observing_root+file)
	# 			cur.execute('''SELECT * FROM Files WHERE filepath="'''+ file +'"')
	# 			dbstamp=None
	# 			for row in cur:
	# 				dbstamp=row[2]
	# 			if dbstamp<stamp:
	# 				sha256 = filehash(observing_root+file)      
	# 				cur.execute("UPDATE Files SET stamp='"+str(stamp)+"' , sha256='"+sha256+"' WHERE filepath='"+file+"'")
	# 				# print(file +' (modified)')
				

	

	# URL_login = server_ip+'accounts/login/'
	URL_login = server_ip+'accounts/login/'
	client = requests.session()

	# Retrieve the CSRF token first
	client.get(URL_login)  # sets cookie
	if 'csrftoken' in client.cookies:
	    csrftoken = client.cookies['csrftoken']

	# login_data = dict(username=input('Username: '), password=getpass.getpass(), csrfmiddlewaretoken=csrftoken, next='/')
	login_data = dict(username=username, password=password, csrfmiddlewaretoken=csrftoken, next='')
	r = client.post(URL_login, data=login_data, headers=dict(Referer=URL_login))
	

	def getlist(mode=1):
		r=client.get(server_ip+'api/listfile/',stream=True)
		a=r.json()
		if mode==0:
			for entry in a:
				if entry['isdir']:
					print(entry['path'])
				else:
					print( entry['sha256'],entry['path'])
		elif mode==1:
			ans={}
			for entry in a:
				ans[entry['path']]=[entry['sha256'],entry['isdir']]
			return ans


	dict_of_lcfiles={}
	dict_of_rmfiles={}

	cur.execute('''SELECT * FROM Files''')
	for row in cur:
		dict_of_lcfiles[row[0]]=row[1]
	list_of_lcfiles=dict_of_lcfiles.keys()
	dict_of_rmfiles=getlist(1)
	list_of_rmfiles=dict_of_rmfiles.keys()

	if [ file for file in list_of_lcfiles if file not in list_of_rmfiles]:
		print('Objects only on local machine:')
		for file in list_of_lcfiles:
			if file not in list_of_rmfiles:
				print(' ',file)
		print()

	if [ file for file in list_of_rmfiles if file not in list_of_lcfiles]:
		print('Objects only on remote server:')
		for file in list_of_rmfiles:
			if file not in list_of_lcfiles:
				print(' ',file)
		print()

	if [ file for file in list_of_rmfiles if file in list_of_lcfiles]:
		print('Objects both on local machine and remote server:')
		for file in list_of_lcfiles:
			if file in list_of_rmfiles:
				if dict_of_rmfiles[file][0]==dict_of_lcfiles[file]:
					print(' ',file)
				else:
					print(' ',file,'(remote has differnt version)')
		print()
	mydb.close()


if __name__ == '__main__':
    main()