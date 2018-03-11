#!/usr/bin/python

import socket
import sys

if len(sys.argv) != 2:
	print "Usage: " + sys.argv[0] + " [host]"
	sys.exit(0)

# args
host = sys.argv[1]

# Read usernames from usernames file
usernames = file("usernames.txt").readlines()

# VRFY a user
for username in usernames:
	# Create a Socket
	sck = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	# Connect to the Server
	sck.connect((host, 25))

	# Receive the banner
	print(sck.recv(1024))

	print("VRFY " + username)

	# Send user name
	sck.send("VRFY " + username + " \r\n")

	# Print result
	print(sck.recv(1024))

	# Close socket connection
	sck.close()