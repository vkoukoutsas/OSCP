#!/bin/bash

for ip in $(cat list.txt); do
	host=$(host $ip.$1 | grep "has address" | grep -v "92.242.140.20")

	if [[ $host != "" ]]; then
		echo $host
	fi
done