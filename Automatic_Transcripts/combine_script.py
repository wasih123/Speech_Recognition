import sys
import os
import json
import shutil

class Time(object):
    mins = 0
    sec = 0
    def __init__(self,mins,sec):
		self.mins = mins
		self.sec = sec
    def changeMins(self,mins):
    	self.mins = mins
    def changeSecs(self,sec):
    	self.sec = sec
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def integrate_transcripts(audio_file_name):
	'''
	Given the audio file name, this function will make one file(MainTranscript.txt) by concatenating all the chunks of this audio file
	'''
	out_path = os.path.join(os.getcwd() + 'Out_Chunks')
	#now combine them into a single file
	transcripts = os.listdir(out_path)
	#first create ordered transcript on the basis of chunk numbers
	#print(transcripts)
	for i in range(0, len(transcripts)):
		number = int(transcripts[i][9:-4])
		transcripts[i] = number

	transcripts.sort()
	#print(transcripts)
	F = open('MainTranscript.txt','w')
	F.write(audio_file_name)
	F.write('\n\n\n')
	cur_time = Time(0,0)
	ite = 0
	for transcript in transcripts:
		name = 'out_chunk' + str(transcript) + '.txt'
		f = open(os.path.join(out_path, name), 'r')
		if(cur_time.sec >= 60):
			cur_time.changeSecs(cur_time.sec - 60)
			cur_time.changeMins(cur_time.mins + 1)
		string1 = "{0:0>2}".format(cur_time.mins)
		string2 = "{0:0>2}".format(cur_time.sec)
		if(ite<2):
			cur_time.changeSecs(cur_time.sec+14)
		else:
			cur_time.changeSecs(cur_time.sec+13)
		if(cur_time.sec >= 60):
			cur_time.changeSecs(cur_time.sec - 60)
			cur_time.changeMins(cur_time.mins + 1)
		string3 = "{0:0>2}".format(cur_time.mins)
		string4 = "{0:0>2}".format(cur_time.sec)
		data = json.load(f)
		if(len(data)!=0):
			F.write(string1 + '.' + string2 + ' - ' + string3 + '.' + string4 + ' sec - ')
			if(isinstance(data, str)):
				F.write(data[u"results"][0][u"alternatives"][0][u"transcript"])
			else:
				F.write(data["results"][0]["alternatives"][0]["transcript"])
			F.write('\n\n\n')
			cur_time.changeSecs(cur_time.sec + 1)
		ite = ite + 1
	F.close()
	shutil.rmtree(out_path)
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
