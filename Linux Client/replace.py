import os
import sys
import fileinput

textToReplace='#! '+os.path.expanduser('~')+'/SPC_config/env_SPC/bin/python3\nimport click,os'
textToSearch='import click,os'
with fileinput.FileInput(os.path.expanduser('~')+'/SPC_config/Linux Client/SPC.py', inplace=True) as file:
	    for line in file:
	        print(line.replace(textToSearch, textToReplace), end='')



textToReplace="os.remove(filepath+'.enc')"
textToSearch="# os.remove(filepath+'.enc')"
with fileinput.FileInput(os.path.expanduser('~')+'/SPC_config/Linux Client/rstatus.py', inplace=True) as file:
	    for line in file:
	        print(line.replace(textToSearch, textToReplace), end='')



textToSearch = '"Files.db"'
textToReplace = "os.path.expanduser('~') + '/SPC.db'"
list_of_files=[]
observing_root= os.path.expanduser('~') + '/SPC_config/Linux Client/'
for root, dirs, files in os.walk(observing_root):
	for fpath in [os.path.join(root, f) for f in files]:
		if not fpath==str(os.path.expanduser('~') + '/SPC_config/Linux Client/replace.py'):
			list_of_files.append(fpath)


for files in list_of_files:
	with fileinput.FileInput(files, inplace=True) as file:
	    for line in file:
	        print(line.replace(textToSearch,textToReplace), end='')

