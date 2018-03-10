#!/bin/bash

# $1 host IP -> 192.168.0
# $2 host name -> example.com

for ip in $(seq 1 254); do
	host=$(host $1.$ip | grep -v "not found" | grep "$2")

	if [[ $host != "" ]]; then
		echo $host
	fi
done