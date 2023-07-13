#!/bin/ksh

print "Content-Type: text/plain\n"

id=${REMOTE_USER:-nobody}-$(date "+%s")

HTML_ROOT=${SCRIPT_FILENAME%${SCRIPT_NAME}}
cd ${HTML_ROOT}/cdn

infile=$id.bin
cat - >$infile

prefix="none"
suffix="raw"
boundary=0
skip=0
while read line
do
	line=${line%?} # strip \r
	[ "$boundary" -eq 0 ] && let boundary=${#line}+2+2+2 # account for preceding/ending \r\n and -- characters in final
	let skip+=${#line}+2
	if [[ $line == Content-Type:* ]]; then
		prefix=${line} prefix=${prefix#* } prefix=${prefix%/*}
		suffix=${line} suffix=${suffix#*/} suffix=${suffix%;*}
		[ "$suffix" = "x-matroska" -o "$suffix" = "octet-stream" ] && suffix="webm"
	elif [ ! "$line" ]; then
		break
	fi
done <$infile
outfile="${infile%.*}-$prefix.$suffix"

dd ibs=1 skip=$skip if=$infile of=$outfile
truncate -s -$boundary $outfile

if [ "$prefix" = "video" ]; then
	ffmpeg -ss 00:00:01 -i $outfile -frames:v 1 -vf scale=200:-1 ${outfile%-*}-frame.jpg 2>/dev/null
	if [ "$suffix" != "mp4" ]; then
		ffmpeg -i $outfile ${outfile%.*}.mp4 2>/dev/null
		rm -f $outfile
		outfile=${outfile%.*}.mp4
	fi
fi

while read line
do
	[[ "$line" == \#* ]] && continue
	addr=${line#*:}
	sendaway.sh "$addr" "WeTube post from ${REMOTE_USER}!" "https://mckspot.net:8888/cdn/$outfile"
done <${HTML_ROOT}/etc/wetube.conf

rm -f $infile

ls -l $id-*
