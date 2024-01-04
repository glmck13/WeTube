#!/bin/ksh

PATH=$PATH:/var/www/.local/bin

for x in ${QUERY_STRING//\&/ }
do
	key=${x%%=*} val=${x#*=}
	val=$(urlencode -d "$val" | sed -e 's/\$/\\\\\\&/g')
	eval $key=\"$val\"
done

cd $DOCUMENT_ROOT/cdn

start=${exten#???} exten=${exten%$start}
POSITION=$PWD/${exten}.secs
if [ "$start" ]; then
	:
elif [ -f "$POSITION" ]; then
	start=$(<$POSITION)
else
	start=0
fi
let end=$start+3600
secs=$(date "+%s")
trap 'let start=${start}+$(date +"%s")-${secs}; echo ${start} >$POSITION' HUP INT TERM EXIT

grep "^$exten|" pbx.conf | IFS='|' read x media addr desc
[ ! "$media" ] && media="file" addr="misc/nothing-en.mp3"

print "Content-Type: audio/mpeg\n"

if [ "$media" = "file" ]; then
	cat "$addr"
elif [ "$media" = "youtube" ]; then
	yt-dlp -o - -x "$addr" --download-sections "*${start}-${end}" 2>/dev/null | ffmpeg -i - -f mp3 -ar 16K - 2>/dev/null
fi
