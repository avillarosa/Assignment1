import socket
import sys

# Command line check
if len(sys.argv) < 2:
	print "USAGE python " + sys.argv[0] + " <PORT NUMBER>"
 
# The server host
serverHost = '127.0.0.1'

# Port number from first argument in command line
serverPort = int(sys.argv[1])

# Create a TCP socket
serverSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
serverSock.bind((serverHost, serverPort))

# Listen for incoming connections
serverSock.listen(2)

print serverHost

def recvAll(sock, numBytes):

	# Buffer
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

def sendAll(sock, numBytes):
	
	# Buffer
	sendBuff = ""

	# Temporary buffer
	tmpBuff = ""

	# Keep sending until all is sent
	while len(sendBuff) < numBytes:
		tmpBuff = sock.send(numBytes)	

		# The other side has closed the socket
		if not tmpBuff:
			break

		# Add the sent bytes to the buffer
		sendBuff += tmpBuff

	return sendBuff

# Accept connection forever
while True:

	print "Waiting for connections..."

	# Accept connections
	clientSock, addr = serverSock.accept()

	print "Accepted connection from client: ", addr
	
	userResponse = clientSock.recv(1024)
	if userResponse == "put":
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
		clientSock.close()

	elif userResponse == "get":
		fileData = ""
		sendBuff = ""
		fileSize = 0
		fileSizeBuff = ""
		fileSizeBuff = sendAll(clientSock, 10)
		fileSize = int(fileSizeBuff)
		fileData = sendAll(clientSock, fileSize)
		clientSock.close()
