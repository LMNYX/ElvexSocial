import time
import os
from enum import Enum
from time import gmtime, strftime
from colorama import Fore, Back, init
import sys
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
if(platform.system() == "Windows"):
	import subprocess
version = 3
debugger_mode = False
oprint = print
ohelp = help
if(platform.system() == "Windows"):
	def clear(): os.system("cls")
else:
	def clear(): os.system("clear")

def help():
	"""List of all functions."""
	NotList = ["Enum", "gmtime", "strftime", "init", "ohelp", "CT", "oprint"]
	for name, val in elvex.__dict__.items():
		if callable(val) and name not in NotList:
			args = inspect.getfullargspec(val)[0]
			args = ', '.join(args)
			if(str(val.__doc__) == "None"):
				print(name + "(" + args + ") - No description.", CT.INFO)
			else:
				print(name + "(" + args + ") - " + val.__doc__, CT.INFO)

StartTime = time.time()

true = True
false = False


init(autoreset=true)

if not(os.path.isfile("current.log")):
	with open("current.log", "w") as w:
		w.write("")

with open("current.log", "w") as w:
	w.write("")

if not(os.path.isfile("unix"+str(StartTime)+".log")):
	with open("unix"+str(StartTime)+".log", "w") as w:
		w.write("")

with open("unix"+str(StartTime)+".log", "w") as w:
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
		with open("unix"+str(StartTime)+".log", "a") as w:
			w.write("[NONE]["+strftime("%Y-%m-%d %H:%M:%S", gmtime())+"] "+stri+"\n")
		return
	if(type == CT.WARN):
		with open("current.log", "a") as w:
			w.write("[WARN]["+strftime("%Y-%m-%d %H:%M:%S", gmtime())+"] "+stri+"\n")
		with open("unix"+str(StartTime)+".log", "a") as w:
			w.write("[WARN]["+strftime("%Y-%m-%d %H:%M:%S", gmtime())+"] "+stri+"\n")
		return
	if(type == CT.INFO):
		with open("current.log", "a") as w:
			w.write("[INFO]["+strftime("%Y-%m-%d %H:%M:%S", gmtime())+"] "+stri+"\n")
		with open("unix"+str(StartTime)+".log", "a") as w:
			w.write("[INFO]["+strftime("%Y-%m-%d %H:%M:%S", gmtime())+"] "+stri+"\n")
		return
	if(type == CT.ERROR):
		with open("current.log", "a") as w:
			w.write("[ERROR]["+strftime("%Y-%m-%d %H:%M:%S", gmtime())+"] "+stri+"\n")
		with open("unix"+str(StartTime)+".log", "a") as w:
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
		with open("unix"+str(StartTime)+".log", "a") as w:
			w.write("[NONE]["+strftime("%Y-%m-%d %H:%M:%S", gmtime())+"] "+stri+"\n")
		return
	if(type == CT.WARN):
		eprint(Fore.YELLOW+"[WARN]"+Back.WHITE+Fore.BLACK+"["+strftime("%Y-%m-%d %H:%M:%S", gmtime())+"]"+Back.RESET+Fore.RESET+" "+stri)
		with open("current.log", "a") as w:
			w.write("[WARN]["+strftime("%Y-%m-%d %H:%M:%S", gmtime())+"] "+stri+"\n")
		with open("unix"+str(StartTime)+".log", "a") as w:
			w.write("[WARN]["+strftime("%Y-%m-%d %H:%M:%S", gmtime())+"] "+stri+"\n")
		return
	if(type == CT.INFO):
		eprint(Fore.CYAN+"[INFO]"+Back.WHITE+Fore.BLACK+"["+strftime("%Y-%m-%d %H:%M:%S", gmtime())+"]"+Back.RESET+Fore.RESET+" "+stri)
		with open("current.log", "a") as w:
			w.write("[INFO]["+strftime("%Y-%m-%d %H:%M:%S", gmtime())+"] "+stri+"\n")
		with open("unix"+str(StartTime)+".log", "a") as w:
			w.write("[INFO]["+strftime("%Y-%m-%d %H:%M:%S", gmtime())+"] "+stri+"\n")
		return
	if(type == CT.ERROR):
		eprint(Fore.RED+"[ERROR]"+Back.WHITE+Fore.BLACK+"["+strftime("%Y-%m-%d %H:%M:%S", gmtime())+"]"+Back.RESET+Fore.RESET+" "+stri)
		with open("current.log", "a") as w:
			w.write("[ERROR]["+strftime("%Y-%m-%d %H:%M:%S", gmtime())+"] "+stri+"\n")
		with open("unix"+str(StartTime)+".log", "a") as w:
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

