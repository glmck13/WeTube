#!/bin/ksh

print "Content-Type: text/plain\n"

HTML_ROOT=${SCRIPT_FILENAME%${SCRIPT_NAME}}
cd ${HTML_ROOT}/cdn

RECENT=3600
now=$(date "+%s")
ls -1t *-frame.* 2>/dev/null | while read frame
do
	when=${frame} when=${when#*-} when=${when%-*}
	who=${frame} who=${who%%-*}
	let secs=$now-$when
	video=$(echo ${frame%-*}-video.*) video=${video% *}
	[ ! "$video" ] && continue
	if [ $secs -lt $RECENT ]; then
		style="style='background-color: gold; border-radius: 10px;'"
	else
		style="style='border-radius: 10px;'"
	fi
	print "<span class=\"card\">"
	print "<span class=\"content\">$who</span>"
	print "<img src=\"/cdn/$frame\" $style onclick='player.src = \"/cdn/$video\";' ondblclick='if (confirm(\"Delete video?\")) { delVideo(\"${video%-*}\"); };' />"
	print "</span>"
done
