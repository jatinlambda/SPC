#! /usr/bin/python3
import requests
import getpass
import os, sys
import hashlib
import json
import sqlite3
import os.path as osp
import base64
import tqdm
import time
import logging

server_ip='http://192.168.1.105:8000/'
observing_root='./'
username=None
password=None
    
def filehash(filepath):
    # blocksize = 64*1024
    # sha = hashlib.sha256()
    # with open(filepath, 'rb') as fp:
    #     while True:
    #         data = base64.encodestring(fp.read(blocksize))
    #         if not data:
    #             break
    #         sha.update(data)
    # return sha.hexdigest()
    file = open(filepath,'rb')
    docfile=file.read()
    docfile=base64.encodestring(docfile)
    sha = hashlib.sha256()
    sha.update(docfile)
    sha=sha.hexdigest()
    return sha

def assure_path_exists(path):
        dir = os.path.dirname(path)
        if not os.path.exists(dir):
                os.makedirs(dir)

class upload_in_chunks(object):
    def __init__(self, filename):
        self.filename = filename
        self.totalsize = os.path.getsize(filename)
        self.readsofar = 0

    def __iter__(self):
        with open(self.filename, 'rb') as file:
        	pbar = tqdm.tqdm(total=self.totalsize,ncols=100)
        	while True:
        		data = file.read(4096)
        		if not data:
        			break
        		yield data
        		pbar.update(len(data))
        	pbar.close()

    def __len__(self):
        return self.totalsize


def main():
	mydb = sqlite3.connect("Files.db")
	cur = mydb.cursor()
	cur.execute('''SELECT * FROM Server_ip''')
	for row in cur:
	    print("Server_ip is set to "+row[0])
	    server_ip=row[0]
	server_ip='http://192.168.1.105:8000/'

	cur.execute('''SELECT * FROM Root''')
	for row in cur:
	    print("Observing "+row[0] +" directory")
	    observing_root='test0/'


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
			name = osp.relpath(fpath, observing_root)+'/'
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
	URL_login = server_ip+'accounts/login/'
	client = requests.session()

	# Retrieve the CSRF token first
	client.get(URL_login)  # sets cookie
	if 'csrftoken' in client.cookies:
	    csrftoken = client.cookies['csrftoken']

	# login_data = dict(username=input('Username: '), password=getpass.getpass(), csrfmiddlewaretoken=csrftoken, next='/')
	login_data = dict(username=username, password=password, csrfmiddlewaretoken=csrftoken, next='')
	r = client.post(URL_login, data=login_data, headers=dict(Referer=URL_login))
	
	log=[]
	# print(r.text)
	# print(r.headers)
	def detailurl(path):
	    # if path[-1]=='/':
	    #     return server_ip+'api/file/'+path
	    # else:
	    #     return server_ip+'api/file/'+path+'/'
	    return server_ip+'api/file/'+path+'/'

	def getlist(mode=0):
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

	def getdetail(path):
		log=''
		try:
			r=client.get(detailurl(path))
			a=r.json()
		except:
			print(path,'(server error)')
			return

		# print(a['path'],a['sha256'],a['isdir'])
		try:
			sha=None
			if not a['isdir']:
				data = bytes(a['docfile'], 'utf-8')
				sha = hashlib.sha256()
				sha.update(data)
				sha=sha.hexdigest()
				data = base64.decodestring(data)
				if sha==a['sha256']:
					assure_path_exists(observing_root+path)
					file = open(observing_root+path, 'wb')
					file.write(data)
					# print(a['path'],'(downloaded)')
					log+=a['path']+' (downloaded)'+'\n'
				else:
					# print(a['path'],'(failed)')
					log+=a['path']+' (failed)'+'\n'
			else:
				assure_path_exists(observing_root+a['path'])
				# print(a['path'],'(checked)')
				log+=a['path']+' (checked)'+'\n'
			stamp = os.path.getmtime(observing_root+path)
			cur.execute("INSERT INTO Files (filepath, sha256, stamp) VALUES (?,?,?)",[path,sha,str(stamp)])
		except:
			# print(path,'(internal error)')
			log+=path+' (internal error)'+'\n'
		return log


	# def getdetail(path):
	# 	try:
	# 		f=open('.temp', "wb")
	# 		r=client.get(detailurl(path),stream=True)
	# 		total_length = r.headers.get('content-length')
	# 		if len(path)<70:
	# 			print(path.ljust(70),str(int(total_length)/1000)+' kb')
	# 		else:
	# 			print(path,str(int(total_length)/1000)+' kb')
	# 		if total_length is None:
	# 			f.write(r.content)
	# 		else:
	# 			dl = 0
	# 			total_length = int(total_length)
	# 			pbar = tqdm.tqdm(total=total_length,ncols=100)
	# 			for data in r.iter_content(chunk_size=4096):
	# 				dl = len(data)
	# 				f.write(data)
	# 				pbar.update(dl)
	# 		pbar.close()
	# 		f.close()
	# 		f=open('.temp')
	# 		a = json.load(f)
	# 		f.close()
	# 		os.remove(".temp")
	# 	except:
	# 		print(path,'(server error or user interupt)')
	# 		return
	# 	try:
	# 		if not a['isdir']:
	# 			data = bytes(a['docfile'], 'utf-8')
	# 			sha = hashlib.sha256()
	# 			sha.update(data)
	# 			sha=sha.hexdigest()
	# 			print(sha)
	# 			data = base64.decodestring(data)
	# 			if sha==a['sha256']:
	# 				assure_path_exists(observing_root+path)
	# 				file = open(observing_root+path, 'wb')
	# 				file.write(data)
	# 				print(a['path'],'(downloaded)')
	# 			else:
	# 				print(a['path'],'(failed)')
	# 		else:
	# 			assure_path_exists(observing_root+a['path'])
	# 			print(a['path'],'(checked)')
	# 	except Exception as e:
	# 		logging.exception("message")
	# 		print(path,'(internal error)')


	def read_in_chunks(file_object, blocksize=4096):
		while True:
			data = file_object.read(blocksize)
			if not data:
				break
			yield data


