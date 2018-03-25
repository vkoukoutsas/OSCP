#!/usr/bin/python

import socket
import sys

def arguments():
	if len(sys.argv) != 2:
		print("Missing argument")
		print("Example: " + sys.argv[0] + " [host]")
		print("Usage: " + sys.argv[0] + " 10.0.0.1/example.com")
		exit()


def connect():
	sck = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	host = sys.argv[1]

	try:
		print("\nSending evil buffer")

		sck.connect((host, 110)) 			# connect to IP, POP#3 port
		data = sck.recv(1024)				# receive banner
		print(data)							# print banner

		sck.send("USER test\r\n")			# send username "test"
		data = sck.recv(1024)				# receive reply
		print(data)							# print reply

		sck.send("PASS test\r\n")			# send password "test"
		data = sck.recv(1024)				# receive reply
		print(data)							# print reply

		sck.close()							# close socket

		print("\nDone!")
	except Exception as e:
		print("Connection error: " + str(e))


def main():
	arguments()
	connect()

main()