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

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


def remove_silence(input_audio):
	'''
	This will produce an audio with silent parts removed
	Input: audio file(in .wav format)
	Output: audio file with silence removed(in .wav format); name is input_audio_rmsilence.wav by default
	'''
	output_audio, ext = os.path.splitext(input_audio)
	output_audio += '_rmsilence.wav'
	sln.remove_silence(input_audio, output_audio)
#***************************************************---------------------------------------------------------------------------*************************************************

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


def train(train_file,test_file):
	learn.train_model(train_file,test_file)

#***************************************************---------------------------------------------------------------------------*************************************************	



