# requests.post('http://some.url/chunked', data=read_in_chunks(f))


	# def updatefile(path):
	#     URL_update = detailurl(path)

	#     if os.path.isfile(observing_root+path):
	#         r=client.get(server_ip)
	#         if 'csrftoken' in client.cookies:
	#             csrftoken = client.cookies['csrftoken']
	#         file = open(observing_root+path,'rb')
	#         docfile=file.read()
	#         docfile=base64.encodestring(docfile)
	#         file = open('.temp2','wb')
	#         file.write(docfile)
	#         file.close()
	#         sha = hashlib.sha256()
	#         sha.update(docfile)
	#         sha=sha.hexdigest()
	#         data = dict(path = path, owner='jatin',sha256 = sha, docfile= upload_in_chunks('.temp2'),isdir=False, csrfmiddlewaretoken=csrftoken)
	#         r = client.put(URL_update, data=data, headers={"Referer": server_ip,"X-CSRFToken" : csrftoken})
	#         if r.status_code == 500:
	#             print('(server error)')
	#         else:
	#         	print(path,'(updated)')
	#         # print(r.status_code,sha, path)
	#         # print(r.status_code)
	#     else:
	#         print(path,'(file does not exist)')

	def updatefile(path):
	    URL_update = detailurl(path)
	    log=''

	    if os.path.isfile(observing_root+path):
	        r=client.get(server_ip)
	        if 'csrftoken' in client.cookies:
	            csrftoken = client.cookies['csrftoken']
	        file = open(observing_root+path,'rb')
	        docfile=file.read()
	        docfile=base64.encodestring(docfile)
	        sha = hashlib.sha256()
	        sha.update(docfile)
	        sha=sha.hexdigest()
	        data = dict(path = path, owner='jatin',sha256 = sha, docfile= docfile,isdir=False, csrfmiddlewaretoken=csrftoken)
	        r = client.put(URL_update, data=data, headers={"Referer": server_ip,"X-CSRFToken" : csrftoken})
	        if r.status_code == 500:
	            # print('(server error)')
	            log+=path+' (server error)'+'\n'
	        else:
	        	# print(path,'(updated)')
	        	log+=path+' (updated)'+'\n'
	        # print(r.status_code,sha, path)
	        # print(r.status_code)
	    else:
	        # print(path,'(file does not exist)')
	        log+=path+' (file does not exist)'+'\n'
	    return log

	def uploadfile(path):
		URL_create=server_ip + 'api/file/'
		log=''
		try:
			client.get(server_ip)
			if 'csrftoken' in client.cookies:
				csrftoken = client.cookies['csrftoken']
			docfile=None
			sha256=None
			isdir=True
			if os.path.isfile(observing_root+path):
				file = open(observing_root+path,'rb')
				docfile=file.read()
				docfile=base64.encodestring(docfile)
				sha = hashlib.sha256()
				sha.update(docfile)
				isdir=False
				sha256=sha.hexdigest()
			elif os.path.isdir(observing_root+path):
				pass
			else:
				# print(path,'(file does not exist)')
				log+=path+' (file does not exist)'+'\n'

			data = dict(path = path, sha256 = sha256, docfile=docfile , isdir=isdir, csrfmiddlewaretoken=csrftoken,  next='')
			r = client.post(URL_create, data=data, headers=dict(Referer=server_ip))
			if r.status_code == 500:
				# print('(server error)')
				log+=path+' (server error)'+'\n'
			else:
				# print(path, '(uploaded)')
				log+=path+' (uploaded)'+'\n'
		except:
			# print(path, '(failed)')
			log+=path+' (failed)'+'\n'
		return log

	# def uploadfile(path):
	# 	URL_create=server_ip + 'api/file/'
	# 	# try:
	# 	client.get(server_ip)
	# 	if 'csrftoken' in client.cookies:
	# 		csrftoken = client.cookies['csrftoken']
	# 	if os.path.isfile(observing_root+path):
	# 		file = open(observing_root+path,'rb')
	# 		docfile=file.read()
	# 		file.close()
	# 		docfile=base64.encodestring(docfile)
	# 		file = open('.temp2','wb')
	# 		file.write(docfile)
	# 		file.close()
	# 		sha = hashlib.sha256()
	# 		sha.update(docfile)
	# 		isdir=False
	# 		sha256=sha.hexdigest()
	# 		data = dict(path = path, sha256 = sha256, docfile=upload_in_chunks('.temp2') , isdir=False, csrfmiddlewaretoken=csrftoken,  next='')
	# 	elif os.path.isdir(observing_root+path):
	# 		data = dict(path = path, sha256 = None, docfile=None , isdir=True, csrfmiddlewaretoken=csrftoken,  next='')
	# 	else:
	# 		print(path,'(file does not exist)')

	# 	# data = dict(path = path, sha256 = sha256, docfile=upload_in_chunks('.temp2') , isdir=isdir, csrfmiddlewaretoken=csrftoken,  next='')
	# 	r = client.post(URL_create, data=data, headers=dict(Referer=server_ip))
	# 	# print(r.text)
	# 	if r.status_code == 500:
	# 		print(path, '(server error)')
	# 	else:
	# 		print(path, '(uploaded)')
	# 	# except:
	# 	# 	print(path, '(failed)')


	def deletefile(path):	
	    URL_delete=detailurl(path)
	    log=''
	    r=client.get(server_ip)
	  
	    if 'csrftoken' in client.cookies:
	        csrftoken = client.cookies['csrftoken']

	    data = dict(path = path, csrfmiddlewaretoken=csrftoken,  next='')
	    r = client.delete(URL_delete, data=data, headers={"Referer": server_ip, "X-CSRFToken" : csrftoken})
	    if r.status_code == 404:
	        # print(path,'(file does not exist on server)')
	        log+=path+' (file does not exist on server)'+'\n'
	    else:
	        # print(path,'(deleted)')
	        log+=path+' (deleted)'+'\n'
	    # print(r.status_code)
	    return log


	client.get(server_ip) # if 'csrftoken' in client.cookies:
	csrftoken = client.cookies['csrftoken']
	URL_start_sync = server_ip+'api/begin/'#server_ip + 'api/begin/'
	f = client.post(URL_start_sync,dict(csrfmiddlewaretoken=csrftoken, id='linux-client', next='',headers=dict(Referer=server_ip)))
	g = f.json()
	print(g)


	dict_of_lcfiles={}
	dict_of_rmfiles={}

	cur.execute('''SELECT * FROM Files''')
	for row in cur:
		dict_of_lcfiles[row[0]]=row[1]
	list_of_lcfiles=dict_of_lcfiles.keys()
	dict_of_rmfiles=getlist(1)
	list_of_rmfiles=dict_of_rmfiles.keys()

	no_of_files=0
	for file in list_of_lcfiles:
		if file not in list_of_rmfiles:
			if os.path.isfile(observing_root+file):
				no_of_files+=1

	for file in list_of_rmfiles:
		if file not in list_of_lcfiles:
			if not dict_of_rmfiles[file][1]:
				print(file,dict_of_rmfiles[file][1])
				no_of_files+=1

	for file in list_of_lcfiles:
		if file in list_of_rmfiles:
			if os.path.isfile(observing_root+file):
				no_of_files+=1




	pbar = tqdm.tqdm(total=no_of_files,ncols=100,mininterval=0,miniters=0,file=sys.stdout)

	for file in list_of_lcfiles:
		if file not in list_of_rmfiles:
			log.append(uploadfile(file))
			if os.path.isfile(observing_root+file):
				pbar.update(1)

	for file in list_of_rmfiles:
		if file not in list_of_lcfiles:
			log.append(getdetail(file))
			if not dict_of_rmfiles[file][1]:
				pbar.update(1)


	for file in list_of_lcfiles:
		if file in list_of_rmfiles:
			if dict_of_rmfiles[file][0]==dict_of_lcfiles[file]:
				# print(file.ljust(50),' (up to date)')
				log.append(file.ljust(50)+' (up to date)')
			else:
				while True:
					choice=input('For "'+file+'", press "r" to keep remote copy or "l" for local copy\n')
					if choice=='r':
						log.append(getdetail(file))
						break
					elif choice=='l':
						log.append(updatefile(file))
						break
					else:
						print('Invalid choice!')
			if os.path.isfile(observing_root+file):
				pbar.update(1)
	pbar.close()
	for entry in log:
		print(entry)




	# while True:
	#     foo=input('Ready for duty: ')
	#     if foo == 'list':
	#         getlist(0)

	#     elif foo == 'detail':
	#         path = input('Input file path: ')
	#         getdetail(path)

	#     elif foo=='upload':
	#         path = input('Input file path: ')
	#         uploadfile(path)

	#     elif foo=='update':
	#         path = input('Input file path: ')
	#         updatefile(path)

	#     elif foo=='delete':
	#         path = input('Input file path: ')
	#         deletefile(path)

	#     else:
	#         print('Invalid Argument!')
	#         print("Type 'help' for help")

	
	mydb.commit()
	mydb.close()
	csrftoken = client.cookies['csrftoken']
	URL_end_sync = server_ip + 'api/end/'    # URL_start_sync = 'http://127.0.0.1:8000/api/begin/'#server_ip + 'api/begin/'
	sync_ender = client.post(URL_end_sync,dict(csrfmiddlewaretoken=csrftoken,id='linux-client', next='',headers=dict(Referer=server_ip)))
	h = sync_ender.json()  # client.post(URL_end_sync, headers=dict(Referer=URL_end_sync))
	print(h)


if __name__ == '__main__':
    main()