print("Loading libraries...")
import server_settings
import time
import os
import socket
import threading
from threading import Thread
import sys
import requests
import json
import errno
import pprint


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
def print(msg, isLogger = True, newline=True):
	if(newline):
		msg =  msg + "\n" if newline else msg
	sys.stdout.write(msg)
	return

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
				"PROVIDE_METHOD": {"error": "PROVIDE_METHOD", "human_readable": "Request sent to server doesn't have method."}
			}
		def Drop(self, errname, selfDrop = False, clientData = {}, clientIP = ""):
			if(errname not in self.Errors):
				print("Hit Internal Error!")
				self.Drop("INTERNAL_ERROR", True)
				return False
			AddInfo = ""
			if(selfDrop): AddInfo += "This is **self-drop**!\n"
			if(not clientData == {} and not clientIP == ""): AddInfo += "Client IP: `{0}`\nClient Request:\n```json\n{1}\n```\n".format(clientIP, clientData)
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

class MethodCallbacks(object):
	def __init__(self):
		return
	def ListMethods(self):
		global soc
		print("Is it going thru?")
		res = {}
		for m in soc.methods:
			res[m] = soc.methods[m].description
		return json.dumps({"response": "OK" , "methods": res})

mc = MethodCallbacks()
soc = Social()
errs = Social.Errors()

#######################
# Registering methods
soc.Method("dev.listmethods", "", mc.ListMethods)

print("Everything is ready to start the server...")