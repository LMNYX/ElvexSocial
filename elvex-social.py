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
from PIL import Image, ImageDraw
from pystray import Icon as icon, Menu as menu, MenuItem as item
import requests
from io import BytesIO
import psutil
import tkinter as tk
from tkinter import simpledialog
oprint("")

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
state=False

decryptMessages = True

class trayActions:
	def none():
		AN = "AN"
		del AN
	def switchDecryption():
		global decryptMessages
		decryptMessages = not decryptMessages
		if(decryptMessages): print("Messages now decrypts when received!")
		else: print("Messages now expected to be not encrypted.")
	def restart():
		print("Restarting the Elvex SOCIAL server.", CT.WARN)
		try:
			p = psutil.Process(os.getpid())
			for handler in p.get_open_files() + p.connections():
				os.close(handler.fd)
		except Exception as e:
			void1 = "void"
			del void1
		python = sys.executable
		os.execl(python, python, *sys.argv)
	def exit():
		os._exit(1)
	def Exec():
		USER_INP = simpledialog.askstring(title="Elvex",
                                  prompt="Enter function:")
		eval(USER_INP)
	def checkDBs():
		conn = sqlite3.connect('users.db')
		c = conn.cursor()
		try:
			dInfo = c.execute("SELECT data FROM db_info WHERE st = 'ver'")
			dInfo = dInfo.fetchone()[0]
		except Exception:
			print("Your version of users.db is very out of date. Please"+Fore.RED+" recreate "+Fore.RESET+"it ASAP.", CT.ERROR)
			dInfo = db_usersVer
		if(dInfo < db_usersVer):
			print("Your version of users.db is out of date. Please be sure to recreate it or update.", CT.WARN)
		elif(dInfo > db_usersVer):
			print("Your version of users.db is newer than this ELVEX SOCIAL version requires. Something may be broken.", CT.WARN)
		else:
			print("Users.db is up to date!")
		conn.close()
		conn = sqlite3.connect('additional.db')
		c = conn.cursor()
		try:
			dInfo = c.execute("SELECT data FROM db_info WHERE st = 'ver'")
			dInfo = dInfo.fetchone()[0]
		except Exception:
			print("Your version of additional.db is very out of date. Please"+Fore.RED+" recreate "+Fore.RESET+"it ASAP.", CT.ERROR)
			dInfo = db_AdditionalsVer

		if(dInfo < db_AdditionalsVer):
			print("Your version of additional.db is out of date. Please be sure to recreate it or update.", CT.WARN)
		elif(dInfo > db_AdditionalsVer):
			print("Your version of additional.db is newer than this ELVEX SOCIAL version requires. Something may be broken.", CT.WARN)
		else:
			print("Additional.db is up to date!")
		conn.close()
		print("DBs checking was finished!")

icon('elvex', Image.open(BytesIO(requests.get("https://avatars3.githubusercontent.com/u/56801454?s=400&u=0ca69763a92ebb07e3bcf1264d17eaed40682467&v=4").content)), menu=menu(
	item('-- Elvex SOCIAL v'+str(version),trayActions.none, enabled=False),
	item('Run command', trayActions.Exec),
	item('Decrypt messages', trayActions.switchDecryption, checked=lambda item: decryptMessages),
	item('Restart', trayActions.restart),
	item('Exit', trayActions.exit))).run()

loggedMethods = []

def isMethod(method):
	global jsonMessage
	global loggedMethods
	if(method not in loggedMethods):
		print("- "+method)
		loggedMethods.append(method)
	return jsonMessage['act'] == method

class ResponseManager(object):
	def __init__(self):
		self.Responses = []
	def SetError(error_code):
		global Response
		Response = EncodedString(json.dumps({'error': error_code}))
		return True
	def SetOkResponse(response_data):
		response_data['response'] = "OK"
		global Response
		Response = EncodedString(json.dumps(response_data))
		return True
	def isArgument(arg):
		global jsonMessage
		return arg in jsonMessage['args']
	def isntArgument(arg):
		global jsonMessage
		return arg not in jsonMessage['args']
	def isArguments(*args):
		global jsonMessage
		for arg in args:
			if(arg not in jsonMessage['args']):
				return False
		return True
	def isntArguments(*args):
		global jsonMessage
		for arg in args:
			if(arg in jsonMessage['args']):
				return False
		return True

rm = ResponseManager()

