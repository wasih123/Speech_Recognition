from pyAudioAnalysis import audioBasicIO
from pyAudioAnalysis import audioFeatureExtraction
from statistics import mean, stdev
import csv
import timeit

start = timeit.default_timer()

#import matplotlib.pyplot as plt
l1=[]
for i in range(1,488,1):
	l = []
	[Fs, x] = audioBasicIO.readAudioFile("f"+str(i)+".wav")
	#x=audioBasicIO.stereo2mono(x)
	F = audioFeatureExtraction.stFeatureExtraction(x, Fs, 0.05*Fs, 0.025*Fs)
	print(len(F[0]))
	for j in range(34):
		l.append(min(F[j]))
		l.append(max(F[j]))
		l.append(mean(F[j]))
		l.append(stdev(F[j]))
	l.append(1)
	l1.append(l)
for i in range(1,488,1):
	l = []
	[Fs, x] = audioBasicIO.readAudioFile("m"+str(i)+".wav")
	#x=audioBasicIO.stereo2mono(x)
	F = audioFeatureExtraction.stFeatureExtraction(x, Fs, 0.05*Fs, 0.025*Fs)
	print(len(F[0]))
	for j in range(34):
		l.append(min(F[j]))
		l.append(max(F[j]))
		l.append(mean(F[j]))
		l.append(stdev(F[j]))
	l.append(0)
	l1.append(l)
print(len(l1[0]))
stop = timeit.default_timer()
with open("output1.csv", "w") as f:
    writer = csv.writer(f)
    writer.writerows(l1)
print stop - start

#ffmpeg -i inputfile.flac output.wav