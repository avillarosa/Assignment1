import socket
import sys

# Command line check
if len(sys.argv) < 2:
	print "USAGE python " + sys.argv[0] + " <PORT NUMBER>"
 
serverHost = '127.0.0.1'
serverPort = int(sys.argv[1])

# Create a TCP socket
serverSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
serverSock.bind((serverHost, serverPort))

# Start listening for incoming connections
serverSock.listen(1)

print serverHost

"""
print "Waiting for connections..."

serverConnection, addr = serverSock.accept()
print addr, " has connected to the server"

filename = raw_input("ftp> ")
file = open(filename, 'rb')
file_data = file.read(1024)
serverConnection.send(file_data)
print "Data has been transmitted successfully"

serverSock.close()
"""
def recvAll(sock, numBytes):

	# The buffer
	recvBuff = ""

	# Temporary buffer
	tmpBuff = ""

	# Keep receiving until all is received
	while len(recvBuff) < numBytes:

		# Attempt to receive bytes
		tmpBuff = sock.recv(numBytes)

		# The other side has closed the socket
		if not tmpBuff:
			break

		# Add the received bytes to the buffer
		recvBuff += tmpBuff

	return recvBuff

# Accept connections forever
while True:

	print "Waiting for connections..."

	# Accept connections
	clientSock, addr = serverSock.accept()

	print "Accepted connection from client: ", addr
	print "\n"
	
	# The buffer to all data received from the client.
	fileData = ""

	# The temporary buffer to store the received data.
	recvBuff = ""

	# The size of the incoming file
	fileSize = 0

	# Buffer containing the file size
	fileSizeBuff = ""

	# Receive the first 10 bytes indicating the size of the file
	fileSizeBuff = recvAll(clientSock, 10)

	# Get the file size
	fileSize = int(fileSizeBuff)
	print "FILE SIZE: ", fileSize

	# Get the file data
	fileData = recvAll(clientSock, fileSize)

	print "FILE DATA: ", fileData
		
	# Close client socket
	clientSock.close()
