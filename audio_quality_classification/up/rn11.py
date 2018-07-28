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
import matplotlib.pyplot as plt
from sklearn.learning_curve import learning_curve
from sklearn.multiclass import OneVsRestClassifier
from sklearn.metrics import confusion_matrix

rows = []
filename = 'output11.csv'
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


#Train decision tree model
tree = DecisionTreeClassifier(random_state=0).fit(X_train, y_train)
print("Decision Tree")
print("Accuracy on training set: {:.3f}".format(tree.score(X_train, y_train)))
print("Accuracy on test set: {:.3f}".format(tree.score(X_test, y_test)))
print("Accuracy on test set: {:.3f}".format(tree.score(X1, y1)))

#Train random forest model
forest = RandomForestClassifier(n_estimators=5, random_state=0).fit(X_train, y_train)
print("Random Forests")
print("Accuracy on training set: {:.3f}".format(forest.score(X_train, y_train)))
print("Accuracy on test set: {:.3f}".format(forest.score(X_test, y_test)))
print("Accuracy on test set: {:.3f}".format(forest.score(X1, y1)))



#Train support vector machine model


def gaussianKernelGramMatrixFull(X1, X2, sigma=0.1):
    """(Pre)calculates Gram Matrix K"""

    gram_matrix = np.zeros((X1.shape[0], X2.shape[0]))
    for i, x1 in enumerate(X1):
        for j, x2 in enumerate(X2):
            x1 = x1.flatten()
            x2 = x2.flatten()
            gram_matrix[i, j] = np.exp(- np.sum( np.power((x1 - x2),2) ) / float( 2*(sigma**2) ) )
    return gram_matrix


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

#Train neural network model
mlp = MLPClassifier(random_state=0,hidden_layer_sizes=(80,25)).fit(X_train, y_train)
print("Multilayer Perceptron")
print("Accuracy on training set: {:.3f}".format(mlp.score(X_train, y_train)))
print("Accuracy on test set: {:.3f}".format(mlp.score(X_test, y_test)))
print("Accuracy on test set: {:.3f}".format(mlp.score(X1, y1)))
#print("Accuracy on test set: {:.3f}".format(mlp.score(X2, rows1[:,136])))
#print(mlp.predict(X1))



#train_sizes, train_scores, test_scores = learning_curve(
        #svm, X_train, y_train, cv=10, n_jobs=-1, train_sizes=np.linspace(.1, 1., 10), verbose=0)

#train_scores_mean = np.mean(train_scores, axis=1)
#train_scores_std = np.std(train_scores, axis=1)
#test_scores_mean = np.mean(test_scores, axis=1)
#test_scores_std = np.std(test_scores, axis=1)

#plt.figure()
#plt.title("Classifier")
#plt.legend(loc="best")
#plt.xlabel("Training examples")
#plt.ylabel("Score")
#plt.ylim((0.2, 1.01))
#plt.gca().invert_yaxis()
#plt.grid()

# Plot the average training and test score lines at each training set size
#plt.plot(train_sizes, train_scores_mean, 'o-', color="b", label="Training score")
#plt.plot(train_sizes, test_scores_mean, 'o-', color="r", label="Test score")

# Plot the std deviation as a transparent range at each training set size
#plt.fill_between(train_sizes, train_scores_mean - train_scores_std, train_scores_mean + train_scores_std, alpha=0.1, color="b")
#plt.fill_between(train_sizes, test_scores_mean - test_scores_std, test_scores_mean + test_scores_std, alpha=0.1, color="r")

# Draw the plot and reset the y-axis
#plt.draw()
#plt.show()
#plt.gca().invert_yaxis()

