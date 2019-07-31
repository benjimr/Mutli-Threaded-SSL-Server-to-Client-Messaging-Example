# Ben Ryan 
# Server-side

# Summary of operation:
# Listener thread accepts connections and spawns Handler threads for each new connection
# Handler thread waits for a message to appear in its queue, then sends the message to its client
# The main thread handles input from the user. 
# The user will input messages, which the handler threads will send to the clients

from collections import deque
import socket as sock
import ssl
from threading import Thread
import threading
import time

HOST='localhost'
PORT=5000
CERT='./server.crt'
KEY='./server.key'

class Listener(Thread):
	def __init__(self, addr):
		Thread.__init__(self)
		context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
		context.load_cert_chain(certfile=CERT, keyfile=KEY)

		unsecureSocket = sock.socket(sock.AF_INET, sock.SOCK_STREAM)
		unsecureSocket.bind(addr)
		unsecureSocket.listen()

		self.secureSocket = context.wrap_socket(unsecureSocket, server_side=True)

	def run(self):
		while True:
			conn, addr = self.secureSocket.accept()
			print("\n\nNew connection to", addr)
			handler = Handler(conn, addr)
			handler.setDaemon(True)
			handler.start()

class Handler(Thread):
	def __init__(self, socket, addr):
		Thread.__init__(self)
		self.socket = socket
		self.addr = addr
		self.msg = deque()

	def run(self):
		while self.socket:
			while len(self.msg) == 0 : time.sleep(0.1)

			self.socket.sendall(self.msg.pop())

			data = b''
			while b'END' not in data:
				data += self.socket.recv(32)

			msg = data[:len(data)-len('END')].decode('utf-8')

			if msg != "Received":
				print("Error on connection", self.addr)

if __name__ == '__main__':
	listener = Listener((HOST, PORT))
	listener.setDaemon(True)
	listener.start()

	print("Waiting for clients to connect...\n\n")
	while True:
		while threading.activeCount() <= 2: time.sleep(0.1)
		msg = input("\n\nInput a message to send to all clients: ").encode('utf-8')+b'END'

		currentThread = threading.currentThread()
		for thread in threading.enumerate():
			if thread is not currentThread and thread is not listener:
				thread.msg.append(msg)

