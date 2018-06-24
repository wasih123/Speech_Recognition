import numpy as np
import csv
import soundfile as sf
from pyAudioAnalysis import audioBasicIO
from pyAudioAnalysis import audioFeatureExtraction
from statistics import mean, stdev
import csv
#import mglearn

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from keras.models import Sequential
from keras.layers import Dense, Dropout


rows = []
filename = 'output2.csv'
with open(filename, 'r') as csvfile:
	csvreader = csv.reader(csvfile)
	fields = csvreader.next()
	for row in csvreader:
		rows.append(row)
rows1=[]
filename1 = 'output3.csv'
with open(filename1, 'r') as csvfile:
	csvreader = csv.reader(csvfile)
	fields = csvreader.next()
	for row in csvreader:
		rows1.append(row)

rows = np.array(rows)
rows1 = np.array(rows1)
#print(rows[:,136])
X_train, X_test, y_train, y_test = train_test_split(rows[:,0:136],rows[:,136], random_state=0, test_size=0.2)
scaler = StandardScaler()
scaler.fit(X_train)
X_train = scaler.transform(X_train)
X_test = scaler.transform(X_test)
X1 = scaler.transform(rows1[:,0:136])
y1 = rows1[:,136]

model = Sequential()
model.add(Dense(25, input_dim=136, activation='relu'))
model.add(Dropout(0.4))
model.add(Dense(10, activation='relu'))
model.add(Dropout(0.4))
model.add(Dense(1, activation='sigmoid'))


model.compile(loss='binary_crossentropy',
              optimizer='rmsprop',
              metrics=['accuracy'])

model.fit(X_train, y_train,
          epochs=10,
          batch_size=128)
score = model.evaluate(X_test, y_test, batch_size=128)
score1 = model.evaluate(X1,y1,batch_size=128)
print(score)
print(score1)
data, samplerate = sf.read('tstm3.wav')
i=0
j=1
temp = samplerate*10
print(temp)
n = (len(data)/temp)
print(n)
while i<len(data):
	sf.write('f'+str(j)+'.wav',data[i:i+temp],samplerate)
	i += temp
	j += 1
l1=[]
for i in range(1,n+1,1):
	l = []
	[Fs, x] = audioBasicIO.readAudioFile("f"+str(i)+".wav")
	#x=audioBasicIO.stereo2mono(x)
	F = audioFeatureExtraction.stFeatureExtraction(x, Fs, 0.05*Fs, 0.025*Fs)
	#print(len(F[0]))
	for j in range(34):
		l.append(min(F[j]))
		l.append(max(F[j]))
		l.append(mean(F[j]))
		l.append(stdev(F[j]))
	l.append(0)
	l1.append(l)
l1 = np.array(l1)
#print(l1[0])
[a,b] = model.evaluate(scaler.transform(l1[:,0:136]),l1[:,136])
if b>0.5:
	print('M')
else:
	print('F')
#print(model.predict(scaler.transform(l1[:,0:136])))
