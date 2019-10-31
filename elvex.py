import time
import os
from enum import Enum
from time import gmtime, strftime
from colorama import Fore, Back, init
import random
import sys
import math
import json
import sqlite3
import platform
import hmac
import hashlib
import base64
import binascii
import re
import elvex
import inspect
from OpenSSL import crypto, SSL
from socket import gethostname
import psutil
import prompt_toolkit
from time import gmtime, mktime
try:
    import readline
except ImportError:
    import pyreadline as readline
import npyscreen
if(platform.system() == "Windows"):
	import subprocess

db_AdditionalsVer = 1
db_usersVer = 1
version = 3
oprint = print



def Void():
	umm = "umm"
	del umm
try:
	ohelp = help
except Exception:
	Void()

def clear():
	"""Clear the output."""
	if(platform.system() == "Windows"): os.system("cls")
	else: os.system("clear")

NotList = ["Void","Enum", "gmtime", "strftime", "init", "ohelp", "CT", "oprint", "round50", "create_self_signed_cert","completer","v", "dbgSwitchErrorDisplay", "dbgNoDebug"]
def help():
	"""List of all functions."""
	global NotList
	if not(isDebugger):
		return
	cmds = 0
	for name, val in elvex.__dict__.items():
		if callable(val) and name not in NotList:
			try:
				args = inspect.getfullargspec(val)[0]
			except Exception:
				continue
			args = ', '.join(args)
			if(name.startswith("nolist_")):
				continue
			if(name.startswith("dbg")):
				name = Fore.CYAN + name + Fore.RESET
			cmds += 1
			if(str(val.__doc__) == "None"):
				print(name + "(" + args + ") - No description.", CT.INFO)
			else:
				print(name + "(" + args + ") - " + val.__doc__, CT.INFO)
	if(cmds > 0):
		print("There is "+Fore.GREEN+str(cmds)+Fore.RESET + " functions in total.")
	else:
		print("There is "+Fore.RED+str(cmds)+Fore.RESET + " functions in total.")

StartTime = time.time()

isDebugger = False

true = True
false = False

def round50(n):
    return round(n * 2, -2)

init(autoreset=true)

if not(os.path.isfile("current.log")):
	with open("current.log", "w") as w:
		w.write("")

with open("current.log", "w") as w:
	w.write("")

try:
	os.mkdir("log")
except FileExistsError:
	idc = "i dont care"

if not(os.path.isfile("log/unix"+str(StartTime)+".log")):
	with open("log/unix"+str(StartTime)+".log", "w") as w:
		w.write("")

with open("log/unix"+str(StartTime)+".log", "w") as w:
	w.write("")

class CT(Enum):
	WARN = 1
	INFO = 2
	ERROR = 3
	NONE = 4

def EncodedString(stri):
	"""Encodes string."""
	return str.encode(stri)

def eprint(t):
	"""Prints with newline."""
	sys.stdout.write(t+'\n')

def Logger(stri,type = CT.NONE):
	"""Add message to log."""
	global StartTime
	if(type == CT.NONE):
		with open("current.log", "a") as w:
			w.write("[NONE]["+strftime("%Y-%m-%d %H:%M:%S", gmtime())+"] "+stri+"\n")
		with open("log/unix"+str(StartTime)+".log", "a") as w:
			w.write("[NONE]["+strftime("%Y-%m-%d %H:%M:%S", gmtime())+"] "+stri+"\n")
		return
	if(type == CT.WARN):
		with open("current.log", "a") as w:
			w.write("[WARN]["+strftime("%Y-%m-%d %H:%M:%S", gmtime())+"] "+stri+"\n")
		with open("log/unix"+str(StartTime)+".log", "a") as w:
			w.write("[WARN]["+strftime("%Y-%m-%d %H:%M:%S", gmtime())+"] "+stri+"\n")
		return
	if(type == CT.INFO):
		with open("current.log", "a") as w:
			w.write("[INFO]["+strftime("%Y-%m-%d %H:%M:%S", gmtime())+"] "+stri+"\n")
		with open("log/unix"+str(StartTime)+".log", "a") as w:
			w.write("[INFO]["+strftime("%Y-%m-%d %H:%M:%S", gmtime())+"] "+stri+"\n")
		return
	if(type == CT.ERROR):
		with open("current.log", "a") as w:
			w.write("[ERROR]["+strftime("%Y-%m-%d %H:%M:%S", gmtime())+"] "+stri+"\n")
		with open("log/unix"+str(StartTime)+".log", "a") as w:
			w.write("[ERROR]["+strftime("%Y-%m-%d %H:%M:%S", gmtime())+"] "+stri+"\n")
		return

