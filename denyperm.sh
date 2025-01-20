#!/bin/bash

for(( i="$1";i<="$2";i++ ))
do
	username="user$i"
	setfacl -b /home/examination/$username
done
