# Pandas is a software library written for the Python programming language for data manipulation and analysis.
import pandas as pd
# NumPy is a library for the Python programming language, adding support for large, multi-dimensional arrays and matrices, along with a large collection of high-level mathematical functions to operate on these arrays
import numpy as np
# Matplotlib is a plotting library for python and pyplot gives us a MatLab like plotting framework. We will use this in our plotter function to plot data.
import matplotlib.pyplot as plt
#Seaborn is a Python data visualization library based on matplotlib. It provides a high-level interface for drawing attractive and informative statistical graphics
import seaborn as sns
# Preprocessing allows us to standarsize our data
from sklearn import preprocessing
# Allows us to split our data into training and testing data
from sklearn.model_selection import train_test_split
# Allows us to test parameters of classification algorithms and find the best one
from sklearn.model_selection import GridSearchCV
# Logistic Regression classification algorithm
from sklearn.linear_model import LogisticRegression
# Support Vector Machine classification algorithm
from sklearn.svm import SVC
# Decision Tree classification algorithm
from sklearn.tree import DecisionTreeClassifier
# K Nearest Neighbors classification algorithm
from sklearn.neighbors import KNeighborsClassifier

# This function is to plot the confusion matrix.

def plot_confusion_matrix(y,y_predict):
    "this function plots the confusion matrix"
    from sklearn.metrics import confusion_matrix

    cm = confusion_matrix(y, y_predict)
    ax= plt.subplot()
    sns.heatmap(cm, annot=True, ax = ax); #annot=True to annotate cells
    ax.set_xlabel('Predicted labels')
    ax.set_ylabel('True labels')
    ax.set_title('Confusion Matrix'); 
    ax.xaxis.set_ticklabels(['did not land', 'land']); ax.yaxis.set_ticklabels(['did not land', 'landed'])
    plt.show()

# Load the data
data = pd.read_csv("https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/dataset_part_2.csv")

# If you were unable to complete the previous lab correctly you can uncomment and load this csv

# data = pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DS0701EN-SkillsNetwork/api/dataset_part_2.csv')

# print(data.head())
#    FlightNumber        Date BoosterVersion  PayloadMass Orbit  ... ReusedCount Serial   Longitude   Latitude  Class
# 0             1  2010-06-04       Falcon 9  6104.959412   LEO  ...           0  B0003  -80.577366  28.561857      0
# 1             2  2012-05-22       Falcon 9   525.000000   LEO  ...           0  B0005  -80.577366  28.561857      0
# 2             3  2013-03-01       Falcon 9   677.000000   ISS  ...           0  B0007  -80.577366  28.561857      0
# 3             4  2013-09-29       Falcon 9   500.000000    PO  ...           0  B1003 -120.610829  34.632093      0
# 4             5  2013-12-03       Falcon 9  3170.000000   GTO  ...           0  B1004  -80.577366  28.561857      0

# [5 rows x 18 columns]

X = pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/dataset_part_3.csv')

# If you were unable to complete the previous lab correctly you can uncomment and load this csv

# X = pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DS0701EN-SkillsNetwork/api/dataset_part_3.csv')

# print(X.head(100))
#     FlightNumber   PayloadMass  Flights  Block  ReusedCount  ...  GridFins_True  Reused_False  Reused_True  Legs_False  Legs_True
# 0            1.0   6104.959412      1.0    1.0          0.0  ...            0.0           1.0          0.0         1.0        0.0 
# 1            2.0    525.000000      1.0    1.0          0.0  ...            0.0           1.0          0.0         1.0        0.0 
# 2            3.0    677.000000      1.0    1.0          0.0  ...            0.0           1.0          0.0         1.0        0.0 
# 3            4.0    500.000000      1.0    1.0          0.0  ...            0.0           1.0          0.0         1.0        0.0 
# 4            5.0   3170.000000      1.0    1.0          0.0  ...            0.0           1.0          0.0         1.0        0.0 
# ..           ...           ...      ...    ...          ...  ...            ...           ...          ...         ...        ... 
# 85          86.0  15400.000000      2.0    5.0          2.0  ...            1.0           0.0          1.0         0.0        1.0 
# 86          87.0  15400.000000      3.0    5.0          2.0  ...            1.0           0.0          1.0         0.0        1.0 
# 87          88.0  15400.000000      6.0    5.0          5.0  ...            1.0           0.0          1.0         0.0        1.0 
# 88          89.0  15400.000000      3.0    5.0          2.0  ...            1.0           0.0          1.0         0.0        1.0 
# 89          90.0   3681.000000      1.0    5.0          0.0  ...            1.0           1.0          0.0         0.0        1.0 

