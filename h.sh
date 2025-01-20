#!/bin/bash

for(( i =0; i<100000; i++ ))do

	username="user$i"
	sudo userdel "user$i"
	rm -rf /home/${username}
done;
