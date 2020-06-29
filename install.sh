#!/bin/bash

function createConfig() {
    # touch /etc/PiPyCam.json

    # Get the folder id email
    echo 'Please enter the folder id for the Google Driver folder: '
    read folder_id

    # Get the email
    echo 'Please enter your email:'
    read email
    
    if [ -n "$folder_id" ] ; then

        if [ -n "$email" ] ; then

            touch /etc/PiPyCam.json

            echo '{"FOLDER_ID": "'${folder_id}'", "EMAIL": "'${email}'"}' > /etc/PiPyCam.json
            echo 'PiPyCam.json created in /etc/. You can edit the email and folder id if needed.'

            return 1
        fi
    fi

    echo 'Error: folder id and email not entered, config folder not created.'
}

function createLogs() {
    dir_path='/var/log/PiPyCam'

    mkdir $dir_path
    chown pi:pi $dir_path
}

function runSetup() {
    echo 'Running setup.py, a browser should open...'
    python3 src/resources/setup.py
}

function installPipPkgs() {
    echo 'Installing Pip packages...'
    pip3 install -r requirements.txt
}

function main() {

    #createConfig
    createLogs
    #installPipPkgs
    #runSetup
}

if [ "$EUID" -ne 0 ]
    then echo "Please run as root."
    exit
fi


read -p "Do you wish to install this program? (y/n): " yn
case $yn in
    [Yy]* ) main break;;
    [Nn]* ) exit;;
esac



