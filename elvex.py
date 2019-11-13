import time
import socket
import os
import configparser
from colorama import Fore, Back, init
from elvex_module import *
import json
import hmac
import hashlib
from http.server import BaseHTTPRequestHandler,HTTPServer
import base64
import sqlite3
import asyncio
import logging
import traceback
import subprocess
import ssl
import webbrowser
import elvex_module
import threading
from binascii import a2b_base64
from PIL import Image, ImageDraw
try:
	from pystray import Icon as icon, Menu as menu, MenuItem as item
	DisableTray = False
except:
	DisableTray = True
import requests
from io import BytesIO
import psutil
import argparse
oprint("")

Logger("Python importing complete.", CT.INFO)

init(autoreset=True)
Logger("Colorama initialized.", CT.INFO)

Logger("Elvex Social Server version "+str(version), CT.INFO)

if not (platform.system() == "Windows"):
	print("You are running Elvex SOCIAL on "+str(platform.system())+" OS.", CT.ERROR)
	print("Linux/Darwin are very limited right now, please use Windows to host Elvex SOCIAL for now.", CT.ERROR)
	print("Server will start in 5 seconds...", CT.ERROR)
	time.sleep(5)


bufferSize = 1024
config = configparser.ConfigParser()
DefaultConfig = {}
DefaultConfig['Connection'] = {'serverip': '127.0.0.1','port': '60606','version': 3, "servername": "Social Unnamed"}
Logger("Checking config...", CT.NONE)
if not(os.path.isfile("server.ini")):
	Logger("Config doesn't exists. Creating...", CT.WARN)
	config['Connection'] = DefaultConfig['Connection']
	with open('server.ini', 'w') as cf:
		config.write(cf)

Logger("Reading config...", CT.INFO)
config.read("server.ini")
Logger("Config imported.", CT.INFO)
if('version' not in config['Connection'] or int(config['Connection']['version']) != version):
	print("Version of server.ini and server doesn't match. Recreating server.ini", CT.WARN)
	config['Connection'] = DefaultConfig['Connection']
	with open('server.ini', 'w') as cf:
		config.write(cf)
print("Starting server on IP "+config['Connection']['serverip']+" with port "+config["Connection"]['port'], CT.INFO)
server = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
if(config['Connection']['serverip'] == "127.0.0.1" or config['Connection']['serverip'] == ""):
	config['Connection']['serverip'] = ""
try:
	server.bind((config['Connection']['serverip'], int(config['Connection']['port'])))
except Exception:
	print("Port "+Fore.CYAN+config['Connection']['port']+Fore.RESET+" is already in use.", CT.ERROR)
	time.sleep(10)
	os._exit(-1)

class trayActions:
	def none():
		AN = "AN"
		del AN
	def dashboardOpen():
		webbrowser.open('http://localhost:55155', new=0, autoraise=True)
	def switchDecryption():
		print("Deprecated method. Will be removed in v3 COMPLETELY.")
	def switchTechWorks(s):
		global TechWorkID
		ReasonNames = ["Disabled", "Maintenance", "Update", "Not Listed"]
		CurrentReason = ReasonNames[s+1]
		print("Switched current maintenance state to "+Fore.CYAN+CurrentReason+Fore.RESET+".", CT.INFO)
		TechWorkID = s
	def GetCheckedMaintenance(s):
		global TechWorkID
		return TechWorkID == s
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

if(PromoteFromWeb):
	_ad = requests.get('https://act8team.com/elvexsocial/get_advertisment.php')
	if _ad.status_code == 200 and not _ad.json()['response'] == None:
		for ad in  _ad.json()['response']:
			fprint(""+Fore.MAGENTA+'[ALERT] '+Fore.RESET+ad)


@synchronized
def IconCreate():
	global TechWorkID
	global trayActions
	global icon
	global DisableTray
	if(DisableTray): return
	icon('elvex', Image.open(BytesIO(requests.get("https://avatars3.githubusercontent.com/u/56801454?s=400&u=0ca69763a92ebb07e3bcf1264d17eaed40682467&v=4").content)), menu=menu(
		item('-- Elvex SOCIAL v'+str(version),trayActions.none, enabled=False),
		item('Dashboard', trayActions.dashboardOpen),
		item('Server settings', menu(
			item("Maintenance", menu(
				item('Disabled', lambda: trayActions.switchTechWorks(-1), checked=lambda i: trayActions.GetCheckedMaintenance(-1)),
				item('Maintenance', lambda: trayActions.switchTechWorks(0), checked=lambda i: trayActions.GetCheckedMaintenance(0)),
				item('Update', lambda: trayActions.switchTechWorks(1), checked=lambda i: trayActions.GetCheckedMaintenance(1)),
				item('Not listed', lambda: trayActions.switchTechWorks(2), checked=lambda i: trayActions.GetCheckedMaintenance(2))
			))
		)),
		item('Restart', trayActions.restart),
		item('Exit', trayActions.exit))).run()