# "unix"+str(StartTime)+".log"

def is_json(myjson):
  """Check if string is json."""
  try:
    json_object = json.loads(myjson)
  except ValueError as e:
    return False
  return True

def LogPrint(stri,type = CT.NONE):
	"""Print and add to log."""
	global StartTime
	if(type == CT.NONE):
		eprint("[NONE]" + Back.WHITE+Fore.BLACK + "["+strftime("%Y-%m-%d %H:%M:%S", gmtime())+"]"+Back.RESET+Fore.RESET+" "+stri)
		with open("current.log", "a") as w:
			w.write("[NONE]["+strftime("%Y-%m-%d %H:%M:%S", gmtime())+"] "+stri+"\n")
		with open("log/unix"+str(StartTime)+".log", "a") as w:
			w.write("[NONE]["+strftime("%Y-%m-%d %H:%M:%S", gmtime())+"] "+stri+"\n")
		return
	if(type == CT.WARN):
		eprint(Fore.YELLOW+"[WARN]"+Back.WHITE+Fore.BLACK+"["+strftime("%Y-%m-%d %H:%M:%S", gmtime())+"]"+Back.RESET+Fore.RESET+" "+stri)
		with open("current.log", "a") as w:
			w.write("[WARN]["+strftime("%Y-%m-%d %H:%M:%S", gmtime())+"] "+stri+"\n")
		with open("log/unix"+str(StartTime)+".log", "a") as w:
			w.write("[WARN]["+strftime("%Y-%m-%d %H:%M:%S", gmtime())+"] "+stri+"\n")
		return
	if(type == CT.INFO):
		eprint(Fore.CYAN+"[INFO]"+Back.WHITE+Fore.BLACK+"["+strftime("%Y-%m-%d %H:%M:%S", gmtime())+"]"+Back.RESET+Fore.RESET+" "+stri)
		with open("current.log", "a") as w:
			w.write("[INFO]["+strftime("%Y-%m-%d %H:%M:%S", gmtime())+"] "+stri+"\n")
		with open("log/unix"+str(StartTime)+".log", "a") as w:
			w.write("[INFO]["+strftime("%Y-%m-%d %H:%M:%S", gmtime())+"] "+stri+"\n")
		return
	if(type == CT.ERROR):
		eprint(Fore.RED+"[ERROR]"+Back.WHITE+Fore.BLACK+"["+strftime("%Y-%m-%d %H:%M:%S", gmtime())+"]"+Back.RESET+Fore.RESET+" "+stri)
		with open("current.log", "a") as w:
			w.write("[ERROR]["+strftime("%Y-%m-%d %H:%M:%S", gmtime())+"] "+stri+"\n")
		with open("log/unix"+str(StartTime)+".log", "a") as w:
			w.write("[ERROR]["+strftime("%Y-%m-%d %H:%M:%S", gmtime())+"] "+stri+"\n")
		return

class print():
	"""Print a message."""
	def __init__(self,msg,typeo = CT.NONE):
		LogPrint(msg,typeo)

def IsUserExists(login):
	"""Is user exists in Elvex DB?"""
	conn = sqlite3.connect('users.db')
	c = conn.cursor()
	r = c.execute("SELECT * FROM users WHERE username = '{}'".format(login))
	if(r.fetchone()):
		return True
	else:
		return False

def EStr(stre):
	"""Encode string to password."""
	a = hmac.new(b'_EaLEoELXoELWoXLOWQlWA_1+-2#)LC<E!!!(!0CC@@@@A', stre.encode(), hashlib.sha256)
	return str(a.hexdigest())

