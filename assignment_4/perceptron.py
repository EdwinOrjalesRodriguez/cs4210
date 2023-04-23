#-------------------------------------------------------------------------
# AUTHOR: Edwin O. Rodriguez
# FILENAME: perceptron.py
# SPECIFICATION: Accuracy comparison
# FOR: CS 4210- Assignment #4
# TIME SPENT: 64 hours
#-----------------------------------------------------------*/

#IMPORTANT NOTE: YOU HAVE TO WORK WITH THE PYTHON LIBRARIES numpy AND pandas to complete this code.

#importing some Python libraries
from sklearn.linear_model import Perceptron
from sklearn.neural_network import MLPClassifier #pip install scikit-learn==0.18.rc2 if needed
import numpy as np
import pandas as pd
from sklearn.linear_model import Perceptron
from sklearn.neural_network import MLPClassifier #pip install scikit-learn==0.18.rc2 if needed

n = [0.0001, 0.0005, 0.001, 0.005, 0.01, 0.05, 0.1, 0.5, 1.0]
r = [True, False]

df = pd.read_csv('optdigits.tra', sep=',', header=None) #reading the data by using Pandas library

X_training = np.array(df.values)[:,:64] #getting the first 64 fields to form the feature data for training
y_training = np.array(df.values)[:,-1]  #getting the last field to form the class label for training

df = pd.read_csv('optdigits.tes', sep=',', header=None) #reading the data by using Pandas library

X_test = np.array(df.values)[:,:64]    #getting the first 64 fields to form the feature data for test
y_test = np.array(df.values)[:,-1]     #getting the last field to form the class label for test

top_accuracy_perceptron = 0
top_accuracy_mlp = 0

for learning_rate in n: #iterates over n

    for bool in r: #iterates over r

        #iterates over both algorithms
        #-->add your Pyhton code here

        for i in range(2): #iterates over the algorithms

            #Create a Neural Network classifier
            #if Perceptron then
            #   clf = Perceptron()    #use those hyperparameters: eta0 = learning rate, shuffle = shuffle the training data, max_iter=1000
            #else:
            #   clf = MLPClassifier() #use those hyperparameters: activation='logistic', learning_rate_init = learning rate, hidden_layer_sizes = number of neurons in the ith hidden layer,
            #                          shuffle = shuffle the training data, max_iter=1000
            #-->add your Pyhton code here
            if i == 0:
                clf = Perceptron(eta0=learning_rate, shuffle=bool, max_iter=1000)
            else:
                clf = MLPClassifier(activation='logistic', learning_rate_init=learning_rate, hidden_layer_sizes=(100,),
                                    shuffle=bool, max_iter=1000)

            #Fit the Neural Network to the training data
            clf.fit(X_training, y_training)

            #make the classifier prediction for each test sample and start computing its accuracy
            #hint: to iterate over two collections simultaneously with zip() Example:
            #for (x_testSample, y_testSample) in zip(X_test, y_test):
            #to make a prediction do: clf.predict([x_testSample])
            #--> add your Python code here
            right = 0
            for (x_testSample, y_testSample) in zip(X_test, y_test):
                class_predicted = clf.predict([x_testSample])
                if class_predicted == y_testSample:
                    right = right + 1
            accuracy = right / len(y_test)

            #check if the calculated accuracy is higher than the previously one calculated for each classifier. If so, update the highest accuracy
            #and print it together with the network hyperparameters
            #Example: "Highest Perceptron accuracy so far: 0.88, Parameters: learning rate=0.01, shuffle=True"
            #Example: "Highest MLP accuracy so far: 0.90, Parameters: learning rate=0.02, shuffle=False"
            #--> add your Python code here
            if i == 0 and top_accuracy_perceptron < accuracy:
                top_accuracy_perceptron = accuracy
                print("Highest Perceptron accuracy so far:", round(top_accuracy_perceptron, 3), ", Parameters: learning rate=", learning_rate, ", shuffle=", bool)
            if i == 1 and top_accuracy_mlp < accuracy:
                top_accuracy_mlp = accuracy
                print("Highest MLP accuracy so far:", round(top_accuracy_mlp, 3), ", Parameters: learning rate=", learning_rate,", shuffle=", bool)
