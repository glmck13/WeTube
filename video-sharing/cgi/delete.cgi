#!/bin/ksh

print "Content-Type: text/plain\n"

HTML_ROOT=${SCRIPT_FILENAME%${SCRIPT_NAME}}
cd ${HTML_ROOT}/cdn

eval "$QUERY_STRING"
rm -f ${video}-*.*

print ${video}