# [90 rows x 83 columns]
# Create a NumPy array from the column <code>Class</code> in <code>data</code>, by applying the method <code>to_numpy()</code>  then
# assign it  to the variable <code>Y</code>,make sure the output is a  Pandas series (only one bracket df\['name of  column']).
# for comparing the accuracy by the methods
methods = []
accuracy = []

Y = data["Class"].to_numpy()
# print(Y.type())
#  print(Y.type())
# AttributeError: 'numpy.ndarray' object has no attribute 'type'
# print(Y)
# [0 0 0 0 0 0 1 1 0 0 0 0 1 0 0 0 1 0 0 1 1 1 1 1 0 1 1 0 1 1 0 1 1 1 0 1 1
#  1 1 1 1 1 1 1 1 0 0 0 1 1 0 0 1 1 1 1 1 1 1 0 0 1 1 1 1 1 1 0 1 1 1 1 0 1
#  0 1 0 1 1 1 1 1 1 1 1 1 1 1 1 1]
# Standardize the data in <code>X</code> then reassign it to the variable  <code>X</code> using the transform provided below.
# students get this 
transform = preprocessing.StandardScaler()
X = transform.fit_transform(X)

# We split the data into training and testing data using the  function  <code>train_test_split</code>.   The training data is divided into validation data, a second set used for training  data; then the models are trained and hyperparameters are selected using the function <code>GridSearchCV</code>.

# Use the function train_test_split to split the data X and Y into training and test data. Set the parameter test_size to  0.2 and random_state to 2. The training data and test data should be assigned to the following labels.

X_train,X_test, Y_train, Y_test = train_test_split(X,Y,test_size=0.2,random_state=2)
# print(Y_test.shape)
# (18,)
# Create a logistic regression object  then create a  GridSearchCV object  <code>logreg_cv</code> with cv = 10.  Fit the object to find the best parameters from the dictionary <code>parameters</code>.
parameters ={'C':[0.01,0.1,1],
             'penalty':['l2'],
             'solver':['lbfgs']}
lr=LogisticRegression()
logreg_cv = GridSearchCV(lr,parameters,cv=10)
logreg_cv.fit(X_train,Y_train)
# We output the <code>GridSearchCV</code> object for logistic regression. We display the best parameters using the data attribute <code>best_params\_</code> and the accuracy on the validation data using the data attribute <code>best_score\_</code>.

print("tuned hpyerparameters :(best parameters) ",logreg_cv.best_params_)
print("accuracy :",logreg_cv.best_score_)
# tuned hpyerparameters :(best parameters)  {'C': 0.01, 'penalty': 'l2', 'solver': 'lbfgs'}
# accuracy : 0.8464285714285713

# accuracy = logreg_cv.score(X_test,Y_test)
# print("Test accuracy:", accuracy)

methods.append('Logistic regression')
accuracy.append(logreg_cv.score(X_test,Y_test))




# Test accuracy: 0.8333333333333334

yhat=logreg_cv.predict(X_test)
plot_confusion_matrix(Y_test,yhat)

# Examining the confusion matrix, we see that logistic regression can distinguish between the different classes.  We see that the major problem is false positives.


# Create a support vector machine object then  create a  <code>GridSearchCV</code> object  <code>svm_cv</code> with cv - 10.  Fit the object to find the best parameters from the dictionary <code>parameters</code>.

