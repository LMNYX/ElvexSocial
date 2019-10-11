import socket
import time
from Crypto.Cipher import AES
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Util.asn1 import DerSequence
# Test Client
from binascii import a2b_base64
key = RSA.importKey(open('public.pem').read())
cipher = PKCS1_OAEP.new(key)
serverAddressPort   = ("127.0.0.1", 60606)
bufferSize          = 1024
UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
while(True):
	print("> ",end='')
	a = cipher.encrypt(input().encode())
	bytesToSend = a
	UDPClientSocket.sendto(bytesToSend, serverAddressPort)
	msgFromServer = UDPClientSocket.recvfrom(bufferSize)
	msg = "[R]: {}".format(msgFromServer[0][:-1][2:])
	print(msg)
print(msg)
time.sleep(1000)