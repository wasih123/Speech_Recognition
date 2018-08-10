from pyAudioAnalysis import audioBasicIO
from pyAudioAnalysis import audioFeatureExtraction
from statistics import mean, stdev
import csv
import timeit
import soundfile as sf


def get_features(input_file, gender = 0):
	'''
	Given an input .wav file and its gender, this function will return a list of lists corresponding to features of each of its chunks
	male is 0
	female is 1;
	by default we will assume gender to be male(0) and then we will compare our test predictions with gender = male and decide what did the model predict the gender as
	'''
	data, samplerate = sf.read(input_file)
	i=0
	j=1
	temp = samplerate*10
	n = (len(data)/temp)
	while i<len(data):
		sf.write('m' + str(j) + '.wav', data[i:i+temp], samplerate)
		i += temp
		j += 1
	l1=[]
	for i in range(1, n+1, 1):
		l = []
		[Fs, x] = audioBasicIO.readAudioFile("m" + str(i) + ".wav")
		F = audioFeatureExtraction.stFeatureExtraction(x, Fs, 0.05*Fs, 0.025*Fs)
		for j in range(34):
			l.append(min(F[j]))
			l.append(max(F[j]))
			l.append(mean(F[j]))
			l.append(stdev(F[j]))
		l.append(gender)
		l1.append(l)
	return l1
#******************************************************-----------------------------------------------------------------------*************************************************

def generate_data(output_csv):
	'''
	This function will read in the entire liste of audio files and extract features from them and append to output_csv
	'''
	l1=[]
	for i in range(1,488,1):
		l = []
		[Fs, x] = audioBasicIO.readAudioFile("f" + str(i) + ".wav")
		F = audioFeatureExtraction.stFeatureExtraction(x, Fs, 0.05*Fs, 0.025*Fs)
		for j in range(34):
			l.append(min(F[j]))
			l.append(max(F[j]))
			l.append(mean(F[j]))
			l.append(stdev(F[j]))
		l.append(1)
		l1.append(l)
	for i in range(1,488,1):
		l = []
		[Fs, x] = audioBasicIO.readAudioFile("m" + str(i) + ".wav")
		F = audioFeatureExtraction.stFeatureExtraction(x, Fs, 0.05*Fs, 0.025*Fs)
		for j in range(34):
			l.append(min(F[j]))
			l.append(max(F[j]))
			l.append(mean(F[j]))
			l.append(stdev(F[j]))
		l.append(0)
		l1.append(l)
	with open(output_csv, "w") as f:
		writer = csv.writer(f)
		writer.writerows(l1)
#******************************************************-----------------------------------------------------------------------**************************************************
