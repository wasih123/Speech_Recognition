'''
This is the main library file which will have all the basic functions, we want to provide to the user
We will keep on appending gender, transcripts, silence removal and quality classification parts to this file

Authors: Jayanth Reddy, Mohammad Wasih, Aaditeshwar Seth
Last Modified: 7th August, 2018
'''

'''
Necessory Utilities:

HIGH LEVEL:
1. Remove silence from audio 
2. Get Gender of audio
3. Obtain Transcripts of audio
4. Obtain quality of audio

LOW LEVEL:
> get_feature_representation of an audio
> train neural_network for gender
> train svm for quality
> get accuracy of transcript
...
'''
import os
import sys
import numpy as np
from sklearn.preprocessing import StandardScaler
from keras.models import load_model
from subprocess import Popen
#done with standard imports

import Gender_Classification.integrate as integ
import Gender_Classification.disintegrate as disinteg
import Gender_Classification.mp3_to_wav as mtw
import Gender_Classification.learn as learn
import Gender_Classification.extract_features as exf
import Gender_Classification.excl_http_req as exhr
#done with Gender_Classification imports

import Silence_Removal.sln as sln
#done with Silence_Removal imports

import Automatic_Transcripts.combine_script as cs
import Automatic_Transcripts.script as sc
#done with Automatic_Transcripts imports
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


#LOW LEVEL routines

def train(train_file, test_file):
	'''
	This function will train the neural network;
	train_file is input.csv and test_file is test.csv
	'''
	learn.train_model(train_file,test_file)
#***************************************************---------------------------------------------------------------------------*************************************************	

def authenticate_user(path_to_key):
	'''
	Given path to key.json file(used for authentication), this function will generate access token file
	'''
	os.environ['key_path'] = path_to_key
	p1 = Popen(['gcloud auth activate-service-account --key-file=${key_path}'], shell = 'True')
	p1.wait()
	os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = path_to_key
	p2 = Popen(['gcloud auth application-default print-access-token > access-token'], shell = 'True')
#***************************************************---------------------------------------------------------------------------*************************************************	
	
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------	


#HIGH LEVEL routines

def remove_silence(input_audio):
	'''
	This will produce an audio with silent parts removed
	Input: audio file(in .wav format)
	Output: audio file with silence removed(in .wav format); name is input_audio_rmsilence.wav by default
	'''
	output_audio, ext = os.path.splitext(input_audio)
	output_audio += '_rmsilence.wav'
	sln.remove_silence(input_audio, output_audio)
#***************************************************--------------------------------------------------------------------*********************************************************

def get_gender(input_url, input_audio = None):
	'''
	This will return the predicted gender of the audio file as characterized by its input_url
	Basic Process:
	1. Get mp3 file from input_url
	2. Convert to wav format
	3. Remove silence periods in the wav file
	4. Get feature representation of the wav file by chunking it and appending all features to a list and assume gender is male
	5. Load Gender Classification neural network
	6. Forward pass the feature vector and get the corresponding label
	7. Return the gender(label) to user; male is 0 and female is 1
	'''
	if(input_audio == None):
		exhr.get_audio_from_url(input_url, 'test_point.mp3')
		mtw.convert_mp3_to_wav('test_point.mp3')
		remove_silence('test_point.wav')
		features = np.array(exf.get_features('test_point_rmsilence.wav'))
		print(features)
		model = load_model('gender_nn')
		scaler = StandardScaler()
		scaler.fit(features[:,0:136])
		[a, b] = model.evaluate(scaler.transform(features[:,0:136]), features[:,136])
		if b > 0.5:
			return 0
		else:
			return 1
	
	else:
		mtw.convert_mp3_to_wav(input_audio)
		input_audio_name, ext = os.path.splitext(input_audio)
		input_audio_wav = input_audio_name + '.wav'
		remove_silence(input_audio_wav)
		features = np.array(exf.get_features(input_audio_name + '_rmsilence.wav'))
		model = load_model('gender_nn')
		scaler = StandardScaler()
		scaler.fit(features[:,0:136])
		[a, b] = model.evaluate(scaler.transform(features[:,0:136]), features[:,136])
		if b > 0.5:
			return 0
		else:
			return 1
#***************************************************---------------------------------------------------------------------------*************************************************	

def get_automatic_transcript(input_url, path_to_key, bucket_name, input_audio = None, silence_removal = None):
	'''
	Given an input_url or input_audio in .mp3 format and whether to remove silence or not;
	this function will generate a file, 'AutomaticTrans.txt' which will contain the automatic transcript for this audio
	'''
	authenticate_user(path_to_key)
	if(input_audio == None):
		exhr.get_audio_from_url(input_url, 'test_point.mp3')
		mtw.convert_mp3_to_wav('test_point.mp3')
		if(silence_removal):
			remove_silence('test_point.wav')
			sc.get_transcript('test_point_rmsilence.wav', bucket_name)
			cs.integrate_transcripts('test_point_rmsilence.wav')
		else:
			sc.get_transcript('test_point.wav')
			cs.integrate_transcripts('test_point.wav')
	
	else:
		mtw.convert_mp3_to_wav(input_audio)
		input_audio_name, ext = os.path.splitext(input_audio)
		input_audio_wav = input_audio_name + '.wav'
		if(silence_removal):
			remove_silenc
			e(input_audio_wav)
			sc.get_transcript(input_audio_name + '_rmsilence.wav')
			cs.integrate_transcripts(input_audio_name + '_rmsilence.wav')
		else:
			sc.get_transcript(input_audio_name)
			cs.integrate_transcripts(input_audio_name)
	
	F = open('AutomaticTrans.txt', 'w')
	f = open('MainTranscript.txt', 'r')
	lines = f.readlines()
	for line in lines:
		F.write(line)
	os.remove('MainTranscript.txt')
	F.close()
#********************************************************---------------------------------------------------------------------**************************************************























