import socket
import os
import sys
import commands

# Command line checks
if len(sys.argv) < 3:
	print "USAGE python " + sys.argv[0] + " <SERVER MACHINE>" + " <SERVER PORT>"

serverHost = sys.argv[1]
serverPort = int(sys.argv[2])

# Server Welcome
print "======================================================================="
print "Welcome to the FTP server"
print "Commands are \'get <FILENAME>\' to download a file, \'put <FILENAME>\'"
print "\'ls\' to list the files in the directory, and \'quit\' to exit"
print "=======================================================================" 
# Getting user input
userInput = raw_input("ftp> ")

# Parsing user input where parseUserInput[0] is the command
# and parseUserInput[1] is the file name
parseUserInput = userInput.split()
userCommand = parseUserInput[0]
if len(parseUserInput) == 2:
	fileName = parseUserInput[1]

# Create a TCP socket
connectionSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
connectionSock.connect((serverHost, serverPort))

while userCommand != "quit":
	if userCommand == "put":

		connectionSock.send("put")
		# Open the file
		fileObj = open(fileName, "r")

		# Number of bytes sent
		numSent = 0

		# File data
		fileData = None

		# Keep sending until all is sent
		while True:

			# Read 65536 bytes of data
			fileData = fileObj.read(65536)

			# Make sure did not hit EOF
			if fileData:

				# Get the size of the data read and convert to string
				dataSizeStr = str(len(fileData))

				# Prepend 0's to the size string until the size is 10 bytes
				while len(dataSizeStr) < 10:
					dataSizeStr = "0" + dataSizeStr

				# Prepend the size of the data to the file data
				fileData = dataSizeStr + fileData

				# Number of bytes sent
				numSent = 0

				# Sending data
				while len(fileData) > numSent:
					numSent += connectionSock.send(fileData[numSent:])

			# The file has been read
			else:
				break

		print "Sent ", numSent, " bytes."

		# Close the socket and the file
		connectionSock.close()
		fileObj.close()

	elif userCommand == "get":
		"""	
		connectionSock.send(str(fileName))
		data = connectionSock.recv(1024)
		fileSize = long(data[6:])
		f = open("new_"+fileName, "wb")
		data = connectionSock.recv(1024)
		totalRecv = len(data)
		f.write(data)
		while totalRecv < fileSize:
			data = connectionSock.recv(1024)
			totalRecv += len(data)
			f.write(data)
		connectionSock.close()
		print "Download Complete!"
		"""
	elif userCommand == "ls":
		for line in commands.getstatusoutput('ls -l'):
			print line
	else:
		print "\nWrong command. Please enter \'get <FILENAME>\', \'put <FILENAME>\', \'ls\', or \'quit\'\n"

	# Getting user input
	userInput = raw_input("ftp> ")

	# Parsing user input where parseUserInput[0] is the command
	# and parseUserInput[1] is the file name
	parseUserInput = userInput.split()
	userCommand = parseUserInput[0]
	if len(parseUserInput) == 2:
		fileName = parseUserInput[1]

print "Exited FTP server"
