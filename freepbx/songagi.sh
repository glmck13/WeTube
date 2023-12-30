#!/bin/bash

digit=${1:-0} dir=${2:-0}
song=$(ls /var/lib/asterisk/sounds/${dir}/${digit}[_-]* 2>/dev/null)
song=${song##*/sounds/} song=${song%.*}

[ "$song" ] && echo "SET VARIABLE SONG_FILE ${song}"
