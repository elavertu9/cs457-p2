#!/bin/bash

if [[ $# == 0 || $# > 1 ]]; then
	echo "Usage: ./transfer.sh <cs username>"
else
	scp * $1@denver.cs.colostate.edu:~$1
fi
