print("Loading libraries...")
import server_settings, time, os, socket, threading, sys, requests, json, errno, pprint, psycopg2, re, hmac, hashlib, base64, psycopg2.extras, uuid
from threading import Thread
from inspect import signature
# DB connection


db = psycopg2.connect(host=server_settings.DB_HOST, database="elvexsocial", user=server_settings.DB_USER, password=server_settings.DB_PASSWORD)
dc = db.cursor()
dc.execute('''CREATE TABLE IF NOT EXISTS users (
	-- Service
	user_id serial PRIMARY KEY,
	username text,
	passhash text, 
	avatar int DEFAULT 0,
	lastonline int DEFAULT 0,
	permission int DEFAULT 0,
	-- Game
	pp int DEFAULT 0,
	electricity int DEFAULT 0,
	inventory text DEFAULT '{"inventory": [], "equipment": {"item1": null, "item2": null, "item3": null, "item4": null, "item5": null, "skin_head": null, "skin_lamp": null, "skin_body": null, "skin_legs": null, "skin_color": null, "perk1": null, "perk2": null, "perk3": null\}\}',
	stats text DEFAULT '\{\}',
	bio text DEFAULT 'No bio provided.'
	)''')
db.commit()
server_settings.PUBLIC_IP = requests.get("https://api.ipify.org/").text

if(server_settings.DISCORD_WEBHOOK == ""):
	print("Put Discord webhook into your settings!")
	os._exit(0)

OLD_PRINT = print
if not os.path.exists(".logs"):
	os.mkdir(".logs")

def is_json(myjson):
  try:
    json_object = json.loads(myjson)
  except ValueError as e:
    return False
  return True

# PRINT OVERWRITTEN
def print(msg, isLogger = True, end="\n"):
	msg =  str(msg) + end
	sys.stdout.write(msg)
	return

print("Log started at "+str(time.strftime("%Y-%m-%d %H:%M:%S",time.gmtime(time.time()))))

class SocialHolder(object):
	def __init__(self):
		self.methods = {}

def WebhookSend(url,content,username, embeds = []):
	data = {}
	data['content'] = content
	data['username'] = username
	data['embeds'] = embeds
	result = requests.post(url, data=json.dumps(data), headers={"Content-Type": "application/json"})
	return result

class Security(object):
	def hmac(self, key, val):
		key = key.encode()
		val = val.encode()
		return hmac.new(key, val, hashlib.sha256).hexdigest()

class DbManager(object):
	def __init__(self):
		global db
		global dc
		self.db = db
		self.dc = dc
		return
	def Insert(self,tablename, **kwargs):
		columns = []
		valuePlaceholders = []
		values = []
		for column, value in kwargs.items():
			columns.append(column)
			valuePlaceholders.append('%s')
			values.append(value)

		QUERY = "INSERT INTO " + tablename + " (%s) VALUES (%s)" % (', '.join(columns), ', '.join(valuePlaceholders))
		try:
			self.dc.execute(QUERY, values)
			self.db.commit()
			return True
		except Exception as e:
			raise e
			return False
	def RegisterNewUser(self, username, password):
		password = Security().hmac(server_settings.ENCODING_KEY, password)
		insertion = self.Insert("users", username=username, passhash=password)
		return insertion

dbm = DbManager()