def AddUser(login, pswd, avatar = 0, electricity = 0, ppcount = 0.0, inventory = "[]", customization = '{"droidColor": "blue", "lampColor": "blue","hat": "none", "body": "none", "hands": "none", "legs": "none"}', bio = "Not specified.", stats = "{}", banned = False, regip = "0.0.0.0", accessible = True, ban_reason = -1):
	"""Create user in Elvex DB."""
	if(IsUserExists(login)):
		print("Creation user with username "+login+" failed. User already exists.", CT.ERROR)
		return "USER_EXISTS"
	if(login.isspace() or login == ""):
		return "USER_SPACE"
	h = hmac.new(b'_EaLEoELXoELWoXLOWQlWA_1+-2#)LC<E!!!(!0CC@@@@A', pswd.encode(), hashlib.sha256)
	pswd = str(h.hexdigest())
	if(re.search('[^a-zA-Z0-9_]', login) is not None):
		return "USER_CHARACTERS"
	conn = sqlite3.connect('users.db')
	c = conn.cursor()
	r = c.execute("SELECT * FROM bannednames WHERE lower(name) = '{}'".format(login.lower()))
	if(r.fetchone()):
		return "NAME_BANNED"
	#        TEXT, TEXT, INT, FLOAT, TEXT, TEXT, TEXT, TEXT, BOOL, TEXT
	c.execute("INSERT INTO users VALUES ('{}', '{}', {}, {}, {}, '{}', '{}', '{}', '{}', {}, '{}', {}, {})".format(login, pswd, str(avatar), str(electricity), str(ppcount),inventory, customization,bio, stats, str(banned), regip, str(accessible), str(ban_reason)))
	conn.commit()
	conn.close()
	return "OK"


def RemoveUser(login):
	"""Remove user from Elvex DB."""
	if not (IsUserExists(login)):
		print("Removal failed. User doesn't exists. ("+login+")", CT.ERROR)
		return "USER_GONE"
	if(login.isspace()):
		return "USER_SPACE"
	conn = sqlite3.connect('users.db')
	c = conn.cursor()
	c.execute("UPDATE users SET accessible = false WHERE username = '{}'".format(login))
	conn.commit()
	conn.close()
	conn = sqlite3.connect('users.db')
	c = conn.cursor()
	c.execute("INSERT INTO bannednames VALUES ('{}')".format(login))
	conn.commit()
	conn.close()
	return "OK"

def RestoreUser(login):
	"""Restores user profile."""
	if not (IsUserExists(login)):
		print("Restoring failed. User doesn't exists. ("+login+")", CT.ERROR)
		return "USER_GONE"
	if(login.isspace()):
		return "USER_SPACE"
	conn = sqlite3.connect('users.db')
	c = conn.cursor()
	c.execute("UPDATE users SET accessible = true WHERE username = '{}'".format(login))
	conn.commit()
	conn.close()
	conn = sqlite3.connect('users.db')
	c = conn.cursor()
	c.execute("DELETE FROM bannednames WHERE name = '{}'".format(login))
	conn.commit()
	conn.close()
	return "OK"
def IsAccessibleUser(username):
	"""Is user profile accessible?"""
	conn = sqlite3.connect('users.db')
	c = conn.cursor()
	r = c.execute("SELECT accessible FROM users WHERE username = '{}'".format(username))
	r = r.fetchone()
	return bool(r[0])
def ListUsers()->'User list':
	"""List all users."""
	conn = sqlite3.connect('users.db')
	c = conn.cursor()
	a = c.execute("SELECT * FROM users")
	for b in a:
		print("- "+b[0])
	conn.close()

def BanUser(login,reason = -1):
	"""Ban player from Elvex."""
	if not (IsUserExists(login)):
		print("Ban failed. User doesn't exists. ("+login+")", CT.ERROR)
		return "USER_GONE"
	if(login.isspace()):
		return "USER_SPACE"
	conn = sqlite3.connect('users.db')
	c = conn.cursor()
	c.execute("UPDATE users SET banned = true WHERE username = '{}'".format(login))
	c.execute("UPDATE users SET ban_reason = {} WHERE username = '{}'".format(reason,login))
	conn.commit()
	conn.close()
	return "OK"

def UnbanUser(login):
	"""Pardon a player."""
	if not (IsUserExists(login)):
		print("Ban failed. User doesn't exists. ("+login+")", CT.ERROR)
		return "USER_GONE"
	if(login.isspace()):
		return "USER_SPACE"
	conn = sqlite3.connect('users.db')
	c = conn.cursor()
	c.execute("UPDATE users SET banned = false WHERE username = '{}'".format(login))
	conn.commit()
	conn.close()
	return "OK"

flushing = False
flushingTried = 0

