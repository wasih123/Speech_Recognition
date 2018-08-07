from pyAudioAnalysis import audioBasicIO
from pyAudioAnalysis import audioFeatureExtraction
from statistics import mean, stdev
import numpy as np
import csv
import timeit

start = timeit.default_timer()

#import matplotlib.pyplot as plt
l1=[]
for i in range(501,1501,1):
	try:
		[Fs, x] = audioBasicIO.readAudioFile("rej_"+str(i)+".wav")
		F = audioFeatureExtraction.stFeatureExtraction(x, Fs, 0.05*Fs, 0.025*Fs)
	#x=audioBasicIO.stereo2mono(x)
	except:
		continue
	print(1)
	print(i)
	k = 0
	while k<len(F[0]):
		l = []
		for j in range(34):
			l.append(np.percentile(F[j,k:k+399],25))
			l.append(np.percentile(F[j,k:k+399],50))
			l.append(np.percentile(F[j,k:k+399],75))
			l.append(np.percentile(F[j,k:k+399],95))
		
		print(k)
		l.append(len(F[j])/399)
		l.append(1)
		l1.append(l)
		k = k+399
for i in range(501,1501,1):
	try:
		[Fs, x] = audioBasicIO.readAudioFile("acc_"+str(i)+".wav")
		F = audioFeatureExtraction.stFeatureExtraction(x, Fs, 0.05*Fs, 0.025*Fs)
	#x=audioBasicIO.stereo2mono(x)
	except:
		continue
	print(2)
	print(i)
	k = 0
	while k<len(F[0]):
		l = []
		for j in range(34):
			l.append(np.percentile(F[j,k:k+399],25))
			l.append(np.percentile(F[j,k:k+399],50))
			l.append(np.percentile(F[j,k:k+399],75))
			l.append(np.percentile(F[j,k:k+399],95))
		
		print(k)
		l.append(len(F[j])/399)
		l.append(2)
		l1.append(l)
		k = k+399


print(len(l1[0]))
stop = timeit.default_timer()
with open("output12.csv", "w") as f:
    writer = csv.writer(f)
    writer.writerows(l1)
print stop - start

#ffmpeg -i inputfile.flac output.wav