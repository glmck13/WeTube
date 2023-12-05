#!/usr/bin/env python3

import sys, os

#AGIVARS = sys.stdin.read()
INFILE = sys.argv[1]
FORMAT = INFILE.split('.')[-1]

os.environ["OPENAI_API_KEY"] = ""
from openai import OpenAI
client = OpenAI()

with open(INFILE, "rb") as f:
    transcript = client.audio.transcriptions.create(model="whisper-1", language="en", response_format="text", file=f)

with open(INFILE[:INFILE.rfind(FORMAT)-1] + ".txt", "w") as f:
    f.write(transcript)
