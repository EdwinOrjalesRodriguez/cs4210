# -------------------------------------------------------------------------
# AUTHOR: Edwin O. Rodriguez
# FILENAME: decision_tree_2.py
# SPECIFICATION: Question 2
# FOR: CS 4210- Assignment #2
# TIME SPENT: 20 Hours
# -----------------------------------------------------------*/

# IMPORTANT NOTE: DO NOT USE ANY ADVANCED PYTHON LIBRARY TO COMPLETE THIS CODE SUCH AS numpy OR pandas. You have to work here only with standard
# dictionaries, lists, and arrays

# importing some Python libraries
from sklearn import tree
import csv

dataSets = ['contact_lens_training_1.csv', 'contact_lens_training_2.csv', 'contact_lens_training_3.csv']

for ds in dataSets:

    dbTraining = []
    X = []
    Y = []
    xMap = [[3, "Young", "Prepresbyopic", "Presbyopic"], [2, "Myope", "Hypermetrope", "Hypermetrope"], [2, "Yes", "No"],
            [2, "Normal", "Reduced"]]
    yMap = [2, "Yes", "No"]
    accuracyFloor = 1

    # reading the training data in a csv file
    with open(ds, 'r') as csvfile:
        reader = csv.reader(csvfile)
        for i, row in enumerate(reader):
            if i > 0:  # skipping the header
                dbTraining.append(row)

    # transform the original categorical training features to numbers and add to the 4D array X. For instance Young = 1, Prepresbyopic = 2, Presbyopic = 3
    # so X = [[1, 1, 1, 1], [2, 2, 2, 2], ...]]
    # --> add your Python code here

    X = [[0 for j in row[:-1]] for i, row in enumerate(dbTraining)]  # Initialize the array, skipping the last col
    Y = [0 for i in enumerate(dbTraining)]
    for i, row in enumerate(dbTraining):
        # transform the original categorical training classes to numbers and add to the vector Y. For instance Yes = 1, No = 2, so Y = [1, 1, 2, 2, ...]
        # --> add your Python code here
        Y[i] = yMap.index(dbTraining[i][-1])
        for j, item in enumerate(row[:-1]):
            X[i][j] = xMap[j].index(item)
    # loop your training and test tasks 10 times here
    for i in range(10):

        # fitting the decision tree to the data setting max_depth=3
        clf = tree.DecisionTreeClassifier(criterion='entropy', max_depth=3)
        clf = clf.fit(X, Y)
        # read the test data and add this data to dbTest
        # --> add your Python code here
        dbTest = []
        with open('contact_lens_test.csv', 'r') as csvfile:
            reader = csv.reader(csvfile)
            for i, row in enumerate(reader):
                if i > 0:  # skipping the header
                    dbTest.append(row)

        # transform the features of the test instances to numbers following the same strategy done during training,
        testX = [[0 for k in row[:-1]] for j, row in enumerate(dbTest)]  # Initialize the array, skipping the last col
        testY = [0 for j in enumerate(dbTest)]

        # Parse array
        for j, row in enumerate(dbTest):
            testY[j] = yMap.index(dbTest[j][-1])
            for k, item in enumerate(row[:-1]):
                testX[j][k] = xMap[k].index(item)
        # and then use the decision tree to make the class prediction. For instance: class_predicted = clf.predict([[3, 1, 2, 1]])[0]
        # where [0] is used to get an integer as the predicted class label so that you can compare it with the true label
        # --> add your Python code here
        c = 0
        for row in range(len(testX)):
            class_predicted = clf.predict([testX[row]])[0]
            if testY[row] == class_predicted:
                c += 1
        accuracy = c/len(testX)
        if accuracy < accuracyFloor:
            accuracyFloor = accuracy
    print(f'Accuracy ({ds}): {accuracyFloor:.3f}')