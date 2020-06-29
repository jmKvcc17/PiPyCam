#!/bin/bash

# const. vars
motionPicDir="/var/lib/motion"
install_path="/home/pi/Documents/PiCamPython/src"

# function defs.

# clear the log file
function clearLog() {
    
    echo "Clearing log..."

    # cd logs/

    echo -n | tee  logs/debug.log logs/info.log logs/warn.log

    # cd ..
}

# delete all jpg and avi files in motion pic dir
function deletePics() {

    echo "Deleting local pictures..."    

    # cd $motionPicDir

    sudo find $motionPicDir -name "*.jpg" -print0 | xargs -0 rm

    # cd $install_path
}

# stop the motion daemon by getting the pid of 
# the service with ps aux, pipe it into grep
# to search for the 'motion' line, then get 
# the pid from the second column
function stopMotion() {
    sudo kill $(ps aux | grep 'motion' | awk '{print $2}')
}

function stopPython() {
    sudo kill $(ps aux | grep 'quickstart.py' | awk '{print $2}')
}

function startMotion() {

    echo "Starting..." 

    sudo motion
    
    python3 src/quickstart.py &
}

function listDirSize() {
    dirSize=$(du -h $motionPicDir | awk ' { print $1 } ')
    filesInDir=$(ls -lq $motionPicDir | wc -l)

    echo "$motionPicDir is $dirSize"
    echo "$motionPicDir has $filesInDir file(s)"
}

# Displays the main menu
function menu() {

    select userSelect in "Start" "Stop" "List Pic Dir. Size" "Delete Pictures" "Clear Log" "Exit"
    do
       case "$userSelect" in
           "Start")
               startMotion
               ;;
           "Stop")
               echo "Stopping..."
               stopMotion
               stopPython
               ;;
           "List Pic Dir. Size")
               listDirSize
               ;;
           "Delete Pictures")
               
               deletePics
               ;;
           "Clear Log")
                
               clearLog
               ;;
           "Exit")
               exit
               ;;

       esac
   done
}

# main function
function main() {
    menu     
}

main


