#!/bin/bash
start="$1"
end="$2"
for (( i="$1" ; i<"$2" ; i++ ))
do
	user_name="user$i"
	echo "${user_name} unlocked"
	passwd -u $user_name
done