while(True):
	try:
		bap = server.recvfrom(bufferSize)
		if(decryptMessages):
			message = str(cipher.decrypt(bap[0]))
		else:
			message = str.decode(bap[0])
		message = message[:-1][2:]
		address = bap[1]
		Logger("Received packet from "+str(address[0])+" with size of "+str(address[1])+" bytes.", CT.INFO)
		try:
			fff = int(message)
			del fff
			Logger("It's int!", CT.WARN)
			rm.SetError("NOT_JSON")
			server.sendto(Response, address)
			continue
		except Exception:
			Logger("Woah! Everything is ok!")
		if not (is_json(message)):
			rm.SetError("NOT_JSON")
			server.sendto(Response, address)
			continue
		else:
			jsonMessage = json.loads(message)
		if('act' not in jsonMessage or 'args' not in jsonMessage):
			rm.SetError("NO_METHOD")
			server.sendto(Response, address)
			continue
		if(isMethod("account.Create")):
			if (isntArguments('login', 'pswd')):
				rm.SetError("NO_ARGS")
			else:
				r = AddUser(jsonMessage['args']['login'], jsonMessage['args']['pswd'],regip=str(address[0]))
				if(r != "OK"):
					rm.SetError(r)
				else:
					Response = EncodedString(json.dumps({'response':'OK'}))
		elif(isMethod("account.checkPass")):
			if(isntArguments('login', 'pswd')):
				rm.SetError("NO_ARGS")
			else:
				r = GetUser(jsonMessage['args']['login'], False)
				if(r == "USER_GONE" or r == "USER_SPACE"):
					rm.SetError(r)
				else:
					r = json.loads(r)
					if(EStr(jsonMessage['args']['pswd']) != r[1]):
						rm.SetError("BAD_PASSWORD")
					else:
						Response = EncodedString(json.dumps({'response':'OK'}))
		elif(isMethod("account.get")):
			if(isntArgument('login')):
				rm.SetError("NO_ARGS")
			else:
				r = GetUser(jsonMessage['args']['login'])
				if(r == "USER_GONE" or r == "USER_SPACE"):
					rm.SetError(r)
				else:
					r = r
					Response = EncodedString(json.dumps({'response': 'OK', '{}'.format(jsonMessage['args']['login']): {'login': r[0], 'avatar': r[1], 'electricity': r[2], 'pp': r[3], 'inventory': json.loads(r[4]), 'customization': json.loads(r[5]), 'bio': r[6], 'stats': json.loads(r[7]), 'banned': bool(r[8])}}))
		elif(isMethod("inventory.setCustomization")):
			if(isntArguments('login', 'pswd', 'slot', 'item')):
				rm.SetError("NO_ARGS")
			else:
				r = GetUser(jsonMessage['args']['login'])
				if(r == "USER_GONE" or r == "USER_SPACE"):
					rm.SetError(r)
				else:
					r = json.loads(r)
					inv = r[4]
					if(jsonMessage['args']['item'] not in inv):
						rm.SetError("NO_ITEM")
					else:
						SetCustomizationUser(r[0], jsonMessage['args']['slot'], jsonMessage['args']['item'])
						Response = EncodedString(json.dumps({'response':'OK'}))
		elif isMethod("account.getBanReason"):
			if(isntArguments('login', 'pswd')):
				rm.SetError("NO_ARGS")
			else:
				r = GetUser(jsonMessage['args']['login'], False)
				if(type(r) == str):
					rm.SetError(r)
				elif(EStr(jsonMessage['args']['pswd']) != r[1]):
					rm.SetError("WRONG_PASS")
				else:
					r = GetBanReason(jsonMessage['args']['login'])
					if(type(r) == str):
						rm.SetError(r)
					elif(type(r) == int):
						Response = EncodedString(json.dumps({'response':'OK', 'ban_reason': r}))
					else:
						rm.SetError("UNKNOWN")
		elif(isMethod("market.get")):
			Response = EncodedString(json.dumps({'response': 'OK', 'items': GetStoreItems()}))
		elif isMethod("market.getTimer"):
			Response = EncodedString(json.dumps({'response': 'OK', 'seconds_left': GetStoreTimer()}))
		elif(isMethod("market.buyItem")):
			if(isntArguments('login', 'pswd','slot')):
				rm.SetError("NO_ARGS")
			else:
				StoreItems = GetStoreItems()
				try:
					tttt = int(jsonMessage['args']['slot'])
					del tttt
					r = GetUser(jsonMessage['args']['login'])
					if(r == "USER_GONE" or r == "USER_SPACE"):
						rm.SetError(r)
					else:
						r = GetStoreItem(int(jsonMessage['args']['slot']))
						if(type(r) == str):
							rm.SetError("NO_INDEX")
						else:
							if(GetUserBalance(jsonMessage['args']['login']) < r[1]):
								rm.SetError("NO_CASH")
							else:
								EditUser(jsonMessage['args']['login'], "electricity", GetUserBalance(jsonMessage['args']['login'])-r[1])
								AddInvUser(jsonMessage['args']['login'], r[0])
								Response = EncodedString(json.dumps({'response':'OK'}))
				except Exception:
					rm.SetError("INVALID_ARG")
		else:
			rm.SetError("BAD_REQUEST")
		server.sendto(Response, address)
	except Exception as e:
		print("Uh oh! Error approaches! ("+str(e)+")", CT.ERROR)