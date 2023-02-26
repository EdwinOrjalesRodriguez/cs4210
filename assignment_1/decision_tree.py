#-------------------------------------------------------------------------
# AUTHOR: Edwin O. Rodriguez
# FILENAME: decision_tree.py
# SPECIFICATION: Prints a decision tree in ugly colors from CSV
# FOR: CS 4210- Assignment #1
# TIME SPENT: 8 Hours
#-----------------------------------------------------------*/

#IMPORTANT NOTE: DO NOT USE ANY ADVANCED PYTHON LIBRARY TO COMPLETE THIS CODE SUCH AS numpy OR pandas. You have to work here only with standard
# dictionaries, lists, and arrays

#importing some Python libraries
from sklearn import tree
import matplotlib.pyplot as plt
import csv
db = []
X = []
Y = []
xMap = [[3, "Young", "Prepresbyopic", "Presbyopic"], [2, "Myope", "Hypermetrope"], [2, "Yes", "No"], [2, "Normal", "Reduced"]]
yMap = [2, "Yes", "No"]

#reading the data in a csv file
with open('contact_lens.csv', 'r') as csvfile:
  reader = csv.reader(csvfile)
  for i, row in enumerate(reader):
      if i > 0: #skipping the header
         db.append (row)
         print(row)

X = [[0 for j in row[:-1]] for i, row in enumerate(db)]  # Initialize the array, skipping the last col
Y = [0 for i in enumerate(db)]
for i, row in enumerate(db):
    # transform the original categorical training classes to numbers and add to the vector Y. For instance Yes = 1, No = 2, so Y = [1, 1, 2, 2, ...]
    # --> add your Python code here
    Y[i] = yMap.index(db[i][-1])
    for j, item in enumerate(row[:-1]):
        X[i][j] = xMap[j].index(item)

#fitting the decision tree to the data
clf = tree.DecisionTreeClassifier(criterion = 'entropy')
clf = clf.fit(X, Y)

#plotting the decision tree
tree.plot_tree(clf, feature_names=['Age', 'Spectacle', 'Astigmatism', 'Tear'], class_names=['Yes','No'], filled=True, rounded=True)
plt.show()