from elvex_module import *

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((server_settings.SERVER_IP, server_settings.SERVER_PORT))
print("Server \""+server_settings.SERVER_NAME+"\" started on port "+str(server_settings.SERVER_PORT)+". Waiting for connections!")


def ContentDelivery():
	global conn
	global addr
	global sock
	currthreadnum = 0
	try:
		sock.listen(1)
		while True:
			conn, addr = sock.accept()
			_n = cc.AddClient(conn,addr)
			tryt = cc.GetClient(_n).StartThread()
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