#for now just focus on running script for just one input file
import soundfile as sf
import os
from subprocess import Popen, PIPE
import numpy
import shutil
import json
import sys

audio = str(sys.argv[1])
path1 = '/home/wasih/Desktop/Speech_Recognition/New/audio'
os.environ["input"] = path1+'/'+audio
p1 = Popen(['ffmpeg -i ${input} temp.flac -loglevel quiet'],shell='true')
p1.wait()
p2 = Popen(['ffmpeg -i temp.flac -ac 1 mono.flac -loglevel quiet'],shell='true')
p2.wait()
os.remove('temp.flac')
print('Step 1 Done!')
#converted audio mp3 to mono.flac.

#now create chunks of 14 size flacs.
data,rate = sf.read('mono.flac')
print(rate)
#do block-wise reading of the file, mono.flac
path = '/home/wasih/Desktop/Speech_Recognition/New/Chunks'
if not os.path.exists(path):
    os.makedirs(path)
d,r = sf.read('mono.flac',rate*14,0)
sf.write(path+'/chunk0.flac',d,rate)
d,r = sf.read('mono.flac',frames = rate*15,start = rate*14)
sf.write(path+'/chunk1.flac',d,rate)

j = 2
for block in sf.blocks('mono.flac',blocksize = rate*14, start = rate*30):
	sf.write(path+'/chunk'+ str(j) +'.flac',block,rate)
	j = j + 1

os.remove('mono.flac')
print('Step 2 Done!')
#generated blocks of 14s duration flac files

#now upload the files on cloud bucket using gsutil
chunks = os.listdir(path)
for chunk in chunks:
	os.environ["object"] = chunk
	os.environ["path"] = path + '/' + chunk
	p = Popen(['gsutil cp ${path} gs://hindi786'],shell='true')
	p.wait()
	p = Popen(['gsutil acl ch -u AllUsers:R gs://hindi786/${object}'],shell='true')
	p.wait()

shutil.rmtree(path)
print('Step 3 Done!')
#uploaded chunks on cloud bucket

#now call speech api on each of the chunks
fp = open('access-token','r')
token = fp.readline()
token = token[:-1]
os.environ["token"] = token

def request_write(filename):	#make the json file sync-request.json using dict data structure and filename as uri parameter
	#dict has key(string):value pairs, separated by commas and enclosed in braces; value can itself be a dict or a list of dicts, and so on.
	d = {"config":{"encoding":"FLAC","languageCode":"hi-IN","enableWordTimeOffsets":False},"audio":{"uri":"gs://hindi786/"+filename}}
	fp = open('sync-request.json','w')
	json.dump(d,fp,indent=4)
	fp.close()

out_path = '/home/wasih/Desktop/Speech_Recognition/New/Out_Chunks'
for chunk in chunks:
	request_write(chunk)
	out_file = out_path+'/out_'+chunk[:-5]+'.txt'
	p = Popen(['curl -s -H "Content-Type: application/json" \-H "Authorization: Bearer ${token}" \https://speech.googleapis.com/v1/speech:recognize \-d @sync-request.json'], stdout=PIPE, stderr=PIPE,shell='True')
	stdout, stderr = p.communicate()
	if not os.path.exists(out_path):
    		os.makedirs(out_path)
	fp = open(out_file,'w')
	fp.write(stdout.decode("utf-8"))
	p.wait()

for chunk in chunks:
	os.environ["file"] = chunk
	p = Popen(['gsutil rm gs://hindi786/${file}'],shell='True')
	p.wait()

print('Step 4 Done!')
#got transcripts for all the chunks
