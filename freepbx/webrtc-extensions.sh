#!/bin/ksh

ext=${1:?Enter starting extension}
count=${2:?Enter number of extensions}
offset=${3:?Enter offset}

cat - <<-"EOF"
[from-internal-custom]

exten => _**44XX.,1,Noop(Entering user defined context from-internal-custom in extensions_custom.conf)
exten => _**44XX.,n,AGI(agi://pimate.local/polly.sh)
exten => _**44XX.,n,Dial(Local/${EXTEN:4}@from-internal)
exten => _**44XX.,n,Hangup

exten => 411,1,Goto(from-pstn-custom,411,1)
exten => 555,1,Goto(from-pstn-custom,555,1)
exten => 333,1,Goto(from-pstn-custom,333,1)
exten => 222,1,Goto(from-pstn-custom,222,1)
exten => 111,1,Goto(from-pstn-custom,111,1)

exten => 7000,1,Noop(Call to 7000)
exten => 7000,n,AGI(agi://pimate.local/polly.sh)
exten => 7000,n,Dial(PJSIP/6100&PJSIP/6200)
exten => 7000,n,Hangup

EOF

while [ "$count" -gt 0 ]
do
cat - <<EOF
exten => ${ext},1,Noop(Call to ${ext})
exten => ${ext},n,Wait(1)
exten => ${ext},n,Dial(PJSIP/\${EXTEN})
exten => ${ext},n,Hangup

EOF

let ext=$ext+$offset
let count=$count-1

done

cat - <<-"EOF"
[from-pstn-custom]

exten => 411,1,Answer()
exten => 411,n,MP3Player(http://piville.home/public/dmr.cgi)
exten => 411,n,Hangup()

exten => 555,1,Noop(Call to 555)
exten => 555,n,Dial(PJSIP/OBIBOSTON)
exten => 555,n,Hangup

exten => 333,1,Noop(Call to 333)
exten => 333,n,Dial(PJSIP/6100&PJSIP/6200)
exten => 333,n,Hangup

exten => 111,1,Noop(Call to 111)
exten => 111,n,Dial(PJSIP/OBIMDOC)
exten => 111,n,Hangup

exten => 222,1,Answer()
exten => 222,n,Set(VOLUME(TX)=3)
;exten => 222,n,AGI(ttsagi.py,"Hi, I'm G's voice assistant, and I can help you send a text message.",/var/lib/asterisk/sounds/myapp/answer.mp3)
;exten => 222,n,AGI(ttsagi.py,"After the beep, press numbers for everyone you want to send your message to. Press 1 for Mom<break time=\"500ms\"/>, 2 for Dad<break time=\"500ms\"/>, 3 for Dee Dee<break time=\"500ms\"/>, 4 for G<break time=\"500ms\"/>, 5 for Aunt KK<break time=\"500ms\"/>, and 6 for Uncle Daniel. Press star when you're done.",/var/lib/asterisk/sounds/myapp/who.mp3)
;exten => 222,n,AGI(ttsagi.py,"Give me a second to process that...",/var/lib/asterisk/sounds/myapp/pause.mp3)
;exten => 222,n,AGI(ttsagi.py,"Now tell me your message. Start speaking after the beep. Press any key when you're finished.",/var/lib/asterisk/sounds/myapp/what.mp3)
;exten => 222,n,AGI(ttsagi.py,"You said:",/var/lib/asterisk/sounds/myapp/replay.mp3)
;exten => 222,n,AGI(ttsagi.py,"If that's correct, press 1 to continue, or 2 to try again.",/var/lib/asterisk/sounds/myapp/chkwho.mp3)
;exten => 222,n,AGI(ttsagi.py,"If your message sounds OK, press 1 to send it. Otherwise, press 2 to record it again, or 3 to cancel.",/var/lib/asterisk/sounds/myapp/chkwhat.mp3)
;exten => 222,n,AGI(ttsagi.py,"Message canceled!",/var/lib/asterisk/sounds/myapp/canceled.mp3)
;exten => 222,n,AGI(ttsagi.py,"Message sent!",/var/lib/asterisk/sounds/myapp/sent.mp3)
;exten => 222,n,AGI(ttsagi.py,"Goodbye!",/var/lib/asterisk/sounds/myapp/bye.mp3)
;
exten => 222,n(msghello),Playback(myapp/answer)
;
exten => 222,n(msgwho),Playback(myapp/who)
exten => 222,n,Read(CONTACTS,beep,,t(*#))
exten => 222,n,Playback(myapp/pause)
exten => 222,n,AGI(contactsagi.py,${CONTACTS})
exten => 222,n,AGI(ttsagi.py,"${CONTACTS_RSP}",${RECORDED_FILE}.mp3)
;
exten => 222,n(msgloop1),Playback(${RECORDED_FILE})
exten => 222,n,GotoIf($[${LEN(${CONTACTS_LIST})} = 0}]?msgwho)
exten => 222,n,Playback(myapp/chkwho)
exten => 222,n,Read(MYCHOICE,beep,1)
exten => 222,n,GotoIf($["${MYCHOICE}" = "1"]?msgwhat)
exten => 222,n,GotoIf($["${MYCHOICE}" = "2"]?msgwho)
exten => 222,n,Goto(msgloop1)
;
exten => 222,n(msgwhat),Playback(myapp/what)
exten => 222,n,Playback(beep)
exten => 222,n,Record(/tmp/msg%d:wav,,,y)
exten => 222,n,Playback(myapp/pause)
exten => 222,n,AGI(sttagi.py,${RECORDED_FILE}.wav)
;
exten => 222,n(msgloop2),Playback(myapp/replay)
exten => 222,n,Playback(${RECORDED_FILE})
exten => 222,n,Playback(myapp/chkwhat)
exten => 222,n,Read(MYCHOICE,beep,1)
exten => 222,n,GotoIf($["${MYCHOICE}" = "1"]?msgsend)
exten => 222,n,GotoIf($["${MYCHOICE}" = "2"]?msgwhat)
exten => 222,n,GotoIf($["${MYCHOICE}" = "3"]?msgcancel)
exten => 222,n,Goto(msgloop2)
;
exten => 222,n(msgcancel),Playback(myapp/canceled)
exten => 222,n,Goto(msgbye)
;
exten => 222,n(msgsend),System(ffmpeg -i ${RECORDED_FILE}.wav ${RECORDED_FILE}.mp3)
exten => 222,n,Set(id=${CALLERID(all)})
exten => 222,n,AGI(smsagi.py,${RECORDED_FILE},${id},${CONTACTS_LIST})
exten => 222,n,Playback(myapp/sent)
exten => 222,n,Goto(msgbye)
;
exten => 222,n(msgbye),Playback(myapp/bye)
exten => 222,n,hangup
EOF