class Social(object):
	def __init__(self):
		self.methods = {}
	class Method(object):
		def __init__(self, call_name, description, callback, isAuthNeeded = False):
			global soc
			self.call_name = call_name
			self.description = description
			self.auth = isAuthNeeded
			self.callback = callback
			soc.methods[call_name] = self
		def RunCallback(self, **args):
			return self.callback(**args)
	class Errors(object):
		def __init__(self):
			self.Errors = {

				"INTERNAL_ERROR": {"error": "INTERNAL_ERROR", "human_readable": "Something went wrong, we are not sure what, but we will investigate this!", "aum0b_readable": "01001000 01100101 01101100 01101100 01101111 00101100 00100000 01010111 01101111 01110010 01101100 01100100 00100001"},
				"REQUIRED_JSON_REQUEST": {"error": "REQUIRED_JSON_REQUEST", "human_readable": "Request sent to server doesn't represent the JSON input."},
				"PROVIDE_ARGS": {"error": "PROVIDE_ARGS", "human_readable": "Request sent to server doesn't have arguments."},
				"PROVIDE_METHOD": {"error": "PROVIDE_METHOD", "human_readable": "Request sent to server doesn't have method."},
				"TOO_MANY_ARGS": {"error": "TOO_MANY_ARGS", "human_readable": "In request, sent to server was provided too many arguments."},
				"NO_ACCESS": {"error": "NO_ACCESS", "human_readable": "Request sent to server represents forbidden action."},
				"FEW_ARGS": {"error": "FEW_ARGS", "human_readable": "Request sent to server doesn't have required arguments."},
				"INPROPPERATE_USERNAME": {"error": "INPROPPERATE_USERNAME", "human_readable": "Username, which you trying to use is inpropperate."},
				"SMOLL_PP": {"error": "SMOLL_PP", "human_readable": "Some of arguments given to server needs to be longer than specific amount of symbols."},
				"GIANT_PP": {"error": "GIANT_PP", "human_readable": "Some of arguments given to server are too big."},
				"TOO_MANY_CONNECTIONS": {"error": "TOO_MANY_CONNECTIONS", "human_readable": "You have too many connections on one IP address."}
			}
		def Drop(self, errname, selfDrop = False, clientData = {}, clientIP = "", Additional = ""):
			if(errname not in self.Errors):
				print("Hit Internal Error!")
				self.Drop("INTERNAL_ERROR", True)
				return False
			AddInfo = ""
			if(selfDrop): AddInfo += "This is **self-drop**!\n"
			if(not clientData == {} and not clientIP == ""): AddInfo += "Client IP: `{0}`\nClient Request:\n```json\n{1}\n```\n".format(clientIP, clientData)
			AddInfo = AddInfo + Additional
			if(AddInfo == ""): AddInfo = "Nothing more."
			WebhookSend(server_settings.DISCORD_WEBHOOK, "", "ElvexSocial", [{
				"content": "Wild error approached in Content Delivery!\nPlease check.",
				"title": "Error Exception",
				"color": 13979446,
				"timestamp": time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime( time.time())),
				"author": {
					"name": "{0} ({1})".format(server_settings.SERVER_NAME, server_settings.SERVER_REGION),
					"icon_url": "https://avatars2.githubusercontent.com/u/56801454?s=200&v=4",
				},
				"description": "Server is running on `{0}:{1}` ({2}:{1}).".format(server_settings.PUBLIC_IP, server_settings.SERVER_PORT, server_settings.SERVER_IP),
				"fields": [
					{
					"name": errname,
					"value": "```json\n{0}\n```".format(json.dumps(self.Errors[errname], sort_keys=True, indent=4, separators=(',', ': ')))
					},
					{
					"name": "Additional Information",
					"value": AddInfo
					}
				]
				}])
			return json.dumps(self.Errors[errname])

def AuthorizationRequired(level = 0): # 0 - Player, 1 - Premium Account?, 2 - Moderator, 3 - Developer
	def _authReq(func):
		def inner1(*args, **kwargs):
			if(level > 3 or level < 0):
				return json.dumps(errs.Drop("INTERNAL_ERROR", Additional = "Requested %s level of access in `%s`." % (level, str(func))))
			if('authKey' not in kwargs):
				print('no authkey')
			for a in kwargs:
				print(a)
			for a in dwargs:
				print(a)
			ret = func(*args, **kwargs)
			return ret
		return inner1
	return _authReq

class ResponseComposer(object):
	def __init__(self):
		return
	def OK(self, additionalObj = {}):
		res = {"response": "OK"}
		res.update(additionalObj)
		res = json.dumps(res)
		return res

def NoAccess(func):
	def inner(*arg, **kwarg):
		return json.dumps(errs.Drop("NO_ACCESS"))
	return inner

errs = Social.Errors()
soc = Social()

class Client(object):
	def __init__(self, conn, addr,uid):
		self.conn = conn
		self.uuid = uid
		self.ip, self.port = addr
		self.isThreading = False
		self.vars = {}
		return
	def StartThread(self):
		if(self.isThreading):
			print("Client (%s) is already in thread." % self.uuid)
			return False
		self.thread = Thread(target=ContentDelivery_UserThread, args=(self.conn, self.uuid,))
		self.thread.start()
		self.isThreading = True
		return True
	def SetVar(self, var, val):
		self.vars[str(var)] = val
	def GetVar(self, var):
		return self.vars[str(var)] if str(var) in self.vars else False

class ClientComposer(object):
	def __init__(self):
		self.Clients = {}
		self.SameIP = {}
	def AddClient(self,conn, addr):
		ClientUUID =  uuid.uuid4()
		if(addr[0] not in self.SameIP): self.SameIP[addr[0]] = 1
		else: self.SameIP[addr[0]] += 1
		self.Clients[ClientUUID] = Client(conn=conn, addr=addr, uid=ClientUUID)
		return ClientUUID
	def GetClient(self,_uuid):
		return self.Clients[_uuid] if _uuid in self.Clients else False
	def RemoveClient(self, _uuid):
		if not (_uuid in self.Clients): return False
		self.SameIP[self.Clients[_uuid].ip] -= 1
		print("[-] Session %s closed. (%s/%s)" % (_uuid, self.SameIP[self.Clients[_uuid].ip], server_settings.MAX_CONNECTIONS))
		del self.Clients[_uuid]
		return True

