#!/bin/bash

digit=${1:-0}
song=$(ls /var/lib/asterisk/sounds/songs/${digit}_* 2>/dev/null)
song=${song##*/} song=${song%.*}

echo "SET VARIABLE SONG_FILE ${song}"