loggedMethods = []

def isMethod(method):
	global jsonMessage
	global loggedMethods
	if(method not in loggedMethods):
		loggedMethods.append(method)
	return jsonMessage['act'] == method

class ResponseManager(object):
	def __init__(self):
		self.Responses = []
	def SetError(self, error_code):
		global Response
		global MessageDelay
		time.sleep(MessageDelay)
		Response = EncodedString(json.dumps({'error': error_code}))
		return True
	def SetOkResponse(self,response_data = {}):
		response_data['response'] = "OK"
		global Response
		global MessageDelay
		time.sleep(MessageDelay)
		Response = EncodedString(json.dumps(response_data))
		return True
	def isArgument(self, arg):
		global jsonMessage
		return arg in jsonMessage['args']
	def isntArgument(self,arg):
		global jsonMessage
		return arg not in jsonMessage['args']
	def isArguments(self,*args):
		global jsonMessage
		for arg in args:
			if(arg not in jsonMessage['args']):
				return False
		return True
	def isntArguments(self,*args):
		global jsonMessage
		for arg in args:
			if(arg in jsonMessage['args']):
				return False
		return True
	def GetArgument(self,arg):
		global jsonMessage
		if(self.isArgument(arg)):
			return jsonMessage['args'][arg]
		else:
			return ""

class HTTPHandler(BaseHTTPRequestHandler):
	
	#Handler for the GET requests
	def do_GET(self):
		try:
			mimetype='text/html'
			self.send_response(200)
			self.send_header('Content-type',mimetype)
			self.end_headers()
			if(self.path == "/"):
				self.wfile.write(("<title>ELVEX SOCIAL</title>").encode())
				self.wfile.write("<button>do nothing</button>".encode())
			else:
				self.send_response(404)
				self.wfile.write(("<title>Not Found</title>").encode())
				self.wfile.write("<h1>404 Not Found</h1><hr>This page doesn't exists. You will be redirected to the home page in 5 seconds.<script>window.onload = function(){ setTimeout(function(){ window.location.href = '/'; }, 5000); }</script>".encode())
			return
		except IOError:
			self.set_error(404, "File Not Found.")
			return
	def do_POST(self):
		return
	def log_message(self, format, *args):
		Logger("[HTTP] %s - - [%s] %s\n" % (self.address_string(),self.log_date_time_string(),format%args))
		return

TechWorkID = -1
rm = ResponseManager()
def HTTPAServer():
	print("HTTP server started at 127.0.0.1:55155", CT.INFO)
	server = HTTPServer(('', 55155), HTTPHandler)
	server.serve_forever()

