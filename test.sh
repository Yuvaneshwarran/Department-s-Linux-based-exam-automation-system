#!/bin/bash

LAST_USER_FILE="last_user.txt"
LOGIN_FILE="login.txt"
echo "starting of the file"
if [[ "${UID}" -ne 0 ]]; then 
    echo "It is not a sudo user or root"
    echo "Run with sudo user or root"
    exit 1
fi

if [[ "${#}" -lt 1 ]]; then 
    echo "Insufficient number of arguments"
    echo "Usage: $0 <number_of_users>"
    exit 1
fi
echo "after checking arguments"
num_users="${1}"

if ! [[ "${num_users}" =~ ^[0-9]+$ ]]; then
    echo "Invalid argument: ${num_users}. Please provide a valid number."
    exit 1
fi

if [[ -f "$LAST_USER_FILE" ]]; then
    last_user=$(cat "$LAST_USER_FILE")
else
    last_user=0
fi

echo "after providing last user"

start_index=$((last_user + 1))
end_index=$((last_user + num_users ))

# Truncate the login file
> "$LOGIN_FILE"
echo "before for loop"
for (( i=start_index; i<=end_index; i++ ))
do
    User_name="user${i}"
    Password=$(openssl rand -base64 5)

    useradd -m "$User_name"

    if [[ $? -ne 0 ]]; then 
        echo "The account for '$User_name' could not be created" 
    else
        echo "${User_name},${Password}" >> "$LOGIN_FILE"
        echo "${User_name}:${Password}" | chpasswd 

        if [[ $? -ne 0 ]]; then 
            echo "The password for '$User_name' could not be set" 
        fi
    fi
done
echo "${User_name}  ${Password}"
echo "the end index is $end_index"

# Save the last user number for next execution
echo "$end_index" > "$LAST_USER_FILE"

