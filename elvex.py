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
if(platform.system() == "Windows"):
	import subprocess


oprint = print
ohelp = help

def help():
	return

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
	return str.encode(stri)

def eprint(t):
	sys.stdout.write(t+'\n')

def Logger(stri,type = CT.NONE):
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
  try:
    json_object = json.loads(myjson)
  except ValueError as e:
    return False
  return True

def LogPrint(stri,type = CT.NONE):
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
	def __init__(self,msg,typeo = CT.NONE):
		LogPrint(msg,typeo)

def IsUserExists(login):
	conn = sqlite3.connect('users.db')
	c = conn.cursor()
	r = c.execute("SELECT * FROM users WHERE username = '{}'".format(login))
	if(r.fetchone()):
		return True
	else:
		return False

def EStr(stre):
	a = hmac.new(b'_EaLEoELXoELWoXLOWQlWA_1+-2#)LC<E!!!(!0CC@@@@A', stre.encode(), hashlib.sha256)
	return str(a.hexdigest())

def AddUser(login, pswd, avatar = 0, electricity = 0, ppcount = 0.0, inventory = "[]", customization = '{"droidColor": "blue", "lampColor": "blue","hat": "none", "body": "none", "hands": "none", "legs": "none"}', bio = "Not specified.", stats = "{}", banned = False, regip = "0.0.0.0"):
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

def BanUser(login):
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

def ChangeUserStat(username,stat,to):
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

if not (os.path.isfile("matches.db")):
	conn = sqlite3.connect('matches.db')
	c = conn.cursor()
	c.execute('''CREATE TABLE matches
             (creator text, actions text, party string, perfomance string, teamstats text)''')
	conn.commit()
	conn.close()
	Logger("Created new match database, because matches.db was missing.", CT.INFO)

if(platform.system() == "Windows"):
	subprocess.check_call(["attrib","+H","users.db"])
	subprocess.check_call(["attrib","+H","matches.db"])
if(len(sys.argv) > 1 and sys.argv[1] == "debugger"):
	while(True):
		oprint('> ',end='')
		a = input()
		try:
			eval(a)
		except Exception as e:
			print(str(e), CT.ERROR)
