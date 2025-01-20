#!/bin/bash

t_id="$1"

#start="$2"
#end="$3"

for(( i="$2";i<"$3";i++ ))
do
	username="user$i"
	echo "$t_id teacherid"
	setfacl -R -m u:$t_id:rwx /home/examination/$username
	getfacl "/home/examination/$username"
done
