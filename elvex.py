from elvex_module import *

sock = socket.socket()
sock.bind(('', 6868))
print("Server started on port 6868. Waiting for connections!")

# Message parser (Client => Server => Client)
def ContentDelivery():
	global conn
	global addr
	global sock
	sock.listen(1)
	conn, addr = sock.accept()
	while True:
		data = conn.recv(1024)
		if not data:
			break
		conn.send(data.upper())

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
	# Exiting the app
	os._exit(0)