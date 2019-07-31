# Ben Ryan 
# Client-side

# Summary of operation:
# Connects to server
# Displays messages received from server

import socket as sock
import ssl

HOST='localhost'
PORT=5000
CERT='./server.crt'

context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
context.load_verify_locations(CERT)

unsecureSocket = sock.socket(sock.AF_INET, sock.SOCK_STREAM)
secureSocket = context.wrap_socket(unsecureSocket, server_hostname='Ben')
secureSocket.connect((HOST, PORT))

print("Connected, waiting for message.")
while secureSocket:
	data = b''
	while b'END' not in data:
		data += secureSocket.recv(32)

	msg =  data[:len(data)-len('END')].decode('utf-8')
	print("Message Received:", msg)

	secureSocket.sendall("Received".encode('utf-8')+b'END')