def FlushUsers():
	"""(WARNING) Delete all users."""
	global flushing
	global flushingTried
	if(flushing == False):
		print("To flush all users use FlushUsers() again.",CT.WARN)
		flushing = True
		flushingTried = time.time()
		return
	if(flushing == True and flushingTried+30 < time.time()):
		print("To flush all users use FlushUsers() again.",CT.WARN)
		flushing = True
		flushingTried = time.time()
		return
	conn = sqlite3.connect('users.db')
	c = conn.cursor()
	c.execute("DELETE FROM users")
	c.execute("DELETE FROM bannednames")
	conn.commit()
	conn.close()
	print("Users were flushed.", CT.INFO)
	flushing = False

def IsUserBanned(username):
	"""Check if user is banned or no."""
	conn = sqlite3.connect('users.db')
	c = conn.cursor()
	a = c.execute("SELECT banned FROM users WHERE username = '{}'".format(username))
	a = bool(a.fetchone()[0])
	conn.close()
	return a

def GetBanReason(username):
	"""Get reason of ban for user."""
	if not IsUserExists(username):
		return "USER_GONE"
	if not IsUserBanned(username):
		return "USER_LAW"
	conn = sqlite3.connect('users.db')
	c = conn.cursor()
	a = c.execute("SELECT ban_reason FROM users WHERE username = '{}'".format(username))
	a = a.fetchone()[0]
	conn.close()
	return a

def GetUser(username, safe = True):
	"""Get user by name."""
	global isDebugger
	if not (IsUserExists(username)):
		print("Tried to get user, but user with that name doesn't exists. ("+username+")", CT.ERROR)
		return "USER_GONE"
	elif IsUserBanned(username) and not isDebugger:
		return "USER_BANNED"
	elif not IsAccessibleUser(username) and not isDebugger:
		return "USER_GONE"
	if(username.isspace()):
		return "USER_SPACE"
	conn = sqlite3.connect('users.db')
	c = conn.cursor()
	if(safe):
		a = c.execute("SELECT username, electricity,avatar, ppcount, inventory, customization, bio, stats, banned FROM users WHERE username = '{}'".format(username))
		a = a.fetchone()
	else:
		a = c.execute("SELECT username, passhash, electricity,avatar,ppcount, inventory, customization, bio, stats, banned, regip FROM users WHERE username = '{}'".format(username))
		a = a.fetchone()
	return a

# print(GetUserBalance("test"))

def GetUserBalance(username):
	"""Get user's balance."""
	s = GetUser(username)
	if(type(s) == str):
		return s
	return int(s[1])

def AddInvUser(username,item_code):
	"""Add item to player's inventory."""
	if not (IsUserExists(username)):
		print("Tried to add item to user's inventory, but user with that name doesn't exists. ("+username+")", CT.ERROR)
		return "USER_GONE"
	if(username.isspace()):
		return "USER_SPACE"
	conn = sqlite3.connect("users.db")
	c = conn.cursor()
	a = c.execute("SELECT inventory FROM users WHERE username = '{}'".format(username))
	a = json.loads(a.fetchone()[0])
	a.append(item_code)
	a = json.dumps(a)
	c.execute("UPDATE users SET inventory = '{}' WHERE username = '{}'".format(a,username))
	conn.commit()
	conn.close()
	return "OK"

def RemInvUser(username,index):
	"""Take item from player's inventory."""
	if not (IsUserExists(username)):
		print("Tried to take item from user's inventory, but user with that name doesn't exists. ("+username+")", CT.ERROR)
		return "USER_GONE"
	if(username.isspace()):
		return "USER_SPACE"
	conn = sqlite3.connect("users.db")
	c = conn.cursor()
	a = c.execute("SELECT inventory FROM users WHERE username = '{}'".format(username))
	a = json.loads(a.fetchone()[0])
	del a[index]
	a = json.dumps(a)
	c.execute("UPDATE users SET inventory = '{}' WHERE username = '{}'".format(a,username))
	conn.commit()
	conn.close()
	return "OK"

def SetCustomizationUser(username, n, h):
	"""Set item to customization slot of player."""
	if not (IsUserExists(username)):
		print("Tried to change user's customization, but user with that name doesn't exists. ("+username+")", CT.ERROR)
		return "USER_GONE"
	if(username.isspace()):
		return "USER_SPACE"
	conn = sqlite3.connect("users.db")
	c = conn.cursor()
	a = c.execute("SELECT customization FROM users WHERE username = '{}'".format(username))
	a = json.loads(a.fetchone()[0])
	a[n] = h
	a = json.dumps(a)
	c.execute("UPDATE users SET customization = '{}' WHERE username = '{}'".format(a,username))
	conn.commit()
	conn.close()
	return "OK"

