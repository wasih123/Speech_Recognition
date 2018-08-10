import soundfile as sf
import os
from subprocess import Popen, PIPE
import numpy
import shutil
import json
import sys

#accept a list of audio files and generate a mega transcript file
#input_audio = sys.argv[1:]

#first activate service account and verify credentials and then generate access-token file
os.system('gcloud auth activate-service-account  --key-file=key.json')
os.environ['GOOGLE_APPLICATION_CREDENTIALS']='/home/wasih/Desktop/Speech_Recognition/key.json'
os.system('gcloud auth application-default print-access-token > access-token')

F = open('AutomaticTrans.txt','w')
path = '/home/wasih/Desktop/Speech_Recognition/New/audio'
input_audio = os.listdir(path)

for audio in input_audio:
	print(audio)
	os.environ["audio"]=audio
	p = Popen(['python script.py ${audio}'], shell='true')
	p.wait()
	p = Popen(['python combine_script.py ${audio}'], shell='true')
	p.wait()
	f = open('MainTranscript.txt','r')
	lines = f.readlines()
	for line in lines:
		F.write(line)
	os.remove('MainTranscript.txt')
	print('Audio:'+audio+' done!'+'\n')
	
F.close()
print('Completed!!')

