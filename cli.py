"""
Names: Adam Villarosa
Email: aville@csu.fullerton.edu
Class: CPSC 471-02
Language: Python 2.7
Programming Assignment 1
"""
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
#connectionSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
#connectionSock.connect((serverHost, serverPort))

while userCommand != "quit":
	
	connectionSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	connectionSock.connect((serverHost, serverPort))
	
	# 'put' command from Assignment1SampleCodes/Python/sendfile/sendfileserv.py
	if userCommand == "put":
		
		# Sending user command 'put'
		connectionSock.send(userCommand)
		
		# Open the file
		fileObj = open(fileName, "r")

		# Number of bytes sent
		numBytes = 0

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
				numbytes = 0

				# Sending data
				while len(fileData) > numBytes:
					numBytes += connectionSock.send(fileData[numBytes:])

			# The file has been read
			else:
				break

		print "UPLOADED FILE: ", fileName
		print "NUMBER OF BYTES:", numBytes

		# Close the socket and the file
		connectionSock.close()
		fileObj.close()
	
	# 'get' downloads a file from the server
	elif userCommand == "get":
		
		# Sending user command 'get'
		connectionSock.send(userCommand)

		# Sending file name
		connectionSock.send(fileName)
		
		# Number of bytes
		numBytes = 0
		
		# Opening file, receiving, and writing data
		with open('receieved_'+fileName, 'wb') as f:
			while True:
				data = connectionSock.recv(1024)
				f.write(data)
				numBytes += len(data)
				if not data:
					break
		
		print "DOWNLOADED FILE: ", f,  "."
		print "NUMBER OF BYTES:", numBytes
		
		# Closing file and socket
		f.close()
		connectionSock.close() 
	
	# Prints the directory using ls from the server
	elif userCommand == "ls":
		
		connectionSock.send(userCommand)
		print connectionSock.recv(1024)
		
		# Closing socket
		connectionSock.close()
	
	else:
		print "\nWrong command. Please enter \'get <FILENAME>\', \'put <FILENAME>\', \'ls\', or \'quit\'\n"

	# Getting user input
	userInput = raw_input("ftp> ")

	# Parsing user input where parseUserInput[0] is the command
	# and parseUserInput[1] is the file name
	parseUserInput = userInput.split()
	userCommand = parseUserInput[0]
	if len(parseUserInput) == 2:
		fileName = str(parseUserInput[1])

print "Exited FTP server"