def EditUserPassword(username, currentPass, newPass):
	"""Edit password of user (needs old)."""
	global isDebugger
	if not (IsUserExists(username)):
		print("Tried to change user's password, but user with that name doesn't exists. ("+username+")", CT.ERROR)
		return "USER_GONE"
	elif IsUserBanned(username) and not isDebugger:
		return "USER_BANNED"
	if(username.isspace()):
		return "USER_SPACE"
	conn = sqlite3.connect("users.db")
	c = conn.cursor()
	a = c.execute("SELECT passhash FROM users WHERE username = '{}'".format(username))
	a = str(a.fetchone()[0])
	if not(EStr(currentPass) == a):
		return "USER_WRONG_HASH"
	newPass = EStr(newPass)
	c.execute("UPDATE users SET passhash = '{}' WHERE username = '{}'".format(newPass, username))
	conn.commit()
	conn.close()
	return "OK"

def UnsafeEditUserPassword(username, newPass):
	"""Edit password of user."""
	if not (IsUserExists(username)):
		print("Tried to change user's password, but user with that name doesn't exists. ("+username+")", CT.ERROR)
		return "USER_GONE"
	if(username.isspace()):
		return "USER_SPACE"
	conn = sqlite3.connect("users.db")
	c = conn.cursor()
	a = c.execute("SELECT passhash FROM users WHERE username = '{}'".format(username))
	a = str(a.fetchone()[0])
	newPass = EStr(newPass)
	c.execute("UPDATE users SET passhash = '{}' WHERE username = '{}'".format(newPass, username))
	conn.commit()
	conn.close()
	return "OK"

def ChangeUserStat(username,stat,to):
	"""Change user's statistic."""
	if not (IsUserExists(username)):
		print("Tried to change user's stat, but user with that name doesn't exists. ("+username+")", CT.ERROR)
		return "USER_GONE"
	if(username.isspace()):
		return "USER_SPACE"
	conn = sqlite3.connect("users.db")
	c = conn.cursor()
	a = c.execute("SELECT stats FROM users WHERE username = '{}'".format(username))
	a = json.loads(a.fetchone()[0])
	a[stat] = to
	a = json.dumps(a)
	c.execute("UPDATE users SET stats = '{}' WHERE username = '{}'".format(a,username))
	conn.commit()
	conn.close()
	return "OK"

def EditUser(username, what, how):
	"""Edit user account."""
	global isDebugger
	if not (IsUserExists(username)):
		print("Tried to edit user, but user with that name doesn't exists. ("+username+")", CT.ERROR)
		return "USER_GONE"
	elif IsUserBanned(username) and not isDebugger:
		return "USER_BANNED"
	if(username.isspace()):
		return "USER_SPACE"
	stringlets = ["username", "bio"]
	warners = ["username"]
	if(what == "inventory"):
		print("To change inventory use: AddInvUser() or RemInvUser()")
		return "BAD_REQUEST"
	if(what == "customization"):
		print("To change customization use: SetCustomizationUser()")
		return "BAD_REQUEST"
	if(what == "passhash"):
		print("To change user's password use: EditUserPassword()")
		return "BAD_REQUEST"
	if(what == "stats"):
		print("To change stats use: ChangeUserStat()")
		return "BAD_REQUEST"
	if(what == "banned"):
		print("To change banned state use: BanUser() or UnbanUser()")
		return "BAD_REQUEST"
	if(what == "regip"):
		print("Regip cannot be changed.")
		return "BAD_REQUEST"
	
	conn = sqlite3.connect('users.db')
	c = conn.cursor()
	if(what in stringlets):
		c.execute("UPDATE users SET {} = '{}' WHERE username = '{}'".format(what,how,username))
	else:
		c.execute("UPDATE users SET {} = {} WHERE username = '{}'".format(what,how,username))
	if(what in warners):
		print(username+" just changed "+what+" to "+how,CT.WARN)
	conn.commit()
	conn.close()
	return "OK"

def CreateCrate(item_code, key_item_code, loot_table):
	"""Creates a new crate."""
	conn = sqlite3.connect('additional.db')
	c = conn.cursor()
	if not (is_json(loot_table)):
		return "LOOTTABLE_NOT_JSON"
	c.execute("INSERT INTO crates VALUES ('{}', '{}', '{}')".format(item_code,key_item_code,loot_table))
	conn.commit()
	conn.close()
	return "OK"