def IOelvex():
	global server
	global cipher
	global rm
	global jsonMessage
	global Response
	global TechWorkID
	isDebugRun = False
	Response = ""
	while(True):
		try:
			bap = server.recvfrom(bufferSize)
			message = str(bap[0].decode())
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
			if(jsonMessage['act'] in BannedMethods):
				rm.SetError("METHOD_UNAVAILABLE")
				server.sendto(Response, address)
				continue
			if(isMethod("account.Create")):
				if (rm.isntArguments('login', 'pswd')):
					rm.SetError("NO_ARGS")
				else:
					r = AddUser(rm.GetArgument('login'), rm.GetArgument('pswd'),regip=str(address[0]))
					if(r != "OK"):
						rm.SetError(r)
					else:
						rm.SetOkResponse()
			elif(isMethod("account.checkPass")):
				if(rm.isntArguments('login', 'pswd')):
					rm.SetError("NO_ARGS")
				else:
					r = GetUser(rm.GetArgument('login'), False)
					if(r == "USER_GONE" or r == "USER_SPACE"):
						rm.SetError(r)
					else:
						if(EStr(rm.GetArgument('pswd')) != r[1]):
							print(r[1])
							print(str(EStr(rm.GetArgument('pswd'))))
							rm.SetError("BAD_PASSWORD")
						else:
							rm.SetOkResponse()
			elif(isMethod("account.get")):
				if(rm.isntArgument('login')):
					rm.SetError("NO_ARGS")
				else:
					r = GetUser(rm.GetArgument('login'))
					if(r == "USER_GONE" or r == "USER_SPACE"):
						rm.SetError(r)
					else:
						r = r
						rm.SetOkResponse({'{}'.format(rm.GetArgument("login")): {'login': r[0], 'avatar': r[1], 'electricity': r[2], 'pp': r[3], 'inventory': json.loads(r[4]), 'customization': json.loads(r[5]), 'bio': r[6], 'stats': json.loads(r[7]), 'banned': bool(r[8])}})
			elif(isMethod("inventory.setCustomization")):
				if(rm.isntArguments('login', 'pswd', 'slot', 'item')):
					rm.SetError("NO_ARGS")
				else:
					r = GetUser(rm.GetArgument("login"))
					if(r == "USER_GONE" or r == "USER_SPACE"):
						rm.SetError(r)
					else:
						inv = r[4]
						if(rm.isntArguments('item') not in inv):
							rm.SetError("NO_ITEM")
						else:
							SetCustomizationUser(r[0], rm.GetArgument('slot'), rm.GetArgument('item'))
							rm.SetOkResponse()
			elif isMethod("account.getBanReason"):
				if(rm.isntArguments('login', 'pswd')):
					rm.SetError("NO_ARGS")
				else:
					r = GetUser(rm.GetArgument('login'), False)
					if(type(r) == str):
						rm.SetError(r)
					elif(EStr(rm.GetArgument('pswd')) != r[1]):
						rm.SetError("WRONG_PASS")
					else:
						r = GetBanReason(rm.GetArgument('login'))
						if(type(r) == str):
							rm.SetError(r)
						elif(type(r) == int):
							rm.SetOkResponse({'ban_reason': r})
						else:
							rm.SetError("UNKNOWN")
			elif(isMethod("market.get")):
				rm.SetOkResponse({'items': GetStoreItems()})
			elif isMethod("market.getTimer"):
				rm.SetOkResponse({'seconds_left': GetStoreTimer()})
			elif(isMethod("market.buyItem")):
				if(rm.isntArguments('login', 'pswd','slot')):
					rm.SetError("NO_ARGS")
				else:
					StoreItems = GetStoreItems()
					try:
						tttt = int(rm.GetArgument('slot'))
						del tttt
						r = GetUser(rm.GetArgument('login'),False)
						if(r == "USER_GONE" or r == "USER_SPACE"):
							rm.SetError(r)
						else:
							if(EStr(rm.GetArgument("pswd")) != r[1]):
								rm.SetError("WRONG_PASS")
								server.sendto(Response, address)
								continue
							r = GetStoreItem(int(rm.GetArgument('slot')))
							if(type(r) == str):
								rm.SetError("NO_INDEX")
							else:
								if(GetUserBalance(rm.GetArgument('login')) < r[2]):
									rm.SetError("NO_CASH")
								else:
									EditUser(rm.GetArgument('login'), "electricity", GetUserBalance(rm.GetArgument('login'))-r[1])
									AddInvUser(rm.GetArgument('login'), r[0])
									rm.SetOkResponse()
					except Exception:
						rm.SetError("INVALID_ARG")
			elif(isMethod("crates.open")):
				if(rm.isntArguments("inv_index", "login", "pswd")):
					rm.SetError("NO_ARGS")
				else:
					UserData = GetUser(rm.GetArgument("login"), False)
					if not (UserData[1] == EStr(rm.GetArgument("pswd"))):
						rm.SetError("WRONG_PASS")
					else:
						UserInventory = json.loads(UserData[5])
						if(isCrate(UserInventory[rm.GetArgument("inv_index")])):
							final_item = GetCrateItem(UserInventory[rm.GetArgument("inv_index")])
							RemInvUser(rm.GetArgument("login"), rm.GetArgument("inv_index"))
							AddInvUser(rm.GetArgument("login"), final_item)
							rm.SetOkResponse({"result": final_item})
						else:
							rm.SetError("ISNT_CRATE")

						
			elif(isMethod('debug.raiseError')):
				if(isDebugRun):
					unkFunc()
			elif(isMethod('server.isAlive')):
				if (TechWorkID == -1):
					rm.SetOkResponse({"alive": "alive", "server_name": config['Connection']['servername']})
				else:
					rm.SetOkResponse({"alive": "procedures", "tech_id": TechWorkID, "server_name": config['Connection']['servername']})
			else:
				rm.SetError("BAD_REQUEST")
			server.sendto(Response, address)
		except Exception as e:
			rm.SetError("EXCEPTION_TASK")
			server.sendto(Response, address)

@synchronized
def InputConsole():
	while (true):
		sys.stdout.write('> ')
		cmd = sys.stdin.readline()
		cmd = cmd.split('\n')[0]
		elvex_module.CommandHandler().Run(cmd)

TrayThread = threading.Thread(target=IconCreate)
HTTPThread = threading.Thread(target=HTTPAServer)
IOThread = threading.Thread(target=IOelvex)
ConsoleThread = threading.Thread(target=InputConsole)
TrayThread.start()
IOThread.start()
HTTPThread.start()
time.sleep(0.7)
ConsoleThread.start()
TrayThread.join()
IOThread.join()
HTTPThread.join()
time.sleep(0.7)
ConsoleThread.join()