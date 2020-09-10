from vosk import Model, KaldiRecognizer
import os
import json
import time
import sys
import pyaudio

if not os.path.exists("model"):
    print ("Please download the model from https://github.com/alphacep/vosk-api/blob/master/doc/models.md and unpack as 'model' in the current folder.")
    exit (1)

model = Model("model")
rec = KaldiRecognizer(model, 16000)

p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000)
stream.start_stream()
result=""
init_time = time.time()
while True:
    current_time = time.time()
    if current_time - init_time < 5:    
        data = stream.read(4000)
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            #print(rec.Result())
            result=result+" "+json.loads(rec.Result())['text']
            print(result)
        else:
            pass
    else:
        break

result=result+json.load(rec.FinalResult())['text']
print(result)