def isCrate(item_code):
	"""Checks if item is a crate or no."""
	conn = sqlite3.connect('additional.db')
	c = conn.cursor()
	a = c.execute("SELECT * FROM crates WHERE item_code = '{}'".format(item_code))

	if(a.fetchone()):
		conn.commit()
		conn.close()
		return True
	else:
		conn.commit()
		conn.close()
		return False


def About():
	"""Get information about ELVEX SOCIAL"""
	global isDebugger
	global version
	if not isDebugger:
		return "FAILED"
	print('Elvex SOCIAL v'+str(version))

def GetRandomPoolItem():
	"""Select random item out of shop pool."""
	conn = sqlite3.connect("additional.db")
	c = conn.cursor()
	a = c.execute("SELECT * FROM shop_pool").fetchall()
	a = a
	conn.close()
	return random.choice(a)

def ForceUpdateStore():
	"""Force shop to update its containment."""
	conn = sqlite3.connect("additional.db")
	c = conn.cursor()
	c.execute("DELETE FROM shop_current")
	item = GetRandomPoolItem()
	price = round50(random.randint(item[1], item[2]))
	c.execute("INSERT INTO shop_current VALUES ('{}', {})".format(item[0],str(price)))
	item = GetRandomPoolItem()
	price = round50(random.randint(item[1], item[2]))
	c.execute("INSERT INTO shop_current VALUES ('{}', {})".format(item[0],str(price)))
	item = GetRandomPoolItem()
	price = round50(random.randint(item[1], item[2]))
	c.execute("INSERT INTO shop_current VALUES ('{}', {})".format(item[0],str(price)))
	a = c.execute("SELECT * FROM time_storage WHERE sett = 'store_update';").fetchone()[1]
	c.execute("UPDATE time_storage SET unix = {} WHERE sett = 'store_update'".format(str(int(time.time()))))
	conn.commit()
	conn.close()
	return "SHOP_UPDATED"

def LogStoreItems():
	"""Log current store items."""
	conn = sqlite3.connect("additional.db")
	c = conn.cursor()
	a = c.execute("SELECT * FROM shop_current").fetchall()
	for t in a:
		print(t[0] + " -- " + str(t[1]) +" electricity")
def GetStoreItems():
	"""Get current store items."""
	UpdateStore()
	conn = sqlite3.connect("additional.db")
	c = conn.cursor()
	a = c.execute("SELECT * FROM shop_current").fetchall()
	return a
def UpdateStore():
	"""Update store containment."""
	conn = sqlite3.connect("additional.db")
	c = conn.cursor()
	a = c.execute("SELECT * FROM time_storage WHERE sett = 'store_update';").fetchone()[1]
	if(a+3600 > int(time.time())):
		conn.close()
		return "TIMER_CONTINUES"
	else:
		c.execute("DELETE FROM shop_current")
		item = GetRandomPoolItem()
		price = round50(random.randint(item[1], item[2]))
		c.execute("INSERT INTO shop_current VALUES ('{}', {})".format(item[0],str(price)))
		item = GetRandomPoolItem()
		price = round50(random.randint(item[1], item[2]))
		c.execute("INSERT INTO shop_current VALUES ('{}', {})".format(item[0],str(price)))
		item = GetRandomPoolItem()
		price = round50(random.randint(item[1], item[2]))
		c.execute("INSERT INTO shop_current VALUES ('{}', {})".format(item[0],str(price)))
		c.execute("UPDATE time_storage SET unix = {} WHERE sett = 'store_update'".format(str(int(time.time()))))
		conn.commit()
		conn.close()
		return "SHOP_UPDATED"


def GetStoreTimer():
	"""Get amount of seconds before store updates."""
	UpdateStore()
	conn = sqlite3.connect("additional.db")
	c = conn.cursor()
	a = c.execute("SELECT * FROM time_storage WHERE sett = 'store_update';").fetchone()[1]
	conn.close()
	return 3600-(int(time.time())-a)

def AddItemPool(item_code, min_price, max_price):
	"""Adds item to store pool"""
	conn = sqlite3.connect("additional.db")
	c = conn.cursor()
	c.execute("INSERT INTO shop_pool VALUES ('{}', {}, {})".format(item_code, str(min_price), str(max_price)))
	conn.commit()
	conn.close()
	return "OK"