def AddUser(login, pswd, avatar = 0, electricity = 0, ppcount = 0.0, inventory = "[]", customization = '{"droidColor": "blue", "lampColor": "blue","hat": "none", "body": "none", "hands": "none", "legs": "none"}', bio = "Not specified.", stats = "{}", banned = False, regip = "0.0.0.0"):
	"""Create user in Elvex DB."""
	if(IsUserExists(login)):
		print("Creation user with username "+login+" failed. User already exists.", CT.ERROR)
		return "USER_EXISTS"
	if(login.isspace()):
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
	c.execute("INSERT INTO users VALUES ('{}', '{}', {}, {}, {}, '{}', '{}', '{}', '{}', {}, '{}')".format(login, pswd, str(avatar), str(electricity), str(ppcount),inventory, customization,bio, stats, str(banned), regip))
	conn.commit()
	conn.close()
	return "OK"


def RemoveUser(login):
	"""Remove user from Elvex DB."""
	if not (IsUserExists(login)):
		print("Removal failed. User doesn't exists. ("+login+")", CT.ERROR)
		return "USER_GONE"
	if(username.isspace()):
		return "USER_SPACE"
	conn = sqlite3.connect('users.db')
	c = conn.cursor()
	c.execute("DELETE FROM users WHERE username = '{}'".format(login))
	conn.commit()
	conn.close()
	conn = sqlite3.connect('users.db')
	c = conn.cursor()
	c.execute("INSERT INTO bannednames VALUES ('{}')".format(login))
	conn.commit()
	conn.close()
	return "OK"

def ListUsers():
	"""List all users."""
	conn = sqlite3.connect('users.db')
	c = conn.cursor()
	a = c.execute("SELECT * FROM users")
	for b in a:
		print("- "+b[0])
	conn.close()

def BanUser(login):
	"""Ban player from Elvex."""
	if not (IsUserExists(login)):
		print("Ban failed. User doesn't exists. ("+login+")", CT.ERROR)
		return "USER_GONE"
	if(username.isspace()):
		return "USER_SPACE"
	conn = sqlite3.connect('users.db')
	c = conn.cursor()
	c.execute("UPDATE users SET banned = true WHERE username = '{}'".format(login))
	conn.commit()
	conn.close()
	return "OK"

def UnbanUser(login):
	"""Pardon a player."""
	if not (IsUserExists(login)):
		print("Ban failed. User doesn't exists. ("+login+")", CT.ERROR)
		return "USER_GONE"
	if(username.isspace()):
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
	conn.commit()
	conn.close()
	print("Users were flushed.", CT.INFO)
	flushing = False

def GetUser(username, safe = True):
	"""Get user by name."""
	if not (IsUserExists(username)):
		print("Tried to get user, but user with that name doesn't exists. ("+username+")", CT.ERROR)
		return "USER_GONE"
	if(username.isspace()):
		return "USER_SPACE"
	conn = sqlite3.connect('users.db')
	c = conn.cursor()
	if(safe):
		a = c.execute("SELECT username, electricity,avatar, ppcount, inventory, customization, bio, stats, banned FROM users WHERE username = '{}'".format(username))
		a = a.fetchall()
	else:
		a = c.execute("SELECT username, passhash,avatar, electricity,ppcount, inventory, customization, bio, stats, banned, regip FROM users WHERE username = '{}'".format(username))
		a = a.fetchall()
	return json.dumps(a)

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
	if not (IsUserExists(username)):
		print("Tried to change user's password, but user with that name doesn't exists. ("+username+")", CT.ERROR)
		return "USER_GONE"
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
	if not (IsUserExists(username)):
		print("Tried to edit user, but user with that name doesn't exists. ("+username+")", CT.ERROR)
		return "USER_GONE"
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
	global debugger_mode
	global version
	if not debugger_mode:
		return "FAILED"
	print('Elvex SOCIAL v'+str(version))

# Checking dbs

if not (os.path.isfile("users.db")):
	conn = sqlite3.connect('users.db')
	c = conn.cursor()
	c.execute('''CREATE TABLE users
             (username text, passhash text, avatar int, electricity int, ppcount float, inventory text, customization text, bio text, stats text, banned boolean, regip text)''')
	c.execute('''CREATE TABLE bannednames
		(name text)''')
	conn.commit()
	conn.close()
	Logger("Created new user database, because users.db was missing.", CT.INFO)

if not (os.path.isfile("additional.db")):
	conn = sqlite3.connect('additional.db')
	c = conn.cursor()
	c.execute('''CREATE TABLE crates
             (item_code text, item_open_code text, items_in text)''')
	conn.commit()
	conn.close()
	Logger("Created new additionals database, because additional.db was missing.", CT.INFO)

if(platform.system() == "Windows"):
	subprocess.check_call(["attrib","+H","users.db"])
	subprocess.check_call(["attrib","+H","additional.db"])
if(len(sys.argv) > 1 and sys.argv[1] == "debugger"):
	Logger("Debugger initialized.", CT.WARN)
	debugger_mode = True
	while(True):
		oprint('> ',end='')
		a = input()
		try:
			eval(a)
		except Exception as e:
			print(str(e), CT.ERROR)
