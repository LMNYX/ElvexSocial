import time
import socket
import os
import configparser
from colorama import Fore, Back, init
from elvex import *
import json
import hmac
import hashlib
import base64
import sqlite3
import subprocess

Logger("Python importing complete.", CT.INFO)

init(autoreset=True)
Logger("Colorama initialized.", CT.INFO)


Logger("Elvex Social Server version "+str(version), CT.INFO)

bufferSize = 1024
config = configparser.ConfigParser()
DefaultConfig = {}
DefaultConfig['Connection'] = {'serverip': '127.0.0.1','port': '60606','version': 3}
DefaultConfig['Encryption'] = {'adminkey': '123321'}
Logger("Checking config...", CT.NONE)
if not(os.path.isfile("server.ini")):
	Logger("Config doesn't exists. Creating...", CT.WARN)
	config['Connection'] = DefaultConfig['Connection']
	config['Encryption'] = DefaultConfig['Encryption']
	with open('server.ini', 'w') as cf:
		config.write(cf)

Logger("Reading config...", CT.INFO)
config.read("server.ini")
Logger("Config imported.", CT.INFO)
if('version' not in config['Connection'] or int(config['Connection']['version']) != version):
	print("Version of server.ini and server doesn't match. Recreating server.ini", CT.WARN)
	config['Connection'] = DefaultConfig['Connection']
	config['Encryption'] = DefaultConfig['Encryption']
	with open('server.ini', 'w') as cf:
		config.write(cf)
LogPrint("Starting server on IP "+config['Connection']['serverip']+" with port "+config["Connection"]['port'], CT.INFO)
server = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
if(config['Connection']['serverip'] == "127.0.0.1" or config['Connection']['serverip'] == ""):
	config['Connection']['serverip'] == ""
server.bind((config['Connection']['serverip'], int(config['Connection']['port'])))
LogPrint("Ready to listen.", CT.INFO)

while(True):
	bap = server.recvfrom(bufferSize)
	message = bap[0].decode()
	address = bap[1]
	print("Received packet from "+str(address[0])+" with size of "+str(address[1])+" bytes.", CT.INFO)
	if not (is_json(message)):
		Response = EncodedString(json.dumps({'error': 'NOT_JSON'}))
		server.sendto(Response, address)
		continue
	else:
		jsonMessage = json.loads(message)
	if('act' not in jsonMessage or 'args' not in jsonMessage):
		Response = EncodedString(json.dumps({'error': 'NO_METHOD'}))
		server.sendto(Response, address)
		continue
	if(jsonMessage['act'] == "account.Create"):
		if('login' not in jsonMessage['args'] or 'pswd' not in jsonMessage['args']):
			Response = EncodedString(json.dumps({'error':'NO_ARGS'}))
		else:
			r = AddUser(jsonMessage['args']['login'], jsonMessage['args']['pswd'],regip=str(address[0]))
			if(r != "OK"):
				Response = EncodedString(json.dumps({"error": r}))
			else:
				Response = EncodedString(json.dumps({'response':'OK'}))
	elif(jsonMessage['act'] == 'account.checkPass'):
		if('login' not in jsonMessage['args'] or 'pswd' not in jsonMessage['args']):
			Response = EncodedString(json.dumps({'error':'NO_ARGS'}))
		else:
			r = GetUser(jsonMessage['args']['login'], False)
			if(r == "USER_GONE" or r == "USER_SPACE"):
				Response = EncodedString(json.dumps({'error': r}))
			else:
				r = json.loads(r)
				if(jsonMessage['args']['pswd'] != r[0][1]):
					Response = EncodedString(json.dumps({'error':'BAD_PASSWORD'}))
				else:
					Response = EncodedString(json.dumps({'response':'OK'}))
	elif(jsonMessage['act'] == 'account.get'):
		if('login' not in jsonMessage['args']):
			Response = EncodedString(json.dumps({'error':'NO_ARGS'}))
		else:
			r = GetUser(jsonMessage['args']['login'])
			if(r == "USER_GONE" or r == "USER_SPACE"):
				Response = EncodedString(json.dumps({'error': r}))
			else:
				r = json.loads(r)
				Response = EncodedString(json.dumps({'response': 'OK', '{}'.format(jsonMessage['args']['login']): {'login': r[0][0], 'avatar': r[0][1], 'electricity': r[0][2], 'pp': r[0][3], 'inventory': json.loads(r[0][4]), 'customization': json.loads(r[0][5]), 'bio': r[0][6], 'stats': json.loads(r[0][7]), 'banned': bool(r[0][8])}}))
	elif(jsonMessage['act'] == 'inventory.setCustomization'):
		if('login' not in jsonMessage['args'] or 'pswd' not in jsonMessage['args'] or 'slot' not in jsonMessage['args'] or 'item' not in jsonMessage['args']):
			Response = EncodedString(json.dumps({'error':'NO_ARGS'}))
		else:
			r = GetUser(jsonMessage['args']['login'])
			if(r == "USER_GONE" or r == "USER_SPACE"):
				Response = EncodedString(json.dumps({'error': r}))
			else:
				r = json.loads(r)
				inv = r[0][4]
				if(jsonMessage['args']['item'] not in inv):
					Response = EncodedString(json.dumps({'error':'NO_ITEM'}))
				else:
					SetCustomizationUser(r[0][0], jsonMessage['args']['slot'], jsonMessage['args']['item'])
					Response = EncodedString(json.dumps({'response':'OK'}))
	elif(jsonMessage['act'] == ""):
		e = "e"
	else:
		Response = EncodedString(json.dumps({'error': 'BAD_REQUEST'}))
	server.sendto(Response, address)