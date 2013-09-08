import SocketServer
import os
from RF_IO_Queue import *

class UDPHandler(SocketServer.BaseRequestHandler):
	io_queue = RF_IO_Queue()

	def handle(self):
	        data = self.request[0].strip()
		socket = self.request[1]
        	#print "{} wrote:".format(self.client_address[0])
		#print data
		self.io_queue.put(data)		

def start_server(server_ip, server_port):
    	HOST, PORT = server_ip, int(server_port)
	server = SocketServer.UDPServer((HOST, PORT), UDPHandler)
        server.serve_forever()

