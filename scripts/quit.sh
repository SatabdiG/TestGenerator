#!/bin/bash
#This script will kill a particular process by name expression

if [ $# -lt 1 ]; then
	echo "Process name missing !!"
	exit 1
else	
	# List all the process ID in a line
	list=($(ps aux | awk '{if((index($4,"'$1'")>0) && ($1!="PID")) {print $1}}'))
    echo $1
	echo "Process count: "${#list[*]}
	max=${#list[*]}

	# If no process found exit
	if [ ${#list[*]} -eq 0 ]
	then
		echo "No process found of this name."		
		exit 0
	fi

	# Loop through all the process and kill one by one
	for ((i=0; i<$max; ++i )); 
	do
		echo "Killing process..."${list[$i]}
		kill -9 ${list[$i]}    		
	done

	#Final Message
	if [ $? -eq 0 ]; then
		echo "All process killed sucessfully."
	else
		echo "Proess killed ..."
	fi

fi