def ContentDelivery_UserThread(conn, uid):

	if(cc.SameIP[cc.GetClient(uid).ip] > server_settings.MAX_CONNECTIONS):
		conn.sendall(errs.Drop("TOO_MANY_CONNECTIONS").encode())
		cc.RemoveClient(uid)
		conn.close()
		return
	print("[+] New session with ID %s was started. (%s/%s)" % (uid, str(cc.SameIP[cc.GetClient(uid).ip]), str(server_settings.MAX_CONNECTIONS)))
	try:
		while True:
			data = conn.recv(1024)
			data = data.decode()
			if('User-Agent:' in data):
				cc.RemoveClient(uid)
				conn.close()
				return
			if not data:
				break
			if not is_json(data):
				conn.sendall(errs.Drop("REQUIRED_JSON_REQUEST", clientData=data, clientIP = cc.GetClient(uid).ip).encode())
				continue
			data = json.loads(data)
			if('method' not in data):
				conn.sendall(errs.Drop("PROVIDE_METHOD", clientData=data, clientIP = cc.GetClient(uid).ip).encode())
				continue
			if('args' not in data):
				conn.sendall(errs.Drop("PROVIDE_ARGS", clientData=data, clientIP = cc.GetClient(uid).ip).encode())
				continue

			if(data['method'] in soc.methods):
				try:
					# -1 due to `self` parameter
					sc = signature(soc.methods[data['method']].callback).parameters
					if('self' in sc):
						del sc['self']
					if(len(sc)  < len(data['args'])):
						conn.sendall(errs.Drop("TOO_MANY_ARGS", clientData = data, clientIP = cc.GetClient(uid).ip).encode())
						continue
					res = soc.methods[data['method']].RunCallback(**data['args'])
				except Exception as e:
					conn.sendall(errs.Drop("INTERNAL_ERROR", clientData = data, clientIP = cc.GetClient(uid).ip, Additional = '**Error Exception**:\n`'+str(e)+'`').encode())
					continue
				conn.sendall(res.encode())
			else:
				conn.sendall(errs.Drop("INTERNAL_ERROR", clientData = data, clientIP = cc.GetClient(uid).ip).encode())
		cc.RemoveClient(uid)
		conn.close()
	except ConnectionResetError:
		cc.RemoveClient(uid)
		conn.close()
	except Exception as e:
		#raise e
		WebhookSend(server_settings.DISCORD_WEBHOOK, "", "ElvexSocial", [{
				"content": "@everyone Something wrong in ContentDeliveryPersonal sockets!\nPlease check.",
				"title": "Error Exception",
				"color": 13979446,
				"timestamp": time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime( time.time())),
				"author": {
					"name": "{0} ({1})".format(server_settings.SERVER_NAME, server_settings.SERVER_REGION),
					"icon_url": "https://avatars2.githubusercontent.com/u/56801454?s=200&v=4",
				},
				"description": "Server is running on `{0}:{1}` ({2}:{1}).".format(server_settings.PUBLIC_IP, server_settings.SERVER_PORT, server_settings.SERVER_IP),
				"fields": [
					{
					"name": str(e),
					"value": "```json\n{0}\n```".format(str(e))
					},
					{
					"name": "Additional Information",
					"value": '**Error Exception**:\n`'+str(e)+'`'
					}
				]
				}])

cc = ClientComposer()

class MethodCallbacks(object):
	def __init__(self):
		return
	@AuthorizationRequired(level = 3)
	def ListMethods(self):
		global soc
		res = {}
		for m in soc.methods:
			res[m] = soc.methods[m].description
		return ResponseComposer().OK({"methods": res})
	def CreateAccount(self, username = "", password = ""):
		if not (username or password):
			return errs.Drop("FEW_ARGS")
		forbiddenSymbols = ['fuck', 'elvex', 'admin', 'moder','dick']
		if(any(sym in username for sym in forbiddenSymbols)):
			return errs.Drop("INPROPPERATE_USERNAME")
		if not (re.match('^[A-Za-z0-9_-]*$', username)):
			return errs.Drop("INPROPPERATE_USERNAME")
		if(len(password) < 5 or len(username) < 4):
			return errs.Drop("SMOLL_PP")
		r = dbm.RegisterNewUser(username, password)
		if(len(password) > 64 or len(username) > 15):
			return errs.Drop("GIANT_PP")
		if not r:
			return errs.Drop("INTERNAL_ERROR")
		return ResponseComposer().OK()


mc = MethodCallbacks()

#######################
# Registering methods
soc.Method("dev.listmethods", "", mc.ListMethods)
soc.Method("account.create", "Create a new user account", mc.CreateAccount)
print("Everything is ready to start the server...")