def GetStoreItem(index):
	"""Get store item by index."""
	items = GetStoreItems()
	if(index >= len(items)):
		return "NO_SUCH_INDEX"
	return items[index]

def ChanceTry(chance):
	"""Try the percentage chance."""
	return random.randrange(0,100) < chance

def GetCrateItem(crate_code):
	"""Get random item of crate."""
	conn = sqlite3.connect("additional.db")
	c = conn.cursor()
	cr = c.execute("SELECT items_in FROM crates WHERE item_code = '{}'".format(crate_code))
	cr = cr.fetchone()[0]
	cr = json.loads(cr)
	cr = sorted(cr.items(), key=lambda x: x[1])
	ItemCode_Result = ""
	while ItemCode_Result == "":
		for i in cr:
			a = ChanceTry(i[1])
			if(a):
				ItemCode_Result = i[0]
	return ItemCode_Result

# -- Debugger-only tools

class nolist_createUser(npyscreen.Form):
	def create(self):
		self.username = self.add(npyscreen.TitleText, name='Username')
		self.pswd = self.add(npyscreen.TitlePassword, name='Password')
		self.avatar = self.add(npyscreen.TitleSlider, name='Avatar', out_of=20,step=1,lowest=0)
		self.elec = self.add(npyscreen.TitleSlider, name='Electricity',step=10000,out_of=1000000000,lowest=0)
		self.pps = self.add(npyscreen.TitleSlider, name='PP', out_of=7450,step=50,lowest=0)
		self.banned = self.add(npyscreen.CheckBox, name='Is banned?')
		self.access = self.add(npyscreen.CheckBox, name='Is removed?')
	def realCreate(*args):
		f = nolist_createUser(name="New User")
		f.edit()
		return f

def dbgCreateUser():
	"""Shows form to create user from debugger."""
	if not(isDebugger): return
	curses.initscr()
	storeData = npyscreen.wrapper_basic(nolist_createUser.realCreate)
	a = AddUser(storeData.username.value, EStr(storeData.pswd.value), int(storeData.avatar.value), int(storeData.elec.value), float(storeData.pps.value), "[]", "\{\}", "", "\{\}", bool(storeData.banned.value), "0.0.0.0", bool(storeData.access.value))
	if(a != "OK"):
		print("There was an error while creating user account ("+a+")", CT.ERROR)
	else:
		print("User "+Fore.CYAN+storeData.username.value+Fore.RESET+" was created successfully!", CT.INFO)


def CalculatePPv2(dmgDealt, dmgTaken, supportPoints):
	"""Perfomance Points calculator"""
	if(supportPoints == 0): bonus = -5
	elif(supportPoints > 0):
		bonus = math.fabs(round(math.atan2(supportPoints, -supportPoints)))+math.tan(supportPoints*11.3777)+(supportPoints/0.5*0.25)
	else:
		supportPoints = math.fabs(supportPoints)
		bonus = math.fabs(round(math.atan2(supportPoints, -supportPoints)))+math.tan(supportPoints*11.3777)+(supportPoints/0.5*0.25)+supportPoints * 2.5
		bonus = -(bonus)
	return -3 + (dmgDealt ** 1.25 - dmgTaken ** 1.2589)/10.5+bonus

# Checking dbs

if not (os.path.isfile("users.db")):
	conn = sqlite3.connect('users.db')
	c = conn.cursor()
	c.execute('''CREATE TABLE users
             (username text, passhash text, avatar int, electricity int, ppcount float, inventory text, customization text, bio text, stats text, banned boolean, regip text, accessible boolean,ban_reason int)''')
	c.execute('''CREATE TABLE bannednames
		(name text)''')
	c.execute('''CREATE TABLE db_info
             (st text, data int)''')
	c.execute('''INSERT INTO db_info VALUES ('ver', {})'''.format(str(db_usersVer)))
	conn.commit()
	conn.close()
	Logger("Created new user database, because users.db was missing.", CT.INFO)

