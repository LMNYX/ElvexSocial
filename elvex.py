from elvex_module import *

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((server_settings.SERVER_IP, server_settings.SERVER_PORT))
print("Server \""+server_settings.SERVER_NAME+"\" started on port "+str(server_settings.SERVER_PORT)+". Waiting for connections!")

# Message parser (Client => Server => Client)
ClientThreads = {}
def ContentDelivery_UserThread(conn, clientid, addr):
	try:
		while True:
			data = conn.recv(1024)
			data = data.decode()
			if not data:
				break
			if not is_json(data):
				conn.sendall(errs.Drop("REQUIRED_JSON_REQUEST", clientData=data, clientIP = addr).encode())
				continue
			data = json.loads(data)
			if('method' not in data):
				conn.sendall(errs.Drop("PROVIDE_METHOD", clientData=data, clientIP = addr).encode())
				continue
			if('args' not in data):
				conn.sendall(errs.Drop("PROVIDE_ARGS", clientData=data, clientIP = addr).encode())
				continue

			if(data['method'] in soc.methods):
				res = soc.methods[data['method']].RunCallback(**data['args'])
				conn.sendall(res.encode())
			else:
				conn.sendall(errs.Drop("INTERNAL_ERROR", clientData = data, clientIP = addr).encode())
		print('[-] Client disconnected (%s)' % addr)
		conn.close()
	except ConnectionResetError:
		print('[-] Client disconnected (%s)' % addr)
		conn.close()
	except Exception as e:
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
					"value": "Nothing more."
					}
				]
				}])
def ContentDelivery():
	global ClientThreads
	global conn
	global addr
	global sock
	currthreadnum = 0
	try:
		sock.listen(1)
		while True:
			conn, addr = sock.accept()
			print('[+] Connection found with '+str(addr[0]))
			ClientThreads[str(currthreadnum)] = Thread(target=ContentDelivery_UserThread, args=(conn,currthreadnum+1, addr[0],))
			ClientThreads[str(currthreadnum)].start()
			currthreadnum+=1
	except socket.error as e:
		if(e.errno == errno.ECONNRESET):
			pass
		else:
			WebhookSend(server_settings.DISCORD_WEBHOOK, "", "ElvexSocial", [{
				"content": "@everyone Something wrong in sockets!\nPlease check.",
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
					"value": "Nothing more."
					}
				]
				}])
			pass

# Threading
try:
	# Creating threads
	ContentDeliveryThread = Thread(target=ContentDelivery)
	# Starting them
	ContentDeliveryThread.start()
	# Joining them
	ContentDeliveryThread.join()
except (KeyboardInterrupt, SystemExit): # KeyboardInterrupt and SystemExit
	sock.close()
	print("Server closed.")
	# Exiting the app
	os._exit(0)