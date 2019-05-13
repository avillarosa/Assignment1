import socket
import os
import sys
import commands

# Command line checks
if len(sys.argv) < 3:
	print "USAGE python " + sys.argv[0] + " <SERVER MACHINE>" + " <SERVER PORT>"

serverHost = sys.argv[1]
serverPort = int(sys.argv[2])

# Name of the file
#fileName = raw_input("ftp> PUT ")

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

if userCommand == "put":

	# Create a TCP socket
	#connectionSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	# Connect to the server
	#connectionSock.connect((serverHost, serverPort))

	# Open the file
	fileObj = open(fileName, "r")

	# Number of bytes sent
	numSent = 0

	# File data
	fileData = None

	# Keep sending until all is sent
	while True:

		# Read 64436 bytes of data
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

elif userCommand == "ls":
	for line in commands.getstatusoutput('ls -l'):
		print line

else:
	print "wrong input"

print "Exited FTP server"
