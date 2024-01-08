#!/bin/ksh

PATH=$PATH:$DOCUMENT_ROOT/cgi

M3UFILE="$DOCUMENT_ROOT/cdn/misc/scripture.m3u"

scripture.cgi >/dev/null

print "Content-Type: audio/mpeg\n"
ffmpeg -protocol_whitelist file,http,https,tcp,tls -i $M3UFILE -f mp3 -filter:a "volume=2.0" -ar 48000 - 