parameters = {'kernel':('linear', 'rbf','poly','rbf', 'sigmoid'),
              'C': np.logspace(-3, 3, 5),
              'gamma':np.logspace(-3, 3, 5)}
svm = SVC()
svm_cv = GridSearchCV(svm,parameters,cv=10)
svm_cv.fit(X_train,Y_train)
print("tuned hpyerparameters :(best parameters) ",svm_cv.best_params_)
print("accuracy :",svm_cv.best_score_)

# tuned hpyerparameters :(best parameters)  {'C': 1.0, 'gamma': 0.03162277660168379, 'kernel': 'sigmoid'}
# accuracy : 0.8482142857142856

# accuracy = svm_cv.score(X_test,Y_test)


methods.append('Support Vector Machine')
accuracy.append(svm_cv.score(X_test, Y_test))

# print("Test accuracy:", accuracy)
# Test accuracy: 0.8333333333333334
yhat  = svm_cv.predict(X_test)
plot_confusion_matrix(Y_test,yhat)

# Create a decision tree classifier object then  create a  <code>GridSearchCV</code> object  <code>tree_cv</code> with cv = 10.  Fit the object to find the best parameters from the dictionary <code>parameters</code>.

parameters = {'criterion': ['gini', 'entropy'],
     'splitter': ['best', 'random'],
     'max_depth': [2*n for n in range(1,10)],
     'max_features': ['auto', 'sqrt'],
     'min_samples_leaf': [1, 2, 4],
     'min_samples_split': [2, 5, 10]}

tree = DecisionTreeClassifier()
tree_cv = GridSearchCV(tree,parameters,cv=10)
tree_cv.fit(X_train,Y_train)
print("tuned hpyerparameters :(best parameters) ",tree_cv.best_params_)
print("accuracy :",tree_cv.best_score_)

# tuned hpyerparameters :(best parameters)  {'criterion': 'entropy', 'max_depth': 16, 'max_features': 'auto', 'min_samples_leaf': 2, 'min_samples_split': 5, 'splitter': 'random'}
# accuracy : 0.8732142857142857
score_dt = tree_cv.score(X_test,Y_test)


methods.append('Decision Tree Classifier')
accuracy.append(tree_cv.score(X_test, Y_test))

# print("Score :",score_dt)
# Score : 0.7222222222222222
yhat = tree_cv.predict(X_test)
plot_confusion_matrix(Y_test,yhat)

# Create a k nearest neighbors object then  create a  <code>GridSearchCV</code> object  <code>knn_cv</code> with cv = 10.  Fit the object to find the best parameters from the dictionary <code>parameters</code>.


parameters = {'n_neighbors': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
              'algorithm': ['auto', 'ball_tree', 'kd_tree', 'brute'],
              'p': [1,2]}

KNN = KNeighborsClassifier()
knn_cv = GridSearchCV(KNN,parameters,cv=10)
knn_cv.fit(X_train,Y_train)
print("tuned hpyerparameters :(best parameters) ",knn_cv.best_params_)
print("accuracy :",knn_cv.best_score_)
# tuned hpyerparameters :(best parameters)  {'algorithm': 'auto', 'n_neighbors': 10, 'p': 1}
# accuracy : 0.8482142857142858

# Calculate the accuracy of tree_cv on the test data using the method <code>score</code>:
# print(knn_cv.score(X_test,Y_test))


methods.append('K Neighbors Classifier')
accuracy.append(knn_cv.score(X_test, Y_test))
# 0.8333333333333334
yhat = knn_cv.predict(X_test)
plot_confusion_matrix(Y_test,yhat)

# scores = [lr_score,svm_score,tree_score,knn_score]
# print(scores)
# print(scores.index(max(scores)))
# [0.8333333333333334, 0.8333333333333334, 0.7777777777777778, 0.8333333333333334]

plt.barh(methods, accuracy)
plt.xlabel('Accuracy')
plt.ylabel('Method')
plt.show()