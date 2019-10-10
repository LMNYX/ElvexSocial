import time
import socket
serverAddressPort = ("127.0.0.1", 60606)
bufferSize          = 1024

cl = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

print("input: ", end='')
i = str.encode(input())
cl.sendto(i, serverAddressPort)
msgFromServer = cl.recvfrom(bufferSize)
msgFromServer = str(msgFromServer[0])[2:][:-1]
msg = "Message from Server {}".format(msgFromServer)
print(msg)