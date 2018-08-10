import os
from subprocess import Popen

def convert_mp3_to_wav(filename):
	'''
	Given an mp3 file, this function will create a corresponding .wav file in the same location where .mp3 file is there
	'''
	if (filename.endswith(".mp3")): #or .avi, .mpeg, whatever.
		[a, b] = filename.split('.')
		p = Popen(['ffmpeg -i ' + filename + ' -acodec pcm_s16le -ac 1 -ar 16000 ' + a + '.wav'.format(filename)], shell = True)
		p.wait()
