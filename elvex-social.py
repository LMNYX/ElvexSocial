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
import ssl
from OpenSSL import crypto, SSL
from Crypto.Cipher import AES
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Util.asn1 import DerSequence
from binascii import a2b_base64


Logger("Python importing complete.", CT.INFO)

init(autoreset=True)
Logger("Colorama initialized.", CT.INFO)

if not (os.path.isfile("private.pem")):
	if not (os.path.isfile("public.pem")):
		key = RSA.generate(2048)
		private_key = key.export_key()
		file_out = open("private.pem", "wb")
		file_out.write(private_key)
		file_out.close()
		public_key = key.publickey().export_key()
		file_out = open("public.pem", "wb")
		file_out.write(public_key)
		file_out.close()
	else:
		os.unlink("public.pem")
		key = RSA.generate(2048)
		private_key = key.export_key()
		file_out = open("private.pem", "wb")
		file_out.write(private_key)
		file_out.close()
		public_key = key.publickey().export_key()
		file_out = open("public.pem", "wb")
		file_out.write(public_key)
		file_out.close()
else:
	if not (os.path.isfile("public.pem")):
		key = RSA.generate(2048)
		private_key = key.export_key()
		file_out = open("private.pem", "wb")
		file_out.write(private_key)
		file_out.close()
		public_key = key.publickey().export_key()
		file_out = open("public.pem", "wb")
		file_out.write(public_key)
		file_out.close()

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
try:
	key = RSA.importKey(open('private.pem').read())
	cipher = PKCS1_OAEP.new(key)
except Exception:
	print("Bad RSA key. Recreate it.", CT.ERROR)
while(True):
	try:
		asdasdsad()
		bap = server.recvfrom(bufferSize)
		message = str(cipher.decrypt(bap[0]))
		message = message[:-1][2:]
		address = bap[1]
		print("Received packet from "+str(address[0])+" with size of "+str(address[1])+" bytes.", CT.INFO)
		try:
			fff = int(message)
			del fff
			Logger("It's int!", CT.WARN)
			Response = EncodedString(json.dumps({'error': 'NOT_JSON'}))
			server.sendto(Response, address)
			continue
		except Exception:
			Logger("Woah! Everything is ok!")
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
					r = r
					Response = EncodedString(json.dumps({'response': 'OK', '{}'.format(jsonMessage['args']['login']): {'login': r[0], 'avatar': r[1], 'electricity': r[2], 'pp': r[3], 'inventory': json.loads(r[4]), 'customization': json.loads(r[5]), 'bio': r[6], 'stats': json.loads(r[7]), 'banned': bool(r[8])}}))
		elif(jsonMessage['act'] == 'inventory.setCustomization'):
			if('login' not in jsonMessage['args'] or 'pswd' not in jsonMessage['args'] or 'slot' not in jsonMessage['args'] or 'item' not in jsonMessage['args']):
				Response = EncodedString(json.dumps({'error':'NO_ARGS'}))
			else:
				r = GetUser(jsonMessage['args']['login'])
				if(r == "USER_GONE" or r == "USER_SPACE"):
					Response = EncodedString(json.dumps({'error': r}))
				else:
					r = json.loads(r)
					inv = r[4]
					if(jsonMessage['args']['item'] not in inv):
						Response = EncodedString(json.dumps({'error':'NO_ITEM'}))
					else:
						SetCustomizationUser(r[0], jsonMessage['args']['slot'], jsonMessage['args']['item'])
						Response = EncodedString(json.dumps({'response':'OK'}))
		elif(jsonMessage['act'] == "market.get"):
			Response = EncodedString(json.dumps({'response': 'OK', 'items': GetStoreItems()}))
		elif jsonMessage['act'] == "market.getTimer":
			Response = EncodedString(json.dumps({'response': 'OK', 'seconds_left': GetStoreTimer()}))
		elif(jsonMessage['act'] == "market.buy"):
			if('login' not in jsonMessage['args'] or 'pswd' not in jsonMessage['args'] or 'slot' not in jsonMessage['args']):
				Response = EncodedString(json.dumps({'error':'NO_ARGS'}))
			else:
				StoreItems = GetStoreItems()
				try:
					tttt = int(jsonMessage['args']['slot'])
					del tttt
					r = GetUser(jsonMessage['args']['login'])
					if(r == "USER_GONE" or r == "USER_SPACE"):
						Response = EncodedString(json.dumps({'error': r}))
					else:
						r = GetStoreItem(int(jsonMessage['args']['slot']))
						if(type(r) == str):
							Response = EncodedString(json.dumps({'error': 'NO_INDEX_ITEM'}))
						else:
							if(GetUserBalance(jsonMessage['args']['login']) < r[1]):
								Response = EncodedString(json.dumps({'error': 'NOT_ENOUGH_CASH'}))
							else:
								EditUser(jsonMessage['args']['login'], "electricity", GetUserBalance(jsonMessage['args']['login'])-r[1])
								AddInvUser(jsonMessage['args']['login'], r[0])
								Response = EncodedString(json.dumps({'response':'OK'}))
				except Exception:
					Response = EncodedString(json.dumps({'error':'INVALID_ARG'}))
		else:
			Response = EncodedString(json.dumps({'error': 'BAD_REQUEST'}))
		server.sendto(Response, address)
	except Exception as e:
		print("Uh oh! Error approaches! ("+str(e)+")", CT.ERROR)