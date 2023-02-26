# -------------------------------------------------------------------------
# AUTHOR: Edwin O. Rodriguez
# FILENAME: naive_bayes.py
# SPECIFICATION: Question 5
# FOR: CS 4210- Assignment #2
# TIME SPENT: 42 Hours Ultra Combo
# -----------------------------------------------------------*/

#IMPORTANT NOTE: DO NOT USE ANY ADVANCED PYTHON LIBRARY TO COMPLETE THIS CODE SUCH AS numpy OR pandas. You have to work here only with standard
# dictionaries, lists, and arrays

#importing some Python libraries
from sklearn.naive_bayes import GaussianNB
import csv

#reading the training data in a csv file
#--> add your Python code here
db = []
test_db = []
xMap = [[3, "Sunny", "Overcast", "Rain"], [3, "Hot", "Mild", "Cool"], [2, "Normal", "High"]]
yMap = [2, "Yes", "No"]
with open('weather_training.csv', 'r') as csvfile:
  reader = csv.reader(csvfile)
  for i, row in enumerate(reader):
      if i > 0: #skipping the header
         db.append(row)

#transform the original training features to numbers and add them to the 4D array X.
#For instance Sunny = 1, Overcast = 2, Rain = 3, so X = [[3, 1, 1, 2], [1, 3, 2, 2], ...]]
#--> add your Python code here
X = [[0 for j in row[:-1]] for i, row in enumerate(db)]  # Initialize the array, skipping the last col
Y = [0 for i in enumerate(db)]
for i, row in enumerate(db):
    # transform the original training features to numbers and add them to the 4D array X.
    # For instance Sunny = 1, Overcast = 2, Rain = 3, so X = [[3, 1, 1, 2], [1, 3, 2, 2], ...]]
    # --> add your Python code here
    Y[i] = yMap.index(db[i][-1])
    for j, item in enumerate(row[:-1]):
        X[i][j] = xMap[j].index(item)

#fitting the naive bayes to the data
clf = GaussianNB()
clf.fit(X, Y)

#reading the test data in a csv file
#--> add your Python code here
with open('weather_test.csv', 'r') as csvfile:
  reader = csv.reader(csvfile)
  for i, row in enumerate(reader):
      if i > 0: #skipping the header
         test_db.append(row)

#printing the header as the solution
#--> add your Python code here
print("Day".ljust(15) + "Outlook".ljust(15) + "Temperature".ljust(15) + "Humidity".ljust(15) + "Wind".ljust(15) + "PlayTennis".ljust(15) + "Confidence".ljust(15))

#use your test samples to make probabilistic predictions. For instance: clf.predict_proba([[3, 1, 2, 1]])[0]
#--> add your Python code here


