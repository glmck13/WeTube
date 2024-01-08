#!/bin/ksh

URLBASE="https://mckspot.net:8443"
VARBASE="/var/www/html"
M3UFILE="./cdn/misc/scripture.m3u"

typeset -l today
today=$(date +"%B-%e-%Y")
today=${today// /}
today="https://soundcloud.com/usccb-readings/daily-mass-reading-podcast-for-$today"

url=$(curl -s "$today" | grep '<script>' | tr ',' '\n' | grep '^"media":')
url=${url#*:} url=${url#*:} url=${url#*:}
url=$(curl -s ${url//\"/}?client_id=)
url=${url#*:} url=${url%*?}

curl -s ${url//\"/} >$VARBASE/$M3UFILE

cat - <<EOF
Content-Tye: application/json

{"speech" : "Downloading $(date +'%B %d')", "audio" : "$URLBASE/$M3UFILE"}
EOF