if not (os.path.isfile("additional.db")):
	conn = sqlite3.connect('additional.db')
	c = conn.cursor()
	c.execute('''CREATE TABLE crates
             (item_code text, item_open_code text, items_in text)''')
	c.execute('''CREATE TABLE shop_pool
             (item_code text, min_price int, max_price int)''')
	c.execute('''CREATE TABLE shop_current
             (item_code text, price int)''')
	c.execute('''CREATE TABLE time_storage
             (sett text, unix int)''')
	c.execute('''CREATE TABLE db_info
             (st text, data int)''')
	c.execute('''INSERT INTO time_storage VALUES ('store_update', 0)''')
	c.execute('''INSERT INTO db_info VALUES ('ver', {})'''.format(str(db_AdditionalsVer)))
	conn.commit()
	conn.close()
	Logger("Created new additionals database, because additional.db was missing.", CT.INFO)



if(platform.system() == "Windows"):
	subprocess.check_call(["attrib","+H","users.db"])
	subprocess.check_call(["attrib","+H","additional.db"])

# Logging information about run

Logger("-----------------------")
Logger("Python: "+sys.version)
try:
	import pip
	Logger("Pip: "+pip.__version__)
except ImportError:
	Logger("Pip: Not found.")
foundProc = False
if(platform.system() == "Windows"):
	foundProc = True
	Logger("Processor: "+platform.processor())
elif platform.system() == "Darwin":
	foundProc = True
	os.environ['PATH'] = os.environ['PATH'] + os.pathsep + '/usr/sbin'
	command ="sysctl -n machdep.cpu.brand_string"
	Logger("Processor: "+str(subprocess.check_output(command).strip()))
elif platform.system() == "Linux":
	foundProc = True
	command = "cat /proc/cpuinfo"
	all_info = subprocess.check_output(command, shell=True).strip()
	for line in all_info.split("\n"):
		if "model name" in line:
			Logger("Processor: "+str(re.sub( ".*model name.*:", "", line,1)))

if not foundProc:
	Logger("Processor: Unknown")

Logger("RAM: "+str(psutil.virtual_memory().total/1024/1024)+" MB")
partitions = psutil.disk_partitions()
Logger('Disks:')
diskCount = 0
for p in partitions:
	diskCount += 1
	Logger('[Disk '+str(diskCount)+'] '+p.device+"(mnt: {} / fstype: {})".format(p.mountpoint, p.fstype))

Logger("Users: ")
uCount = 0
for u in psutil.users():
	uCount += 1
	Logger("[User {}] {}".format(str(uCount), u.name))
pidarray = psutil.pids()
npid = {}
for p in pidarray:
	npid[p] = psutil.Process(p).name
Logger("Current processes: ")
for k,v in npid.items():
	Logger("[PID {}]: {}".format(str(k), v))
Logger("-----------------------")

def dbgSwitchErrorDisplay():
	global isFormattedError
	global isDebugger
	if not(isDebugger): return
	isFormattedError = not isFormattedError
	if(isFormattedError): print("Set formatting to "+Fore.CYAN+"PRETTY"+Fore.RESET+".")
	else: print("Set formatting to "+Fore.CYAN+"INFORMATIVE"+Fore.RESET+".")

def dbgNoDebug():
	global isDebugger
	if not isDebugger:
		print("You can only LEAVE debugger, not ENTER.")
		return
	isDebugger = False
	print("You are now moron.")
	return

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
conn.close()

def CompleterLoad():
	global history
	for name, val in elvex.__dict__.items():
		if callable(val) and name not in NotList:
			try:
				args = inspect.getfullargspec(val)[0]
			except Exception:
				continue
			if(name.startswith("nolist_")):
				continue
			history.append_string(name+"()")

def is_valid_command(v):
	return re.match(r"\b[^()]+\((.*)\)$", v) is not None

if(len(sys.argv) > 1 and sys.argv[1] == "debugger"):
	Logger("Debugger initialized.", CT.WARN)
	import curses
	isFormattedError = True
	isDebugger = True
	history = prompt_toolkit.history.InMemoryHistory()
	CompleterLoad()
	session = prompt_toolkit.PromptSession(
        history=history,
        auto_suggest=prompt_toolkit.auto_suggest.AutoSuggestFromHistory(),
        enable_history_search=True)
	validator = prompt_toolkit.validation.Validator.from_callable(is_valid_command, error_message='Not a valid function. (Cannot be executed)', move_cursor_to_end=True)
	while(True):
		oprint(Fore.CYAN+ '> '+Fore.RESET,end='')
		if(isFormattedError):
			a = session.prompt('  ', validator=validator, validate_while_typing=True)
			try:
				eval(a)
			except Exception as e:
				print(str(e), CT.ERROR)
		else:
			a = input()
			eval(a)
