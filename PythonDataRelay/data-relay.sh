#!/bin/bash

ADDRESS=`grep server_address relay.conf | cut -d "=" -f 2`
TERMTYPE=`grep terminal_type relay.conf | cut -d "=" -f 2`

echo "$ADDRESS $TERMTYPE"

firefox -new-window "$ADDRESS:8000/restaurant/$TERMTYPE" &

python3 arduino-communicator.py
