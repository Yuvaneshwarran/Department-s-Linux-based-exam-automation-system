#!/bin/bash

LAST_USER_FILE="last_user.txt"
LOGIN_FILE="login.txt"
LOG_FILE="user_creation.log"

# Logging function
log() {
    echo "$(date +"%Y-%m-%d %H:%M:%S") - $1" >> "$LOG_FILE"
}

log "Starting the script"

if [[ "${UID}" -ne 0 ]]; then 
    log "Script should be run as root or with sudo"
    echo "Please run this script with sudo or as root."
    exit 1
fi

if [[ "${#}" -lt 1 ]]; then 
    log "Insufficient number of arguments"
    echo "Usage: $0 <number_of_users>"
    exit 1
fi

num_users="${1}"

if ! [[ "${num_users}" =~ ^[0-9]+$ ]]; then
    log "Invalid argument: ${num_users}. Please provide a valid number."
    echo "Invalid argument: ${num_users}. Please provide a valid number."
    exit 1
fi

if [[ -f "$LAST_USER_FILE" ]]; then
    last_user=$(cat "$LAST_USER_FILE")
else
    last_user=0
fi

start_index=$((last_user + 1))
end_index=$((last_user + num_users ))

> "$LOGIN_FILE"

log "Creating $num_users users starting from user${start_index} to user${end_index}"

for (( i=start_index; i<=end_index; i++ ))
do
    User_name="user${i}"
    Password=$(openssl rand -base64 5)

    useradd -m "$User_name"

    if [[ $? -ne 0 ]]; then 
        log "Failed to create account for '$User_name'" 
        echo "The account for '$User_name' could not be created" 
    else
        echo "${User_name},${Password}" >> "$LOGIN_FILE"
        echo "${User_name}:${Password}" | chpasswd 

        if [[ $? -ne 0 ]]; then 
            log "Failed to set password for '$User_name'" 
            echo "The password for '$User_name' could not be set" 
        else
            log "User '$User_name' created successfully with password: $Password"
        fi
    fi
done

echo "${User_name}  ${Password}"
log "End of script execution. Last user index: $end_index"

echo "$end_index" > "$LAST_USER_FILE"
