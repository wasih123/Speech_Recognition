import numpy as np
import csv
import soundfile as sf
from pyAudioAnalysis import audioBasicIO
from pyAudioAnalysis import audioFeatureExtraction
from statistics import mean, stdev
#import mglearn
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.svm import SVC
from sklearn.neural_network import MLPClassifier
from sklearn.learning_curve import learning_curve
from sklearn.multiclass import OneVsRestClassifier
from sklearn.metrics import confusion_matrix

rows = []
filename = 'output_train.csv'
with open(filename, 'r') as csvfile:
    csvreader = csv.reader(csvfile)
    fields = csvreader.next()
    for row in csvreader:
        if int(row[137])<3:
            rows.append(row)

rows1=[]
filename1 = 'output111.csv'
with open(filename1, 'r') as csvfile:
	csvreader = csv.reader(csvfile)
	fields = csvreader.next()
	for row in csvreader:
		if  int(row[137])<3:
			rows1.append(row)

rows = np.array(rows)
rows1 = np.array(rows1)
#print(rows[:,136])
'''
for i in range(len(rows[:,137])):
    if int(rows[i,137])<3:
        rows[i,137] = 0
    elif int(rows[i,137])>=3:
        rows[i,137] = 1

for i in range(len(rows1[:,137])):
    if int(rows1[i,137])<3:
        rows1[i,137] = 0
    elif int(rows1[i,137])>=3:
        rows1[i,137] = 1
'''
X_train1, X_test, y_train1, y_test = train_test_split(rows[:,0:137],rows[:,137], random_state=0, test_size=0.2)
X_train,X1,y_train,y1 = train_test_split(X_train1,y_train1, random_state=0, test_size=0.25)
scaler = StandardScaler()
scaler.fit(X_train)
X_train = scaler.transform(X_train)
X_test = scaler.transform(X_test)
X1 = scaler.transform(X1)
X3 = scaler.transform(rows1[:,0:137])
#X2 = scaler.transform(rows1[:,0:136])
#X1 = scaler.transform(rows1[:,0:136])
#y1 = rows1[:,136]




svm =SVC(C=2,gamma=0.03).fit(X_train, y_train) 
print("Support Vector Machine")
print("Accuracy on training set: {:.3f}".format(svm.score(X_train, y_train)))
print("Accuracy on test set: {:.3f}".format(svm.score(X_test, y_test)))
print("Accuracy on test set: {:.3f}".format(svm.score(X1, y1)))
print("Accuracy on test set: {:.3f}".format(svm.score(X3, rows1[:,137])))
x1 = svm.predict(X_test)
x2 = svm.predict(X1)
x3 = svm.predict(X3)
results1 = confusion_matrix(y_test,x1)
results2 = confusion_matrix(y1,x2)
results3 = confusion_matrix(rows1[:,137],x3)
print(results1)
print(results2)
print(results3)
#print("Accuracy on test set: {:.3f}".format(svm.score(X2, rows1[:,136])))
