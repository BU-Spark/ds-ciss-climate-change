import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix

# load training data into pandas df
X_train = pd.read_csv("src/data/train_created.csv")
X_test = pd.read_csv("src/data/nychanow_pass_two.csv")

# learn the model
X_train_processed = np.array(X_train['relevance score']).reshape(-1,1)
Y_train = X_train['class']
model = KNeighborsClassifier().fit(X_train_processed,Y_train)

# predict type of article based on model
X_test = np.array(X_test['relevance score']).reshape(-1,1)
Y_test_predictions = model.predict(X_test)
print(Y_test_predictions)
# evaluate model on the testing set
# print("Accuracy on testing set = ", accuracy_score(Y_test, Y_test_predictions))