# -------------------------------------------------------------------------
# AUTHOR: Edwin O. Rodriguez
# FILENAME: knn.py
# SPECIFICATION: Question 3
# FOR: CS 4210- Assignment #2
# TIME SPENT: 24 Hours
# -----------------------------------------------------------*/

#IMPORTANT NOTE: DO NOT USE ANY ADVANCED PYTHON LIBRARY TO COMPLETE THIS CODE SUCH AS numpy OR pandas. You have to work here only with standard vectors and arrays

#importing some Python libraries
from sklearn.neighbors import KNeighborsClassifier
import csv

db = []
err = 0
#reading the data in a csv file
with open('binary_points.csv', 'r') as csvfile:
  reader = csv.reader(csvfile)
  for i, row in enumerate(reader):
      if i > 0: #skipping the header
         db.append(row)

#loop your data to allow each instance to be your test set
for i, instance in enumerate(db):
    #add the training features to the 2D array X removing the instance that will be used for testing in this iteration. For instance, X = [[1, 3], [2, 1,], ...]]. Convert each feature value to
    # float to avoid warning messages
    #--> add your Python code here
    ilen = len(instance)
    X = []
    Y = []
    for j, row in enumerate(db):
        if j != i:
            # transform the original training classes to numbers and add to the vector Y removing the instance that will be used for testing in this iteration. For instance, Y = [1, 2, ,...]. Convert each
            #  feature value to float to avoid warning messages
            # --> add your Python code here
            X.append([float(x) for x in row[:-1]]) # Adds rows which are not current instance to X, skipping CLASS column
            Y.append(float(1) if row[-1] == "-" else float(2))

    #store the test sample of this iteration in the vector testSample
    #--> add your Python code here
    testSample = []
    for j in range(ilen):
        if j < (ilen-1):
            testSample.append(float(instance[j]))
        else:
            testSample.append(float(1) if instance[j] == "-" else float(2))

    #fitting the knn to the data
    clf = KNeighborsClassifier(n_neighbors=1, p=2)
    clf = clf.fit(X, Y)

    #use your test sample in this iteration to make the class prediction. For instance:
    #class_predicted = clf.predict([[1, 2]])[0]
    #--> add your Python code here
    class_predicted = clf.predict([testSample[0:2]])[0]

    #compare the prediction with the true label of the test instance to start calculating the error rate.
    #--> add your Python code here
    if testSample[(ilen-1)] != class_predicted:
        err += 1

#print the error rate
#--> add your Python code here
print('Error rate', err/len(db))
