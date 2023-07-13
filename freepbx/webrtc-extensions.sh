#!/bin/ksh

ext=${1:?Enter starting extension}
count=${2:?Enter number of extensions}
offset=${3:?Enter offset}

cat - <<EOF
[from-internal-custom]
exten => _**44XX.,1,Noop(Entering user defined context from-internal-custom in extensions_custom.conf)
exten => _**44XX.,n,AGI(agi://asterisk.local/polly.sh)
exten => _**44XX.,n,Dial(Local/\${EXTEN:4}@from-internal)
exten => _**44XX.,n,Hangup

exten => 411,1,Answer()
exten => 411,n,MP3Player(http://piville.home/public/dmr.cgi)
exten => 411,n,Hangup()

EOF

while [ "$count" -gt 0 ]
do
cat - <<EOF
exten => ${ext},1,Noop(Call to ${ext})
exten => ${ext},n,Wait(1)
exten => ${ext},n,Set(JITTERBUFFER(adaptive)=default)
exten => ${ext},n,Dial(PJSIP/\${EXTEN})
exten => ${ext},n,Hangup

EOF

let ext=$ext+$offset
let count=$count-1

done
