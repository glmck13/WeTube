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
tmpfile=tmp$$.mp4

dd ibs=1 skip=$skip if=$infile of=$outfile
truncate -s -$boundary $outfile

frame=${outfile%-*}-frame.jpg

valid=""
while true
do
	[ "$prefix" != "video" ] && break

	ffmpeg -i $outfile -vf scale=-2:300 -crf 20 $tmpfile 2>/dev/null || break
	rm -f $outfile; outfile=${outfile%.*}.mp4
	mv $tmpfile $outfile

	ffmpeg -ss 00:00:02 -i $outfile -frames:v 1 -vf scale=200:-1 ${frame} 2>/dev/null || break
	[ -s ${frame} ] || break

	valid="y"; break
done

rm -f $infile
if [ "$valid" ]; then
	while read line
	do
		[[ "$line" == \#* ]] && continue
		addr=${line#*:}
		sendaway.sh "$addr" "WeTube post from ${REMOTE_USER}!" "https://mckspot.net:8888/wetube.shtml"
	done <${HTML_ROOT}/etc/wetube.conf

	ls -l $id-*
else
	rm -f $id-*
	echo "Not valid"
fi
