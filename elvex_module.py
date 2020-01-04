print("Loading libraries...")
import time
import os
import socket
import threading
from threading import Thread
import sys

OLD_PRINT = print

if not os.path.exists(".logs"):
	os.mkdir(".logs")

# PRINT OVERWRITTEN
def print(msg, isLogger = True, newline=True):
	if(newline):
		msg =  msg + "\n" if newline else msg
	sys.stdout.write(msg)
	return

class Social(object):
	class Method(object):
		def __init__(self, call_name, description, callback, isAuthNeeded = False):
			self.call_name = call_name
			self.description = description
			self.auth = isAuthNeeded
			self.callback = callback
		def RunCallback(self, **args):
			self.callback(**args)

soc = Social()

print("Everything is ready to start the server...")