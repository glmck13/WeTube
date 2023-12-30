#!/bin/ksh

PATH=$PATH:/var/www/.local/bin

print "Content-Type: audio/mpeg\n"
yt-dlp -o - -x "https://www.youtube.com/watch?v=E3NOvf9WNAQ" 2>/dev/null | ffmpeg -i - -f mp3 -filter:a "volume=2.0" -ar 16000 - 2>/dev/null
