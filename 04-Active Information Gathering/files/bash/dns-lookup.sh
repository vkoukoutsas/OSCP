#!/bin/bash

for ip in $(cat list.txt); do
	echo $(host $ip.$1 | grep "has address")
done